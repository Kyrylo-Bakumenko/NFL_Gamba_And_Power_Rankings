"""Download historical NFL odds from Australia Sports Betting."""
from __future__ import annotations

import io
from pathlib import Path
import pandas as pd
import requests

AUSSPORTS_URL = "https://www.aussportsbetting.com/historical_data/nfl.xlsx"


def fetch_historical_vegas(save_file: Path | None = None) -> pd.DataFrame:
    """Fetch historical Vegas lines (since 2006) from aussportsbetting.com.

    Parameters
    ----------
    save_file : Path, optional
        If provided, the downloaded Excel file will be saved here.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``game_id``, ``date``, ``home_team``, ``away_team``,
        ``spread_close``, ``total_close``, ``moneyline_home``, ``moneyline_away``.
    """
    resp = requests.get(AUSSPORTS_URL, stream=True)
    resp.raise_for_status()
    content = resp.content
    if save_file is not None:
        Path(save_file).write_bytes(content)

    df = pd.read_excel(io.BytesIO(content))

    df = df.rename(
        columns={
            "Date": "date",
            "Home Team": "home_team",
            "Away Team": "away_team",
            "Home Line Close": "home_line_close",
            "Away Line Close": "away_line_close",
            "Home Odds Close": "home_odds_close",
            "Away Odds Close": "away_odds_close",
            "Total Score Close": "total_close",
        }
    )

    # Remove rows without date
    df = df[df["date"].notna()].copy()

    # compute derived fields
    df["spread_close"] = -df["home_line_close"].astype(float)
    df["moneyline_home"] = df["home_odds_close"].astype(float)
    df["moneyline_away"] = df["away_odds_close"].astype(float)

    df["game_id"] = (
        df["date"].dt.strftime("%Y%m%d")
        + "_"
        + df["away_team"].str.replace(" ", "", regex=False)
        + "@"
        + df["home_team"].str.replace(" ", "", regex=False)
    )

    return df[
        [
            "game_id",
            "date",
            "home_team",
            "away_team",
            "spread_close",
            "total_close",
            "moneyline_home",
            "moneyline_away",
        ]
    ]


__all__ = ["fetch_historical_vegas"]

