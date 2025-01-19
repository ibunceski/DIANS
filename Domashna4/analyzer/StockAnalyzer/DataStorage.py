import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
import psycopg2
from psycopg2.extensions import connection

# Singleton Pattern for Database Configuration
class DatabaseConfig:
    _instance = None

    def __new__(cls, db_url: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_url = db_url or os.getenv('DB_URL', "postgresql://dians:dians123@localhost:9555/diansdb")
        return cls._instance

    def get_connection(self) -> connection:
        return psycopg2.connect(self.db_url)

# Strategy Pattern for Database Operations
class DatabaseOperation(ABC):
    @abstractmethod
    def initialize_tables(self, conn: connection) -> None:
        pass

    @abstractmethod
    def load_issuer_dates(self, conn: connection) -> Dict[str, datetime]:
        pass

    @abstractmethod
    def update_issuer(self, conn: connection, issuer: str, last_date: Optional[datetime]) -> None:
        pass

    @abstractmethod
    def get_issuer_date(self, conn: connection, issuer: str) -> Optional[datetime]:
        pass

    @abstractmethod
    def save_issuer_data(self, conn: connection, data_rows: List[Tuple]) -> None:
        pass

    @abstractmethod
    def get_all_data(self, conn: connection) -> List[Tuple]:
        pass

    @abstractmethod
    def count_issuer_data_rows(self, conn: connection) -> int:
        pass

    @abstractmethod
    def get_by_issuer(self, conn: connection, issuer: str) -> List[Tuple]:
        pass

# Concrete Strategy for PostgreSQL
class PostgresOperation(DatabaseOperation):
    def initialize_tables(self, conn: connection) -> None:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS issuer_dates (
                    issuer TEXT PRIMARY KEY,
                    last_date DATE
                )
            """)
            cursor.execute("""
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
                )
            """)
            conn.commit()

    def load_issuer_dates(self, conn: connection) -> Dict[str, datetime]:
        with conn.cursor() as cursor:
            cursor.execute("SELECT issuer, last_date FROM issuer_dates")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def update_issuer(self, conn: connection, issuer: str, last_date: Optional[datetime]) -> None:
        with conn.cursor() as cursor:
            date_str = last_date.strftime('%Y-%m-%d') if last_date else None
            cursor.execute("""
                INSERT INTO issuer_dates (issuer, last_date)
                VALUES (%s, %s)
                ON CONFLICT (issuer) DO UPDATE
                SET last_date = EXCLUDED.last_date
            """, (issuer, date_str))
            conn.commit()

    def get_issuer_date(self, conn: connection, issuer: str) -> Optional[datetime]:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT last_date FROM issuer_dates
                WHERE issuer = %s
            """, (issuer,))
            row = cursor.fetchone()
            return row[0] if row and row[0] else None

    def save_issuer_data(self, conn: connection, data_rows: List[Tuple]) -> None:
        with conn.cursor() as cursor:
            formatted_rows = [
                (datetime.strptime(row[0], "%d.%m.%Y").strftime("%Y-%m-%d"), *row[1:])
                for row in data_rows
            ]
            cursor.executemany("""
                INSERT INTO issuer_data (
                    date, issuer, avg_price, last_trade_price, max_price, min_price,
                    percent_change, turnover_best, total_turnover, volume
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (date, issuer) DO NOTHING
            """, formatted_rows)
            conn.commit()

    def get_all_data(self, conn: connection) -> List[Tuple]:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM issuer_data")
            return cursor.fetchall()

    def count_issuer_data_rows(self, conn: connection) -> int:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM issuer_data")
            return cursor.fetchone()[0]

    def get_by_issuer(self, conn: connection, issuer: str) -> List[Tuple]:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM issuer_data WHERE issuer = %s
            """, (issuer,))
            return cursor.fetchall()

# Factory Pattern for Database Operations
class DatabaseOperationFactory:
    @staticmethod
    def create_operation(db_type: str = "postgres") -> DatabaseOperation:
        if db_type.lower() == "postgres":
            return PostgresOperation()
        raise ValueError(f"Unsupported database type: {db_type}")

# Facade Pattern - Maintains the same public interface
class DataStorage:
    def __init__(self, db_url: Optional[str] = None):
        self.db_config = DatabaseConfig(db_url)
        self.db_operation = DatabaseOperationFactory.create_operation("postgres")
        self._initialize_db()

    def _initialize_db(self) -> None:
        try:
            with self.db_config.get_connection() as conn:
                self.db_operation.initialize_tables(conn)
        except psycopg2.Error as e:
            print(f"Error initializing database: {e}")

    def load_data(self) -> Dict[str, datetime]:
        try:
            with self.db_config.get_connection() as conn:
                return self.db_operation.load_issuer_dates(conn)
        except psycopg2.Error:
            return {}

    def update_issuer(self, issuer: str, last_date: Optional[datetime]) -> None:
        try:
            with self.db_config.get_connection() as conn:
                self.db_operation.update_issuer(conn, issuer, last_date)
        except psycopg2.Error as e:
            print(f"Error updating issuer: {e}")

    def get_issuer_date(self, issuer: str) -> Optional[datetime]:
        try:
            with self.db_config.get_connection() as conn:
                return self.db_operation.get_issuer_date(conn, issuer)
        except psycopg2.Error as e:
            print(f"Error retrieving issuer date: {e}")
            return None

    def save_issuer_data(self, data_rows: List[Tuple]) -> None:
        try:
            with self.db_config.get_connection() as conn:
                self.db_operation.save_issuer_data(conn, data_rows)
        except ValueError as ve:
            print(f"Date format error: {ve}")
        except psycopg2.Error as e:
            print(f"Error saving issuer data: {e}")

    def get_all_data(self) -> List[Tuple]:
        try:
            with self.db_config.get_connection() as conn:
                return self.db_operation.get_all_data(conn)
        except psycopg2.Error as e:
            print(f"Error retrieving data: {e}")
            return []

    def count_issuer_data_rows(self) -> int:
        try:
            with self.db_config.get_connection() as conn:
                return self.db_operation.count_issuer_data_rows(conn)
        except psycopg2.Error as e:
            print(f"Error counting rows: {e}")
            return 0

    def get_by_issuer(self, issuer: str) -> List[Tuple]:
        try:
            with self.db_config.get_connection() as conn:
                return self.db_operation.get_by_issuer(conn, issuer)
        except psycopg2.Error as e:
            print(f"Error retrieving data for issuer {issuer}: {e}")
            return []