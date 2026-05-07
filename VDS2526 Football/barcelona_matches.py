from pathlib import Path
import pandas as pd

OUTPUT = Path("/Users/martaespipou/Documents/tercer de carrera/visualisation in data science/project/data")
OUTPUT.mkdir(parents=True, exist_ok=True)

#load the master matches dataset created in match_data.py
matches = pd.read_csv(OUTPUT / "master_matches.csv")

#check how Barcelona appears in the dataset
print("Home team names containing Barcelona:")
print(matches[matches["home_team_name"].str.contains("Barcelona", na=False)]["home_team_name"].unique())

barcelona_name = "FC Barcelona"

#keep only matches where Barcelona played
barcelona_matches = matches[(matches["home_team_name"] == barcelona_name) |(matches["away_team_name"] == barcelona_name)].copy()

#create Barcelona-centered columns
#create a column to indicate if the match was home or away for Barcelona
barcelona_matches["venue"] = "Away"
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name,"venue"] = "Home"

#create opponent name column
barcelona_matches["opponent_name"] = barcelona_matches["home_team_name"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_name"] = barcelona_matches["away_team_name"]

#barcelona goals in every match
barcelona_matches["barca_goals"] = barcelona_matches["away_team_goal"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_goals"] = barcelona_matches["home_team_goal"]

barcelona_matches["opponent_goals"] = barcelona_matches["home_team_goal"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_goals"] = barcelona_matches["away_team_goal"]

barcelona_matches["barca_possession"] = barcelona_matches["away_possession"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_possession"] = barcelona_matches["home_possession"]

barcelona_matches["opponent_possession"] = barcelona_matches["home_possession"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_possession"] = barcelona_matches["away_possession"]

barcelona_matches["barca_shots_on"] = barcelona_matches["away_shots_on"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_shots_on"] = barcelona_matches["home_shots_on"]

barcelona_matches["opponent_shots_on"] = barcelona_matches["home_shots_on"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_shots_on"] = barcelona_matches["away_shots_on"]

barcelona_matches["barca_shots_off"] = barcelona_matches["away_shots_off"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_shots_off"] = barcelona_matches["home_shots_off"]

barcelona_matches["opponent_shots_off"] = barcelona_matches["home_shots_off"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_shots_off"] = barcelona_matches["away_shots_off"]

barcelona_matches["barca_corners"] = barcelona_matches["away_corners"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_corners"] = barcelona_matches["home_corners"]

barcelona_matches["opponent_corners"] = barcelona_matches["home_corners"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_corners"] = barcelona_matches["away_corners"]

barcelona_matches["barca_crosses"] = barcelona_matches["away_crosses"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_crosses"] = barcelona_matches["home_crosses"]

barcelona_matches["opponent_crosses"] = barcelona_matches["home_crosses"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_crosses"] = barcelona_matches["away_crosses"]

barcelona_matches["barca_fouls"] = barcelona_matches["away_fouls"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_fouls"] = barcelona_matches["home_fouls"]

barcelona_matches["opponent_fouls"] = barcelona_matches["home_fouls"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_fouls"] = barcelona_matches["away_fouls"]

barcelona_matches["barca_yellow_cards"] = barcelona_matches["away_yellow_cards"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_yellow_cards"] = barcelona_matches["home_yellow_cards"]

barcelona_matches["opponent_yellow_cards"] = barcelona_matches["home_yellow_cards"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_yellow_cards"] = barcelona_matches["away_yellow_cards"]

barcelona_matches["barca_red_cards"] = barcelona_matches["away_red_cards"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_red_cards"] = barcelona_matches["home_red_cards"]

barcelona_matches["opponent_red_cards"] = barcelona_matches["home_red_cards"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_red_cards"] = barcelona_matches["away_red_cards"]

barcelona_matches["barca_goal_events"] = barcelona_matches["away_goal_events"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "barca_goal_events"] = barcelona_matches["home_goal_events"]

barcelona_matches["opponent_goal_events"] = barcelona_matches["home_goal_events"]
barcelona_matches.loc[barcelona_matches["home_team_name"] == barcelona_name, "opponent_goal_events"] = barcelona_matches["away_goal_events"]

# result from Barcelona perspective
barcelona_matches["barca_result"] = "Draw"
barcelona_matches.loc[barcelona_matches["barca_goals"] > barcelona_matches["opponent_goals"], "barca_result"] = "Win"
barcelona_matches.loc[barcelona_matches["barca_goals"] < barcelona_matches["opponent_goals"], "barca_result"] = "Loss"

# Barcelona-specific derived columns
barcelona_matches["barca_total_shots"] = (barcelona_matches["barca_shots_on"] + barcelona_matches["barca_shots_off"])

barcelona_matches["opponent_total_shots"] = (barcelona_matches["opponent_shots_on"] + barcelona_matches["opponent_shots_off"])

barcelona_matches["barca_goal_difference"] = (barcelona_matches["barca_goals"] - barcelona_matches["opponent_goals"])

barcelona_matches["barca_shot_accuracy"] = (barcelona_matches["barca_shots_on"] / barcelona_matches["barca_total_shots"].replace(0, pd.NA))

barcelona_matches["barca_points"] = 0
barcelona_matches.loc[barcelona_matches["barca_result"] == "Win", "barca_points"] = 3
barcelona_matches.loc[barcelona_matches["barca_result"] == "Draw", "barca_points"] = 1

# final curated Barcelona dataset
barcelona_matches_final = barcelona_matches[
    [
        "match_id",
        "season",
        "stage",
        "date",
        "country_name",
        "league_name",
        "venue",
        "opponent_name",
        "barca_goals",
        "opponent_goals",
        "barca_result",
        "barca_points",
        "barca_goal_difference",
        "barca_possession",
        "opponent_possession",
        "has_possession_data",
        "barca_shots_on",
        "opponent_shots_on",
        "barca_shots_off",
        "opponent_shots_off",
        "barca_total_shots",
        "opponent_total_shots",
        "barca_shot_accuracy",
        "barca_corners",
        "opponent_corners",
        "barca_crosses",
        "opponent_crosses",
        "barca_fouls",
        "opponent_fouls",
        "barca_yellow_cards",
        "opponent_yellow_cards",
        "barca_red_cards",
        "opponent_red_cards",
        "barca_goal_events",
        "opponent_goal_events"
    ]
].copy()

# quick checks
print("Total Barcelona matches:", len(barcelona_matches_final))
print("Barcelona matches with possession:", barcelona_matches_final["has_possession_data"].sum())
print("Barcelona matches without possession:", (~barcelona_matches_final["has_possession_data"]).sum())

print(barcelona_matches_final.head())

# save the result
barcelona_matches_final.to_csv(OUTPUT / "barcelona_matches.csv", index=False)
print("Saved barcelona_matches.csv")
