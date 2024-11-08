import concurrent.futures
from datetime import date
import pandas as pd
from pathlib import Path
import time
from hw1.data.data_storage import DataStorage
from hw1.filters.issuer_filter import IssuerFilter
from hw1.filters.stock_data_scraper import StockDataScraper


class StockDataManager:
    def __init__(self, output_dir="../stock_data/"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.output_file = self.output_dir / "issuers_data.csv"
        self.storage = DataStorage()
        self.scraper = StockDataScraper()

    @staticmethod
    def format_price(price):
        if isinstance(price, str) and price != '/':
            price_float = float(price.replace(',', '').replace(' ', ''))
            return f"{price_float:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
        return price

    def load_existing_data(self):
        if self.output_file.exists():
            return pd.read_csv(self.output_file, parse_dates=['datetime_object'])
        else:
            return pd.DataFrame()

    def process_issuer(self, issuer):
        storage_data = self.storage.load_data()
        from_date = storage_data.get(issuer)

        data = self.scraper.scrape_issuer_data(issuer, from_date)

        if data:
            new_df = pd.DataFrame(data)
            new_df['datetime_object'] = pd.to_datetime(new_df['Date'], format="%m/%d/%Y")
            new_df['Date'] = new_df['datetime_object'].dt.strftime('%d.%m.%Y')

            price_columns = [
                'Last trade price', 'Max', 'Min', "%chg.", "Avg. Price",
                'Turnover in BEST in denars', 'Total turnover in denars'
            ]
            for col in price_columns:
                new_df[col] = new_df[col].apply(self.format_price)

            self.storage.update_issuer(issuer, date.today().strftime("%m/%d/%Y"))
            print(f"Data scraped for {issuer}")

            return new_df
        else:
            print(f"No data collected for {issuer}")
            return pd.DataFrame()

    def process_all_issuers(self, max_workers=8):
        issuers = IssuerFilter.get_all_issuers()

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.process_issuer, issuers)

        new_data = pd.concat([df for df in results if not df.empty])

        existing_data = self.load_existing_data()
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['Date', 'Issuer'])
        combined_data = combined_data.sort_values(by=['Issuer', 'datetime_object'])

        combined_data.to_csv(self.output_file, index=False)
        print(f"All data successfully saved to {self.output_file}")


def main():
    manager = StockDataManager()
    manager.process_all_issuers()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
