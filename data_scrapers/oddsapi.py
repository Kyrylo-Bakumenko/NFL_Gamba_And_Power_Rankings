"""Scrape Vegas lines from a public webpage using Selenium."""

from __future__ import annotations

import pandas as pd
from bs4 import BeautifulSoup

from .selenium_utils import RateLimitedWebDriver

VEGAS_URL = "https://www.vegasinsider.com/nfl/odds/las-vegas/"


def fetch_vegas_lines(rpm: int = 10, headless: bool = True) -> pd.DataFrame:
    """Return latest Vegas lines scraped from VegasInsider."""
    driver = RateLimitedWebDriver(rpm=rpm, headless=headless)
    html = driver.get_page(VEGAS_URL)
    driver.quit()

    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return pd.DataFrame()
    df = pd.read_html(str(table))[0]
    return df


__all__ = ["fetch_vegas_lines"]
