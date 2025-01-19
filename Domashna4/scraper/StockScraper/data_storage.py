import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import psycopg2
from psycopg2.extensions import connection, cursor

# Configuration class using Singleton pattern
class DatabaseConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.db_url = os.getenv('DB_URL', "postgresql://dians:dians123@localhost:9555/diansdb")
            self.initialized = True

# Database connection factory
class DatabaseConnectionFactory:
    @staticmethod
    def create_connection() -> connection:
        config = DatabaseConfig()
        return psycopg2.connect(config.db_url)

# Abstract strategy for database operations
class DatabaseStrategy(ABC):
    @abstractmethod
    def execute_query(self, conn: connection, query: str, params: tuple = None) -> Any:
        pass

# Concrete strategies
class QueryStrategy(DatabaseStrategy):
    def execute_query(self, conn: connection, query: str, params: tuple = None) -> List[tuple]:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

class UpdateStrategy(DatabaseStrategy):
    def execute_query(self, conn: connection, query: str, params: tuple = None) -> None:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()

class BatchInsertStrategy(DatabaseStrategy):
    def execute_query(self, conn: connection, query: str, params: List[tuple]) -> None:
        with conn.cursor() as cur:
            cur.executemany(query, params)
            conn.commit()

# Data models using Value Object pattern
class IssuerDate:
    def __init__(self, issuer: str, last_date: datetime):
        self.issuer = issuer
        self.last_date = last_date

class IssuerData:
    def __init__(self, date: datetime, issuer: str, avg_price: str, last_trade_price: str,
                 max_price: str, min_price: str, percent_change: str, turnover_best: str,
                 total_turnover: str, volume: str):
        self.date = date
        self.issuer = issuer
        self.avg_price = avg_price
        self.last_trade_price = last_trade_price
        self.max_price = max_price
        self.min_price = min_price
        self.percent_change = percent_change
        self.turnover_best = turnover_best
        self.total_turnover = total_turnover
        self.volume = volume

# Repository pattern for data access
class DataRepository:
    def __init__(self):
        self.connection_factory = DatabaseConnectionFactory()
        self.query_strategy = QueryStrategy()
        self.update_strategy = UpdateStrategy()
        self.batch_strategy = BatchInsertStrategy()
        self._initialize_db()

    def _initialize_db(self) -> None:
        create_tables_query = """
            CREATE TABLE IF NOT EXISTS issuer_dates (
                issuer TEXT PRIMARY KEY,
                last_date DATE
            );
            CREATE TABLE IF NOT EXISTS issuer_data (
                date DATE,
                issuer TEXT,
                avg_price TEXT,
                last_trade_price TEXT,
                max_price TEXT,
                min_price TEXT,
                percent_change TEXT,
                turnover_best TEXT,
                total_turnover TEXT,
                volume TEXT,
                PRIMARY KEY (date, issuer)
            );
        """
        with self.connection_factory.create_connection() as conn:
            self.update_strategy.execute_query(conn, create_tables_query)

    def load_issuer_dates(self) -> Dict[str, datetime]:
        query = "SELECT issuer, last_date FROM issuer_dates"
        with self.connection_factory.create_connection() as conn:
            results = self.query_strategy.execute_query(conn, query)
            return {row[0]: row[1] for row in results}

    def update_issuer_date(self, issuer_date: IssuerDate) -> None:
        query = """
            INSERT INTO issuer_dates (issuer, last_date)
            VALUES (%s, %s)
            ON CONFLICT (issuer) DO UPDATE
            SET last_date = EXCLUDED.last_date
        """
        date_str = issuer_date.last_date.strftime('%Y-%m-%d') if issuer_date.last_date else None
        with self.connection_factory.create_connection() as conn:
            self.update_strategy.execute_query(conn, query, (issuer_date.issuer, date_str))

    def get_issuer_date(self, issuer: str) -> Optional[datetime]:
        query = "SELECT last_date FROM issuer_dates WHERE issuer = %s"
        with self.connection_factory.create_connection() as conn:
            results = self.query_strategy.execute_query(conn, query, (issuer,))
            return results[0][0] if results and results[0][0] else None

    def save_issuer_data(self, data_list: List[IssuerData]) -> None:
        formatted_rows = [
            (
                data.date.strftime("%Y-%m-%d"),
                data.issuer,
                data.avg_price,
                data.last_trade_price,
                data.max_price,
                data.min_price,
                data.percent_change,
                data.turnover_best,
                data.total_turnover,
                data.volume
            )
            for data in data_list
        ]

        query = """
            INSERT INTO issuer_data (
                date, issuer, avg_price, last_trade_price, max_price, min_price,
                percent_change, turnover_best, total_turnover, volume
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date, issuer) DO NOTHING
        """
        
        with self.connection_factory.create_connection() as conn:
            self.batch_strategy.execute_query(conn, query, formatted_rows)

    def get_all_data(self) -> List[IssuerData]:
        query = "SELECT * FROM issuer_data"
        with self.connection_factory.create_connection() as conn:
            results = self.query_strategy.execute_query(conn, query)
            return [
                IssuerData(
                    date=row[0],
                    issuer=row[1],
                    avg_price=row[2],
                    last_trade_price=row[3],
                    max_price=row[4],
                    min_price=row[5],
                    percent_change=row[6],
                    turnover_best=row[7],
                    total_turnover=row[8],
                    volume=row[9]
                )
                for row in results
            ]

    def count_issuer_data_rows(self) -> int:
        query = "SELECT COUNT(*) FROM issuer_data"
        with self.connection_factory.create_connection() as conn:
            results = self.query_strategy.execute_query(conn, query)
            return results[0][0] if results else 0

    def get_by_issuer(self, issuer: str) -> List[IssuerData]:
        query = "SELECT * FROM issuer_data WHERE issuer = %s"
        with self.connection_factory.create_connection() as conn:
            results = self.query_strategy.execute_query(conn, query, (issuer,))
            return [
                IssuerData(
                    date=row[0],
                    issuer=row[1],
                    avg_price=row[2],
                    last_trade_price=row[3],
                    max_price=row[4],
                    min_price=row[5],
                    percent_change=row[6],
                    turnover_best=row[7],
                    total_turnover=row[8],
                    volume=row[9]
                )
                for row in results
            ]