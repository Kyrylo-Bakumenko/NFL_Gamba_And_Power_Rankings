import io
from typing import Optional
import pandas as pd
import requests


GITHUB_BASE = "https://raw.githubusercontent.com/nflverse/nflfastR-data/master/data"


def fetch_pbp(season: int) -> pd.DataFrame:
    """Download play-by-play parquet for a season."""
    url = f"{GITHUB_BASE}/play_by_play/pbp_{season}.parquet"
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return pd.read_parquet(io.BytesIO(resp.content))


def fetch_games(season: int) -> pd.DataFrame:
    """Download games metadata."""
    url = f"{GITHUB_BASE}/games/games_{season}.parquet"
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return pd.read_parquet(io.BytesIO(resp.content))


__all__ = ["fetch_pbp", "fetch_games"]
