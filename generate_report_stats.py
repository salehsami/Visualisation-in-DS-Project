#!/usr/bin/env python
"""Generate statistics from Barcelona match data for the final report."""

import pandas as pd
import pandas as pd
import plotly.express as px
import os


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

os.makedirs("charts", exist_ok=True)

barca = pd.read_csv("data/barcelona_matches.csv")

season_goals = barca.groupby("season")["barca_goals"].sum().reset_index()

fig1 = px.bar(
    season_goals,
    x="season",
    y="barca_goals",
    color="barca_goals",
    color_continuous_scale="Blues",
    title="FC Barcelona: Total Goals Scored Per Season",
    labels={"season": "Season", "barca_goals": "Total Goals"}
)

fig1.update_layout(
    xaxis_title="Season",
    yaxis_title="Total Goals",
    title_font=dict(size=18, family="Arial"),
    plot_bgcolor="white",
    xaxis_tickangle=-45,
    margin=dict(t=70, b=50, l=50, r=30)
)

fig1.write_html("charts/eda_total_goals_bar.html")
print("Saved: charts/eda_total_goals_bar.html")

possession_data = barca[barca["has_possession_data"] == True].copy()

outcome_order = ["Win", "Draw", "Loss"]
outcome_colors = {"Win": "#2ecc71", "Draw": "#f1c40f", "Loss": "#e74c3c"}

fig2 = px.histogram(
    possession_data,
    x="barca_possession",
    color="barca_result",
    color_discrete_map=outcome_colors,
    barmode="stack",
    nbins=20,
    title="Distribution of Ball Possession by Match Outcome",
    labels={"barca_possession": "Ball Possession (%)", "barca_result": "Match Outcome"},
    category_orders={"barca_result": outcome_order}
)

fig2.update_traces(
    marker=dict(line=dict(width=1, color="white"))
)

fig2.update_layout(
    xaxis_title="Ball Possession (%)",
    yaxis_title="Frequency (Number of Matches)",
    title_font=dict(size=18, family="Arial"),
    plot_bgcolor="#f8f9fa",
    margin=dict(t=70, b=50, l=50, r=30)
)

fig2.write_html("charts/eda_possession_hist.html")
print("Saved: charts/eda_possession_hist.html")
