import sqlite3
from pathlib import Path
from datetime import datetime


class DataStorage:
    def __init__(self, storage_path="issuers_data.db"):
        self.storage_path = str(Path(storage_path))
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.storage_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS issuer_dates (
                    issuer TEXT PRIMARY KEY,
                    last_date TEXT
                )
            """)
            conn.commit()

    def load_data(self):
        try:
            with sqlite3.connect(self.storage_path, timeout=20) as conn:
                cursor = conn.execute("SELECT issuer, last_date FROM issuer_dates")
                return {row[0]: datetime.strptime(row[1], '%Y-%m-%d').date()
                if row[1] else None
                        for row in cursor.fetchall()}
        except sqlite3.Error:
            return {}

    def update_issuer(self, issuer, last_date):
        try:
            with sqlite3.connect(self.storage_path, timeout=20) as conn:
                date_str = last_date.strftime('%Y-%m-%d') if last_date else None
                conn.execute("""
                    INSERT OR REPLACE INTO issuer_dates (issuer, last_date)
                    VALUES (?, ?)
                """, (issuer, date_str))
                conn.commit()
        except sqlite3.Error:
            print("Storage error")

    def get_issuer(self, issuer):
        try:
            with sqlite3.connect(self.storage_path, timeout=20) as conn:
                cursor = conn.execute("""
                    SELECT last_date FROM issuer_dates
                    WHERE issuer = ?
                """, (issuer,))
                row = cursor.fetchone()
                if row and row[0]:
                    return datetime.strptime(row[0], '%Y-%m-%d').date()
                return None
        except sqlite3.Error:
            print("Storage error")
