"""Synergy model implemented in PyTorch."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Tuple

import torch
from torch import nn


@dataclass
class SynergySample:
    player_i: int
    player_j: int
    result_actual: float
    result_expected: float
    margin_weight: float
    overlap: float


class SynergyModel(nn.Module):
    def __init__(self, num_players: int, rank: int = 8, l2: float = 1e-3):
        super().__init__()
        self.U = nn.Parameter(torch.zeros(num_players, rank))
        self.l2 = l2

    def forward(self, pairs: torch.Tensor) -> torch.Tensor:
        ui = self.U[pairs[:, 0]]
        uj = self.U[pairs[:, 1]]
        return (ui * uj).sum(dim=1)

    def loss(self, pairs: torch.Tensor, pred_win: torch.Tensor, actual_win: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
        logits = self.forward(pairs) + pred_win
        bce = nn.functional.binary_cross_entropy_with_logits(logits, actual_win, weight=weights, reduction="mean")
        reg = self.l2 * torch.mean(self.U ** 2)
        return bce + reg

    def decay(self, decay_rate: float = 0.98):
        with torch.no_grad():
            self.U.mul_(decay_rate)


def train_epoch(model: SynergyModel, data: Iterator[SynergySample], optimizer: torch.optim.Optimizer) -> float:
    total_loss = 0.0
    total_count = 0
    for sample in data:
        pairs = torch.tensor([[sample.player_i, sample.player_j]], dtype=torch.long)
        pred_win = torch.tensor([sample.result_expected], dtype=torch.float)
        actual = torch.tensor([sample.result_actual], dtype=torch.float)
        weight = torch.tensor([sample.margin_weight * sample.overlap], dtype=torch.float)

        loss = model.loss(pairs, pred_win, actual, weight)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        total_count += 1
    return total_loss / max(1, total_count)
