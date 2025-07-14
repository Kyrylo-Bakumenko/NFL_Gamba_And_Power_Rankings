import time
from typing import List
import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.pro-football-reference.com"
REQUESTS_PER_MINUTE = 20


class RateLimitedSession:
    def __init__(self, rpm: int = REQUESTS_PER_MINUTE):
        self.rpm = rpm
        self.session = requests.Session()
        self._last_request = 0.0

    def get(self, url: str) -> requests.Response:
        wait = 60.0 / self.rpm
        delta = time.time() - self._last_request
        if delta < wait:
            time.sleep(wait - delta)
        resp = self.session.get(url)
        self._last_request = time.time()
        resp.raise_for_status()
        return resp


rate_limited_session = RateLimitedSession()


def fetch_snap_counts(season: int) -> pd.DataFrame:
    """Scrape weekly snap counts from PFR."""
    records: List[dict] = []
    for week in range(1, 19):
        url = f"{BASE_URL}/years/{season}/week_{week}.htm"
        resp = rate_limited_session.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", id="player_offense_snap_counts")
        if not table:
            continue
        for row in table.tbody.find_all("tr"):
            if "class" in row.attrs and "thead" in row["class"]:
                continue
            cells = row.find_all(["th", "td"])
            record = {
                "season": season,
                "week": week,
                "player_id": cells[0].get_text(),
                "team": cells[1].get_text(),
                "snaps": int(cells[2].get_text() or 0),
                "unit": "off",
            }
            records.append(record)
    return pd.DataFrame(records)


def fetch_roster(season: int) -> pd.DataFrame:
    """Fetch roster data from PFR depth charts."""
    url = f"{BASE_URL}/teams/"
    teams_resp = rate_limited_session.get(url)
    teams_soup = BeautifulSoup(teams_resp.text, "lxml")
    team_ids = [a['href'].split('/')[2] for a in teams_soup.select('table#teams_active tbody tr th a')]
    records = []
    for team in team_ids:
        roster_url = f"{BASE_URL}/teams/{team}/{season}_snap_counts.htm"
        resp = rate_limited_session.get(roster_url)
        soup = BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", id="games_played_team")
        if not table:
            continue
        for row in table.tbody.find_all("tr"):
            if "class" in row.attrs and "thead" in row["class"]:
                continue
            cells = row.find_all(["th", "td"])
            pid = cells[0].get_text()
            record = {
                "season": season,
                "player_id": pid,
                "team": team,
                "primary_position": cells[1].get_text(),
            }
            records.append(record)
    return pd.DataFrame(records)


__all__ = ["fetch_snap_counts", "fetch_roster"]
