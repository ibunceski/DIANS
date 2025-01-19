from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import logging
import requests
from bs4 import BeautifulSoup, Tag
from requests.exceptions import RequestException

# Data Models
@dataclass
class ScrapingConfig:
    base_url: str = "https://www.mse.mk/mk/stats/symbolhistory"
    max_days_per_request: int = 364
    retry_attempts: int = 3
    timeout_seconds: int = 30

@dataclass
class ScrapingResult:
    data: List[Dict[str, str]]
    success: bool
    error_message: Optional[str] = None

# Abstract base classes for strategy pattern
class DataParser(ABC):
    @abstractmethod
    def parse(self, content: str, issuer: str) -> List[Dict[str, str]]:
        pass

class DataFetcher(ABC):
    @abstractmethod
    def fetch(self, url: str, params: Dict) -> Optional[str]:
        pass

# Concrete implementations
class HTMLTableParser(DataParser):
    COLUMN_NAMES = [
        "Date", "Last trade price", "Max", "Min", "Avg. Price",
        "%chg.", "Volume", "Turnover in BEST in denars", "Total turnover in denars"
    ]

    def parse(self, content: str, issuer: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(content, 'html.parser')
        return self._parse_table(soup, issuer)

    def _parse_table(self, soup: BeautifulSoup, issuer: str) -> List[Dict[str, str]]:
        results = []
        table = soup.select_one('#resultsTable > tbody')
        
        if not table:
            return results

        for row in table.find_all('tr'):
            row_data = self._parse_row(row)
            if row_data:
                row_data['Issuer'] = issuer
                results.append(row_data)

        return results

    def _parse_row(self, row: Tag) -> Optional[Dict[str, str]]:
        row_data = {}
        cells = row.find_all('td')
        
        if len(cells) != len(self.COLUMN_NAMES):
            return None

        for td, column in zip(cells, self.COLUMN_NAMES):
            # Skip empty Max values as they indicate invalid rows
            if column == 'Max' and not td.text.strip():
                return None
            row_data[column] = td.text.strip()

        return row_data

class RequestsFetcher(DataFetcher):
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def fetch(self, url: str, params: Dict) -> Optional[str]:
        for attempt in range(self.config.retry_attempts):
            try:
                response = requests.get(
                    url, 
                    params=params, 
                    timeout=self.config.timeout_seconds
                )
                response.raise_for_status()
                return response.text
            except RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.config.retry_attempts - 1:
                    self.logger.error(f"All attempts failed for URL: {url}")
                    return None
        return None

# Date range iterator for handling large date ranges
class DateRangeIterator:
    def __init__(self, start_date: date, end_date: date, max_days: int):
        self.current = start_date
        self.end_date = end_date
        self.max_days = max_days

    def __iter__(self):
        return self

    def __next__(self) -> tuple[date, date]:
        if self.current >= self.end_date:
            raise StopIteration

        period_end = min(
            self.current + timedelta(days=self.max_days),
            self.end_date
        )
        result = (self.current, period_end)
        self.current = period_end + timedelta(days=1)
        return result

# Main scraper class
class StockDataScraper:
    def __init__(
        self,
        storage: 'DataStorage',
        config: ScrapingConfig = ScrapingConfig(),
        parser: Optional[DataParser] = None,
        fetcher: Optional[DataFetcher] = None
    ):
        self.storage = storage
        self.config = config
        self.parser = parser or HTMLTableParser()
        self.fetcher = fetcher or RequestsFetcher(config)
        self.logger = logging.getLogger(__name__)

    def scrape_issuer_data(self, issuer: str, start_date: date) -> ScrapingResult:
        """
        Scrapes stock data for a given issuer from start_date until today.
        Returns a ScrapingResult containing the scraped data and status information.
        """
        url = f"{self.config.base_url}/{issuer}"
        all_data = []
        
        date_ranges = DateRangeIterator(
            start_date,
            date.today(),
            self.config.max_days_per_request
        )

        try:
            for period_start, period_end in date_ranges:
                params = {
                    "FromDate": self._format_date(period_start),
                    "ToDate": self._format_date(period_end),
                }

                content = self.fetcher.fetch(url, params)
                if not content:
                    return ScrapingResult(
                        data=[],
                        success=False,
                        error_message=f"Failed to fetch data for {issuer}"
                    )

                period_data = self.parser.parse(content, issuer)
                all_data.extend(period_data)

            self._log_results(issuer, all_data)
            return ScrapingResult(data=all_data, success=True)

        except Exception as e:
            error_msg = f"Unexpected error while scraping {issuer}: {str(e)}"
            self.logger.error(error_msg)
            return ScrapingResult(data=[], success=False, error_message=error_msg)

    @staticmethod
    def _format_date(d: date) -> str:
        return d.strftime("%d.%m.%Y")

    def _log_results(self, issuer: str, data: List[Dict[str, str]]) -> None:
        if data:
            self.logger.info(f"Collected {len(data)} rows for {issuer}")
        else:
            self.logger.warning(f"No data collected for {issuer}")