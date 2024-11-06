from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from hw1.data.data_storage import DataStorage
from hw1.utils.webdriver import WebDriver


class StockDataScraper:
    COLUMN_NAMES = [
        "Date", "Last trade price", "Max", "Min", "Avg. Price",
        "%chg.", "Volume", "Turnover in BEST in denars", "Total turnover in denars"
    ]

    def __init__(self):
        self.storage = DataStorage()

    @staticmethod
    def _format_date(d):
        return d.strftime("%m/%d/%Y")

    @staticmethod
    def _parse_date(date_str):
        return datetime.strptime(date_str, "%m/%d/%Y").date()

    def _scrape_table(self, browser):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        rows = soup.select("tbody > tr")
        if not rows:
            return []

        res = []
        for row in rows:
            parts = row.text.strip().split("\n")
            if len(parts) >= 9:
                row_data = {self.COLUMN_NAMES[i]: parts[i] if len(parts[i]) != 0 else "/"
                            for i in range(len(self.COLUMN_NAMES))}
                res.append(row_data)

        return res

    def scrape_issuer_data(self, issuer, from_date=None):
        today = date.today()
        start_date = (
            self._parse_date(from_date) if from_date
            else today - timedelta(days=3650)  # ~10 years
        )

        browser = WebDriver.setup()
        results = []

        try:
            browser.get(f"https://www.mse.mk/en/stats/symbolhistory/{issuer}")
            current_date = start_date

            while current_date < today:
                end_date = min(current_date + timedelta(days=364), today)

                wait = WebDriverWait(browser, 10)
                find_btn = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "li.container-end > input")))
                from_input = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input#FromDate")))
                to_input = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input#ToDate")))

                for input_field, input_date in [
                    (from_input, current_date),
                    (to_input, end_date)
                ]:
                    input_field.clear()
                    input_field.send_keys(self._format_date(input_date))
                    input_field.send_keys(Keys.RETURN)

                find_btn.click()
                time.sleep(0.04)

                if new_data := self._scrape_table(browser):
                    results.extend(new_data)
                    print(f"Scraped {len(new_data)} rows for {issuer} "
                          f"from {self._format_date(current_date)} "
                          f"to {self._format_date(end_date)}")
                else:
                    print(f"No data found for {issuer} in date range "
                          f"{self._format_date(current_date)} - "
                          f"{self._format_date(end_date)}")

                current_date = end_date + timedelta(days=1)

        except Exception as e:
            print(f"Error scraping {issuer}: {e}")

        finally:
            browser.quit()

        return results
