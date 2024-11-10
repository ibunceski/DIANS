import requests
from bs4 import BeautifulSoup
import re


class IssuerFilter:
    @staticmethod
    def get_all_issuers():
        url = "https://www.mse.mk/mk/stats/symbolhistory/ALKB"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        options = soup.select("select > option")

        return [opt.text for opt in options if not re.search(r'\d', opt.text)]
