"""Example script fetching various datasets for Elo-Core."""
from pathlib import Path
import pandas as pd
from data_scrapers import (
    fetch_pbp,
    fetch_games,
    fetch_snap_counts,
    fetch_roster,
    fetch_vegas_lines,
    fetch_historical_vegas,
    fetch_injuries,
    fetch_draft_combine,
)


def main():
    season = 2023
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    pbp = fetch_pbp(season)
    pbp.to_parquet(data_dir / f"pbp_{season}.parquet")

    games = fetch_games(season)
    games.to_parquet(data_dir / f"games_{season}.parquet")

    snaps = fetch_snap_counts(season)
    snaps.to_parquet(data_dir / f"snaps_{season}.parquet")

    roster = fetch_roster(season)
    roster.to_parquet(data_dir / f"roster_{season}.parquet")

    injuries = fetch_injuries()
    injuries.to_parquet(data_dir / f"injuries_{season}.parquet")

    lines = fetch_vegas_lines()
    lines.to_parquet(data_dir / f"lines_{season}.parquet")

    hist = fetch_historical_vegas()
    hist.to_parquet(data_dir / "vegas_history.parquet")

    draft = fetch_draft_combine()
    draft.to_parquet(data_dir / "draft_combine.parquet")


if __name__ == "__main__":
    main()
