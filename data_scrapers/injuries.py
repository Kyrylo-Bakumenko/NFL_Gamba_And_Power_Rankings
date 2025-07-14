"""Scrape weekly injury report from the NFL site via Selenium."""

from __future__ import annotations

from typing import List
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .selenium_utils import RateLimitedWebDriver


NFL_INJURY_URL = "https://www.nfl.com/injuries/"


def fetch_injuries(rpm: int = 20, headless: bool = True) -> pd.DataFrame:
    """Fetch injury table by rendering the page with Selenium."""
    driver = RateLimitedWebDriver(rpm=rpm, headless=headless)
    driver.get_page(NFL_INJURY_URL)

    # Wait for table rows to load
    WebDriverWait(driver.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    rows = driver.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    records: List[dict] = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            records.append(
                {
                    "player": cells[0].text.strip(),
                    "team": cells[1].text.strip(),
                    "injury": cells[2].text.strip(),
                    "status": cells[3].text.strip(),
                }
            )

    driver.quit()
    return pd.DataFrame(records)


__all__ = ["fetch_injuries"]
