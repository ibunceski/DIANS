import concurrent.futures
from datetime import date
import pandas as pd
from pathlib import Path

from hw1.data.data_storage import DataStorage
from hw1.filters.issuer_filter import IssuerFilter
from hw1.filters.stock_data_scraper import StockDataScraper


class StockDataManager:
    def __init__(self, output_dir="../stock_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.storage = DataStorage()
        self.scraper = StockDataScraper()

    def process_issuer(self, issuer):
        storage_data = self.storage.load_data()
        from_date = storage_data.get(issuer)

        data = self.scraper.scrape_issuer_data(issuer, from_date)

        if data:
            df = pd.DataFrame(data)
            df['datetime_parsed'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
            df = df.sort_values(by="date_parsed")

            output_file = self.output_dir / f"{issuer}.csv"
            df.to_csv(output_file, index=False)

            self.storage.update_issuer(issuer, date.today().strftime("%m/%d/%Y"))

            print(f"Successfully saved {len(df)} records for {issuer}")
        else:
            print(f"No data collected for {issuer}")

    def process_all_issuers(self, max_workers=8):
        # issuers = IssuerFilter.get_all_issuers()
        issuers = ["MKPT", "ADIN", "ALK", "ALKB", "BIKF", "BGOR", "CEVI", "CKB", "GALE"]

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.process_issuer, issuers)


def main():
    manager = StockDataManager()
    manager.process_all_issuers()


if __name__ == '__main__':
    main()
