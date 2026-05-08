#!/usr/bin/env python
"""Generate statistics from Barcelona match data for the final report."""

import pandas as pd

barca = pd.read_csv("data/barcelona_matches.csv")

print("BARCELONA MATCH STATISTICS")
print("=" * 50)
print(f"Total matches: {len(barca)}")
print(f'Home matches: {len(barca[barca["venue"] == "Home"])}')
print(f'Away matches: {len(barca[barca["venue"] == "Away"])}')
print()
print("RESULTS BREAKDOWN")
print("=" * 50)
wins = (barca["barca_result"] == "Win").sum()
draws = (barca["barca_result"] == "Draw").sum()
losses = (barca["barca_result"] == "Loss").sum()
print(f"Wins: {wins} ({wins / len(barca) * 100:.1f}%)")
print(f"Draws: {draws} ({draws / len(barca) * 100:.1f}%)")
print(f"Losses: {losses} ({losses / len(barca) * 100:.1f}%)")
print()
print("POSSESSION ANALYSIS")
print("=" * 50)
possession_data = barca[barca["has_possession_data"]]
print(f"Matches with possession data: {len(possession_data)}")
print(f'Avg possession: {possession_data["barca_possession"].mean():.1f}%')
high_poss_wins = len(
    possession_data[
        (possession_data["barca_possession"] > 60)
        & (possession_data["barca_result"] == "Win")
    ]
)
high_poss_losses = len(
    possession_data[
        (possession_data["barca_possession"] > 60)
        & (possession_data["barca_result"] == "Loss")
    ]
)
print(f"Wins with high possession (>60%): {high_poss_wins}")
print(f"Losses with high possession (>60%): {high_poss_losses}")
print()
print("SHOOTING STATISTICS")
print("=" * 50)
print(f'Avg shots on target: {barca["barca_shots_on"].mean():.2f}')
print(f'Avg shots off target: {barca["barca_shots_off"].mean():.2f}')
print(f'Shot accuracy: {barca["barca_shot_accuracy"].mean():.1f}%')
print(f'Avg goals per game: {barca["barca_goals"].mean():.2f}')
print()
print("SEASON BREAKDOWN")
print("=" * 50)
seasons = (
    barca.groupby("season")
    .agg(
        {
            "barca_result": lambda x: (x == "Win").sum(),
            "barca_possession": "mean",
            "barca_goals": "mean",
            "barca_shot_accuracy": "mean",
        }
    )
    .round(2)
)
seasons.columns = ["Wins", "Avg Possession %", "Avg Goals", "Shot Accuracy %"]
print(seasons.to_string())

print()
print("MOST DIFFICULT OPPONENTS")
print("=" * 50)
opponent_stats = (
    barca.groupby("opponent_name")
    .agg({"barca_goals": "mean", "barca_result": lambda x: (x == "Win").sum()})
    .round(2)
)
opponent_stats.columns = ["Avg Goals Against", "Wins"]
opponent_stats = opponent_stats.sort_values("Avg Goals Against")
print("Top 5 most difficult opponents (lowest avg goals scored):")
print(opponent_stats.head(5).to_string())

print()
print("VENUE COMPARISON")
print("=" * 50)
home = barca[barca["venue"] == "Home"]
away = barca[barca["venue"] == "Away"]
print(f'Home win rate: {(home["barca_result"] == "Win").sum() / len(home) * 100:.1f}%')
print(f'Away win rate: {(away["barca_result"] == "Win").sum() / len(away) * 100:.1f}%')
print(f'Home avg goals: {home["barca_goals"].mean():.2f}')
print(f'Away avg goals: {away["barca_goals"].mean():.2f}')
print(f'Home avg possession: {home["barca_possession"].mean():.1f}%')
print(f'Away avg possession: {away["barca_possession"].mean():.1f}%')
