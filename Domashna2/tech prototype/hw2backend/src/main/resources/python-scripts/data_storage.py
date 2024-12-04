import psycopg2


class DataStorage:
    def __init__(self, db_url="postgresql://ilija:ilija123@localhost:5432/dians_db"):
        self.db_url = db_url
        self._initialize_db()

    def _initialize_db(self):
        try:
            with psycopg2.connect(self.db_url) as conn:
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
                            last_trade_price TEXT,
                            max_price TEXT,
                            min_price TEXT,
                            avg_price TEXT,
                            percent_change TEXT,
                            volume TEXT,
                            turnover_best TEXT,
                            total_turnover TEXT,
                            issuer TEXT,
                            PRIMARY KEY (date, issuer)
                        )
                    """)
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error initializing database: {e}")

    def load_data(self):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT issuer, last_date FROM issuer_dates")
                    return {row[0]: row[1] for row in cursor.fetchall()}
        except psycopg2.Error:
            return {}

    def update_issuer(self, issuer, last_date):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    date_str = last_date.strftime('%Y-%m-%d') if last_date else None
                    cursor.execute("""
                        INSERT INTO issuer_dates (issuer, last_date)
                        VALUES (%s, %s)
                        ON CONFLICT (issuer) DO UPDATE
                        SET last_date = EXCLUDED.last_date
                    """, (issuer, date_str))
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating issuer: {e}")

    def get_issuer_date(self, issuer):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT last_date FROM issuer_dates
                        WHERE issuer = %s
                    """, (issuer,))
                    row = cursor.fetchone()
                    if row and row[0]:
                        return row[0]
                    return None
        except psycopg2.Error as e:
            print(f"Error retrieving issuer date: {e}")
            return None

    def save_issuer_data(self, data_rows):
        """
        Save issuer data into the database.
        :param data_rows: A list of tuples containing issuer data.
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.executemany("""
                        INSERT INTO issuer_data (
                            date, last_trade_price, max_price, min_price, avg_price,
                            percent_change, volume, turnover_best, total_turnover, issuer
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (date, issuer) DO NOTHING
                    """, data_rows)
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error saving issuer data: {e}")

    def get_all_data(self):
        """
        Retrieve and print all data from the database for debugging purposes.
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM issuer_dates")
                    print("Issuer Dates Table:")
                    for row in cursor.fetchall():
                        print(row)

                    cursor.execute("SELECT * FROM issuer_data")
                    print("\nIssuer Data Table:")
                    for row in cursor.fetchall():
                        print(row)
        except psycopg2.Error as e:
            print(f"Error retrieving data: {e}")

    def count_issuer_data_rows(self):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM issuer_data")
                    row_count = cursor.fetchone()[0]
                    return row_count
        except psycopg2.Error as e:
            print(f"Error counting rows in issuer_data table: {e}")
            return 0

    def get_by_issuer(self, issuer):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM issuer_data WHERE issuer = %s
                    """, (issuer,))
                    rows = cursor.fetchall()
                    return rows
        except psycopg2.Error as e:
            print(f"Error retrieving data for issuer {issuer}: {e}")
            return []
