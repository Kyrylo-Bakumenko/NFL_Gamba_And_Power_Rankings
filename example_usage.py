"""Example of updating player Elo ratings and synergy."""
import pandas as pd
from elo_core.elo import EloSystem
from elo_core.synergy import SynergyModel, SynergySample, train_epoch
from elo_core.team_rating import TeamInfo, compute_team_rating
import torch

# Fake game data for demonstration
example_game = pd.DataFrame([
    {
        "player_id": "p1",
        "position": "QB",
        "snap_share": 1.0,
        "result_actual": 1.0,
        "result_expected": 0.55,
        "point_margin": 7,
    },
    {
        "player_id": "p2",
        "position": "WR",
        "snap_share": 0.8,
        "result_actual": 1.0,
        "result_expected": 0.55,
        "point_margin": 7,
    },
])

elo = EloSystem()
elo.update_game(example_game)

# Synergy example with two players
model = SynergyModel(num_players=3, rank=8)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
sample = SynergySample(
    player_i=0,
    player_j=1,
    result_actual=1.0,
    result_expected=0.55,
    margin_weight=1.0,
    overlap=0.8,
)
loss = train_epoch(model, [sample], optimizer)

team = TeamInfo(team_id="A", players=["p1", "p2"], covariates={})
player_to_idx = {"p1": 0, "p2": 1}
team_rating = compute_team_rating(team, elo, model, player_to_idx)
print("Team rating", team_rating)
