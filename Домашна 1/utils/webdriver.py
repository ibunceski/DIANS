from selenium import webdriver


class WebDriver:
    @staticmethod
    def setup():
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)
