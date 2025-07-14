"""Elo rating core utilities."""
from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Dict

MARGIN_SCALE = 7.0
BYE_WEEK_DECAY = 0.995

# Example K-factor table per position
K_FACTORS = {
    "QB": 60,
    "WR": 35,
    "RB": 35,
    "TE": 35,
    "OL": 25,
    "DL": 25,
    "LB": 25,
    "CB": 25,
    "S": 25,
    "ST": 15,
    "LS": 10,
}


def margin_weight(margin: float, c: float = MARGIN_SCALE) -> float:
    """Return logistic-bounded margin weight."""
    return 2 / (1 + np.exp(-abs(margin) / c)) - 1


def expected_result(rating_a: float, rating_b: float) -> float:
    """Win probability for rating_a against rating_b."""
    return 1 / (1 + 10 ** (-(rating_a - rating_b) / 400))


class EloSystem:
    """Manage Elo ratings for players."""

    def __init__(self, k_factors: Dict[str, float] | None = None, initial_elo: float = 1500):
        self.k_factors = k_factors or K_FACTORS
        self.ratings: Dict[str, float] = {}
        self.initial_elo = initial_elo

    def get_rating(self, player_id: str) -> float:
        return self.ratings.get(player_id, self.initial_elo)

    def update_game(self, game_df: pd.DataFrame) -> None:
        """Update Elo ratings after a game.

        ``game_df`` must contain columns:
        ``player_id``, ``position``, ``snap_share``, ``result_actual`` (0/1),
        ``result_expected`` (probability pre game), ``point_margin``.
        """
        if game_df.empty:
            return

        m_weight = margin_weight(float(game_df["point_margin"].iloc[0]))

        for _, row in game_df.iterrows():
            pid = row["player_id"]
            pos = row["position"]
            snap = row.get("snap_share", 1.0)
            actual = row["result_actual"]
            expected = row["result_expected"]
            rating = self.get_rating(pid)
            k = self.k_factors.get(pos, 20)

            delta = k * m_weight * (actual - expected) * snap
            self.ratings[pid] = rating + delta

    def decay_week(self) -> None:
        for pid in list(self.ratings):
            self.ratings[pid] *= BYE_WEEK_DECAY
