import concurrent.futures
import pandas as pd
from pathlib import Path

from Domashna1.app.filter1 import IssuerFilter
from Domashna1.app.filter2 import DataDateChecker
from Domashna1.app.filter3 import DataFetcher


class Pipeline:
    def __init__(self, storage, scraper, output_dir="../stock_data/"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.output_file = self.output_dir / "issuers_data.csv"
        self.storage = storage
        self.scraper = scraper
        self.issuer_filter = IssuerFilter()
        self.date_checker = DataDateChecker(self.storage)
        self.data_fetcher = DataFetcher(self.scraper, self.storage)

    def load_existing_data(self):
        if self.output_file.exists():
            return pd.read_csv(self.output_file, parse_dates=['datetime_object'])
        else:
            return pd.DataFrame()

    def process_issuer(self, issuer):
        last_date = self.date_checker.get_last_data_date(issuer)
        data = self.data_fetcher.fetch_missing_data(issuer, last_date)
        return data

    def run_pipeline(self, max_workers=8):
        issuers = self.issuer_filter.get_all_issuers()

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.process_issuer, issuers)

        non_empty_results = [df for df in results if not df.empty]

        if non_empty_results:
            new_data = pd.concat(non_empty_results)

            existing_data = self.load_existing_data()
            combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['Date', 'Issuer'])
            combined_data = combined_data.sort_values(by=['Issuer', 'datetime_object'])

            combined_data.to_csv(self.output_file, index=False)
            print(f"All data successfully saved to {self.output_file}")
        else:
            print("All data up to date")
