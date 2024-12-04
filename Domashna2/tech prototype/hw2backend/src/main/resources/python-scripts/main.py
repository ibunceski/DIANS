from pipeline import Pipeline
from stock_data_scraper import StockDataScraper
from data_storage import DataStorage
import time


def main():
    storage = DataStorage()
    scraper = StockDataScraper()
    pipeline = Pipeline(storage, scraper)
    pipeline.run_pipeline()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
