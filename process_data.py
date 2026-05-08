"""
Master data processing script to create master_matches.csv and barcelona_matches.csv
from the raw VDS2526 Football dataset.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Define paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA = BASE_DIR / "VDS2526 Football"
OUTPUT = BASE_DIR / "data"
OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("STEP 1: Loading raw data files...")
print("=" * 60)

# Load all data files
match = pd.read_csv(RAW_DATA / "Match.csv")
country = pd.read_csv(RAW_DATA / "Country.csv")
league = pd.read_csv(RAW_DATA / "League.csv")
team = pd.read_csv(RAW_DATA / "Team.csv")
possession = pd.read_csv(RAW_DATA / "Match_Possesion.csv")
goals = pd.read_csv(RAW_DATA / "Match_Goals.csv")
shots_on = pd.read_csv(RAW_DATA / "Match_Shots_On.csv")
shots_off = pd.read_csv(RAW_DATA / "Match_Shots_Off.csv")
corners = pd.read_csv(RAW_DATA / "Match_Corner.csv")
crosses = pd.read_csv(RAW_DATA / "Match_Cross.csv")
fouls = pd.read_csv(RAW_DATA / "Match_Fouls_Committed.csv")
cards = pd.read_csv(RAW_DATA / "Match_Cards.csv")

print(f"✓ Loaded Match.csv ({len(match)} records)")
print(f"✓ Loaded Country.csv ({len(country)} countries)")
print(f"✓ Loaded League.csv ({len(league)} leagues)")
print(f"✓ Loaded Team.csv ({len(team)} teams)")

print("\n" + "=" * 60)
print("STEP 2: Building base matches dataset...")
print("=" * 60)

# Create base matches dataset
matches = match[
    [
        "id",
        "country_id",
        "league_id",
        "season",
        "stage",
        "date",
        "home_team_api_id",
        "away_team_api_id",
        "home_team_goal",
        "away_team_goal",
    ]
].copy()

matches = matches.rename(columns={"id": "match_id"})

# Add country names
country = country.rename(columns={"id": "country_id", "name": "country_name"})
matches = matches.merge(country, on="country_id", how="left")

# Add league names
league = league.rename(columns={"id": "league_id", "name": "league_name"})
matches = matches.merge(league, on="league_id", how="left")

# Add home team names
home_team = team.rename(
    columns={
        "team_api_id": "home_team_api_id",
        "team_long_name": "home_team_name",
        "team_short_name": "home_team_short_name",
    }
)
matches = matches.merge(
    home_team[["home_team_api_id", "home_team_name", "home_team_short_name"]],
    on="home_team_api_id",
    how="left",
)

# Add away team names
away_team = team.rename(
    columns={
        "team_api_id": "away_team_api_id",
        "team_long_name": "away_team_name",
        "team_short_name": "away_team_short_name",
    }
)
matches = matches.merge(
    away_team[["away_team_api_id", "away_team_name", "away_team_short_name"]],
    on="away_team_api_id",
    how="left",
)

print(f"✓ Base dataset: {len(matches)} matches")

print("\n" + "=" * 60)
print("STEP 3: Adding possession data...")
print("=" * 60)

# Process possession data
possession["elapsed"] = pd.to_numeric(possession["elapsed"], errors="coerce")
possession["elapsed_plus"] = pd.to_numeric(
    possession["elapsed_plus"], errors="coerce"
).fillna(0)

# Get last possession reading for each match
possession = (
    possession.sort_values(["match_id", "elapsed", "elapsed_plus"])
    .groupby("match_id")
    .last()
    .reset_index()
)
possession = possession.rename(
    columns={"homepos": "home_possession", "awaypos": "away_possession"}
)
possession = possession[["match_id", "home_possession", "away_possession"]]

matches = matches.merge(possession, on="match_id", how="left")
matches["home_possession"] = pd.to_numeric(matches["home_possession"], errors="coerce")
matches["away_possession"] = pd.to_numeric(matches["away_possession"], errors="coerce")
matches["has_possession_data"] = (
    matches["home_possession"].notna() & matches["away_possession"].notna()
)

print(f"✓ Possession data added ({matches['has_possession_data'].sum()} with data)")

print("\n" + "=" * 60)
print("STEP 4: Adding shots data...")
print("=" * 60)

# Shots on target
shots_on_grouped = (
    shots_on.groupby(["match_id", "team"]).size().reset_index(name="shots_on")
)
shots_on_merged = shots_on_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_shots_on = shots_on_merged[
    shots_on_merged["team"] == shots_on_merged["home_team_api_id"]
][["match_id", "shots_on"]].rename(columns={"shots_on": "home_shots_on"})
away_shots_on = shots_on_merged[
    shots_on_merged["team"] == shots_on_merged["away_team_api_id"]
][["match_id", "shots_on"]].rename(columns={"shots_on": "away_shots_on"})

matches = matches.merge(home_shots_on, on="match_id", how="left")
matches = matches.merge(away_shots_on, on="match_id", how="left")
matches["home_shots_on"] = matches["home_shots_on"].fillna(0).astype(int)
matches["away_shots_on"] = matches["away_shots_on"].fillna(0).astype(int)

# Shots off target
shots_off_grouped = (
    shots_off.groupby(["match_id", "team"]).size().reset_index(name="shots_off")
)
shots_off_merged = shots_off_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_shots_off = shots_off_merged[
    shots_off_merged["team"] == shots_off_merged["home_team_api_id"]
][["match_id", "shots_off"]].rename(columns={"shots_off": "home_shots_off"})
away_shots_off = shots_off_merged[
    shots_off_merged["team"] == shots_off_merged["away_team_api_id"]
][["match_id", "shots_off"]].rename(columns={"shots_off": "away_shots_off"})

matches = matches.merge(home_shots_off, on="match_id", how="left")
matches = matches.merge(away_shots_off, on="match_id", how="left")
matches["home_shots_off"] = matches["home_shots_off"].fillna(0).astype(int)
matches["away_shots_off"] = matches["away_shots_off"].fillna(0).astype(int)

print(f"✓ Shots data added (on target + off target)")

print("\n" + "=" * 60)
print("STEP 5: Adding corners...")
print("=" * 60)

corners_grouped = (
    corners.groupby(["match_id", "team"]).size().reset_index(name="corners")
)
corners_merged = corners_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_corners = corners_merged[
    corners_merged["team"] == corners_merged["home_team_api_id"]
][["match_id", "corners"]].rename(columns={"corners": "home_corners"})
away_corners = corners_merged[
    corners_merged["team"] == corners_merged["away_team_api_id"]
][["match_id", "corners"]].rename(columns={"corners": "away_corners"})

matches = matches.merge(home_corners, on="match_id", how="left")
matches = matches.merge(away_corners, on="match_id", how="left")
matches["home_corners"] = matches["home_corners"].fillna(0).astype(int)
matches["away_corners"] = matches["away_corners"].fillna(0).astype(int)

print(f"✓ Corners data added")

print("\n" + "=" * 60)
print("STEP 6: Adding crosses...")
print("=" * 60)

crosses_grouped = (
    crosses.groupby(["match_id", "team"]).size().reset_index(name="crosses")
)
crosses_merged = crosses_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_crosses = crosses_merged[
    crosses_merged["team"] == crosses_merged["home_team_api_id"]
][["match_id", "crosses"]].rename(columns={"crosses": "home_crosses"})
away_crosses = crosses_merged[
    crosses_merged["team"] == crosses_merged["away_team_api_id"]
][["match_id", "crosses"]].rename(columns={"crosses": "away_crosses"})

matches = matches.merge(home_crosses, on="match_id", how="left")
matches = matches.merge(away_crosses, on="match_id", how="left")
matches["home_crosses"] = matches["home_crosses"].fillna(0).astype(int)
matches["away_crosses"] = matches["away_crosses"].fillna(0).astype(int)

print(f"✓ Crosses data added")

print("\n" + "=" * 60)
print("STEP 7: Adding fouls...")
print("=" * 60)

fouls_grouped = fouls.groupby(["match_id", "team"]).size().reset_index(name="fouls")
fouls_merged = fouls_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_fouls = fouls_merged[fouls_merged["team"] == fouls_merged["home_team_api_id"]][
    ["match_id", "fouls"]
].rename(columns={"fouls": "home_fouls"})
away_fouls = fouls_merged[fouls_merged["team"] == fouls_merged["away_team_api_id"]][
    ["match_id", "fouls"]
].rename(columns={"fouls": "away_fouls"})

matches = matches.merge(home_fouls, on="match_id", how="left")
matches = matches.merge(away_fouls, on="match_id", how="left")
matches["home_fouls"] = matches["home_fouls"].fillna(0).astype(int)
matches["away_fouls"] = matches["away_fouls"].fillna(0).astype(int)

print(f"✓ Fouls data added")

print("\n" + "=" * 60)
print("STEP 8: Adding cards (yellow & red)...")
print("=" * 60)

yellow_cards_grouped = (
    cards[cards["card_type"] == "y"]
    .groupby(["match_id", "team"])
    .size()
    .reset_index(name="yellow_cards")
)
red_cards_grouped = (
    cards[cards["card_type"] == "r"]
    .groupby(["match_id", "team"])
    .size()
    .reset_index(name="red_cards")
)

yellow_merged = yellow_cards_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_yellow = yellow_merged[yellow_merged["team"] == yellow_merged["home_team_api_id"]][
    ["match_id", "yellow_cards"]
].rename(columns={"yellow_cards": "home_yellow_cards"})
away_yellow = yellow_merged[yellow_merged["team"] == yellow_merged["away_team_api_id"]][
    ["match_id", "yellow_cards"]
].rename(columns={"yellow_cards": "away_yellow_cards"})

red_merged = red_cards_grouped.merge(
    matches[["match_id", "home_team_api_id", "away_team_api_id"]],
    on="match_id",
    how="left",
)
home_red = red_merged[red_merged["team"] == red_merged["home_team_api_id"]][
    ["match_id", "red_cards"]
].rename(columns={"red_cards": "home_red_cards"})
away_red = red_merged[red_merged["team"] == red_merged["away_team_api_id"]][
    ["match_id", "red_cards"]
].rename(columns={"red_cards": "away_red_cards"})

matches = matches.merge(home_yellow, on="match_id", how="left")
matches = matches.merge(away_yellow, on="match_id", how="left")
matches = matches.merge(home_red, on="match_id", how="left")
matches = matches.merge(away_red, on="match_id", how="left")

matches["home_yellow_cards"] = matches["home_yellow_cards"].fillna(0).astype(int)
matches["away_yellow_cards"] = matches["away_yellow_cards"].fillna(0).astype(int)
matches["home_red_cards"] = matches["home_red_cards"].fillna(0).astype(int)
matches["away_red_cards"] = matches["away_red_cards"].fillna(0).astype(int)

print(f"✓ Cards data added")

print("\n" + "=" * 60)
print("STEP 9: Adding match results...")
print("=" * 60)

matches["goal_difference"] = matches["home_team_goal"] - matches["away_team_goal"]
matches["total_goals"] = matches["home_team_goal"] + matches["away_team_goal"]
matches["match_result"] = "Draw"
matches.loc[matches["home_team_goal"] > matches["away_team_goal"], "match_result"] = (
    "Home Win"
)
matches.loc[matches["home_team_goal"] < matches["away_team_goal"], "match_result"] = (
    "Away Win"
)

print(f"✓ Match results calculated")

# Save master matches dataset
master_path = OUTPUT / "master_matches.csv"
matches.to_csv(master_path, index=False)
print(f"\n✓ Saved master_matches.csv ({len(matches)} matches)")

print("\n" + "=" * 60)
print("STEP 10: Extracting Barcelona matches...")
print("=" * 60)

# Extract Barcelona matches
barcelona_name = "FC Barcelona"
barcelona_matches = matches[
    (matches["home_team_name"] == barcelona_name)
    | (matches["away_team_name"] == barcelona_name)
].copy()

print(f"Found {len(barcelona_matches)} Barcelona matches")

# Add Barcelona-centric columns
barcelona_matches["venue"] = "Away"
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "venue"
] = "Home"

barcelona_matches["opponent_name"] = barcelona_matches["home_team_name"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_name"
] = barcelona_matches["away_team_name"]

barcelona_matches["barca_goals"] = barcelona_matches["away_team_goal"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_goals"
] = barcelona_matches["home_team_goal"]

barcelona_matches["opponent_goals"] = barcelona_matches["home_team_goal"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_goals"
] = barcelona_matches["away_team_goal"]

barcelona_matches["barca_possession"] = barcelona_matches["away_possession"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_possession"
] = barcelona_matches["home_possession"]

barcelona_matches["opponent_possession"] = barcelona_matches["home_possession"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_possession"
] = barcelona_matches["away_possession"]

barcelona_matches["barca_shots_on"] = barcelona_matches["away_shots_on"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_shots_on"
] = barcelona_matches["home_shots_on"]

barcelona_matches["opponent_shots_on"] = barcelona_matches["home_shots_on"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_shots_on"
] = barcelona_matches["away_shots_on"]

barcelona_matches["barca_shots_off"] = barcelona_matches["away_shots_off"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_shots_off"
] = barcelona_matches["home_shots_off"]

barcelona_matches["opponent_shots_off"] = barcelona_matches["home_shots_off"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_shots_off"
] = barcelona_matches["away_shots_off"]

barcelona_matches["barca_corners"] = barcelona_matches["away_corners"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_corners"
] = barcelona_matches["home_corners"]

barcelona_matches["opponent_corners"] = barcelona_matches["home_corners"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_corners"
] = barcelona_matches["away_corners"]

barcelona_matches["barca_crosses"] = barcelona_matches["away_crosses"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_crosses"
] = barcelona_matches["home_crosses"]

barcelona_matches["opponent_crosses"] = barcelona_matches["home_crosses"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_crosses"
] = barcelona_matches["away_crosses"]

barcelona_matches["barca_fouls"] = barcelona_matches["away_fouls"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_fouls"
] = barcelona_matches["home_fouls"]

barcelona_matches["opponent_fouls"] = barcelona_matches["home_fouls"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_fouls"
] = barcelona_matches["away_fouls"]

barcelona_matches["barca_yellow_cards"] = barcelona_matches["away_yellow_cards"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_yellow_cards"
] = barcelona_matches["home_yellow_cards"]

barcelona_matches["opponent_yellow_cards"] = barcelona_matches["home_yellow_cards"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_yellow_cards"
] = barcelona_matches["away_yellow_cards"]

barcelona_matches["barca_red_cards"] = barcelona_matches["away_red_cards"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "barca_red_cards"
] = barcelona_matches["home_red_cards"]

barcelona_matches["opponent_red_cards"] = barcelona_matches["home_red_cards"]
barcelona_matches.loc[
    barcelona_matches["home_team_name"] == barcelona_name, "opponent_red_cards"
] = barcelona_matches["away_red_cards"]

# Result from Barcelona perspective
barcelona_matches["barca_result"] = "Draw"
barcelona_matches.loc[
    barcelona_matches["barca_goals"] > barcelona_matches["opponent_goals"],
    "barca_result",
] = "Win"
barcelona_matches.loc[
    barcelona_matches["barca_goals"] < barcelona_matches["opponent_goals"],
    "barca_result",
] = "Loss"

# Derived metrics
barcelona_matches["barca_total_shots"] = (
    barcelona_matches["barca_shots_on"] + barcelona_matches["barca_shots_off"]
)
barcelona_matches["opponent_total_shots"] = (
    barcelona_matches["opponent_shots_on"] + barcelona_matches["opponent_shots_off"]
)
barcelona_matches["barca_goal_difference"] = (
    barcelona_matches["barca_goals"] - barcelona_matches["opponent_goals"]
)

# Shot accuracy
barcelona_matches["barca_shot_accuracy"] = (
    barcelona_matches["barca_shots_on"] / barcelona_matches["barca_total_shots"]
).fillna(0) * 100

# Points (3 for win, 1 for draw, 0 for loss)
barcelona_matches["barca_points"] = 0
barcelona_matches.loc[barcelona_matches["barca_result"] == "Win", "barca_points"] = 3
barcelona_matches.loc[barcelona_matches["barca_result"] == "Draw", "barca_points"] = 1

# Save Barcelona matches
barca_path = OUTPUT / "barcelona_matches.csv"
barcelona_matches.to_csv(barca_path, index=False)
print(f"✓ Saved barcelona_matches.csv")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total matches processed: {len(matches)}")
print(f"Barcelona matches: {len(barcelona_matches)}")
print(
    f"Barcelona home wins: {(barcelona_matches[barcelona_matches['venue'] == 'Home']['barca_result'] == 'Win').sum()}"
)
print(
    f"Barcelona away wins: {(barcelona_matches[barcelona_matches['venue'] == 'Away']['barca_result'] == 'Win').sum()}"
)
print(
    f"Barcelona wins with possession data: {barcelona_matches[barcelona_matches['has_possession_data'] & (barcelona_matches['barca_result'] == 'Win')].shape[0]}"
)
print(f"\nFiles saved to: {OUTPUT}")
print("=" * 60)
