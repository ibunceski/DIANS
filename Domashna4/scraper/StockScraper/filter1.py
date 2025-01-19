import re
import requests
from bs4 import BeautifulSoup


class IssuerFilter:

    @staticmethod
    def get_all_issuers():
        resp = requests.get("https://www.mse.mk/en/stats/current-schedule")
        soup = BeautifulSoup(resp.text, "html.parser")
        codes = soup.select("tr > td > a")
        return sorted([code.text for code in codes if not re.search(r'\d', code.text)])
