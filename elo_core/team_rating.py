"""Team rating computation combining talent and synergy."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict

import numpy as np

from .elo import EloSystem
from .synergy import SynergyModel


@dataclass
class TeamInfo:
    team_id: str
    players: Iterable[str]
    covariates: Dict[str, float]


def compute_team_rating(
    team: TeamInfo,
    elo: EloSystem,
    synergy: SynergyModel | None = None,
    player_to_idx: Dict[str, int] | None = None,
    alpha: float = 0.5,
    beta: float = 0.5,
) -> float:
    talent = np.mean([elo.get_rating(p) for p in team.players])
    synergy_score = 0.0
    if synergy is not None and player_to_idx:
        idxs = [player_to_idx[p] for p in team.players if p in player_to_idx]
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                synergy_score += float((synergy.U[idxs[i]] * synergy.U[idxs[j]]).sum())
    covariate_score = sum(team.covariates.values())
    return alpha * talent + beta * synergy_score + covariate_score
