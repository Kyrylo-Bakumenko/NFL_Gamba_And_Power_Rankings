import io
import pandas as pd
import requests

NFLFASTR_BASE = "https://raw.githubusercontent.com/nflverse/nflfastR-data/master/data"


def fetch_draft_combine() -> pd.DataFrame:
    url = f"{NFLFASTR_BASE}/roster-data/players.csv"
    resp = requests.get(url)
    resp.raise_for_status()
    return pd.read_csv(io.BytesIO(resp.content))


__all__ = ["fetch_draft_combine"]
