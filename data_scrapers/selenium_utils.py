import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class RateLimitedWebDriver:
    """Minimal wrapper around Selenium driver with rate limiting."""

    def __init__(self, rpm: int = 20, headless: bool = True):
        self.rpm = rpm
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=opts)
        self._last = 0.0

    def get_page(self, url: str) -> str:
        wait = 60.0 / self.rpm
        now = time.time()
        delta = now - self._last
        if delta < wait:
            time.sleep(wait - delta)
        self.driver.get(url)
        self._last = time.time()
        return self.driver.page_source

    def quit(self) -> None:
        self.driver.quit()
