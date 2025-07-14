from datetime import datetime
from typing import Optional
import pandas as pd
import requests

METEOSTAT_URL = "https://meteostat.p.rapidapi.com/games/nfl"


def fetch_game_weather(game_id: str, api_key: str, api_host: str) -> pd.DataFrame:
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host,
    }
    resp = requests.get(f"{METEOSTAT_URL}/{game_id}", headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data.get("data", []))


__all__ = ["fetch_game_weather"]
