#File used to create a matches dataset with information about all matches together, joining them based on the id
from pathlib import Path
from sys import displayhook
import pandas as pd

#define our folder paths and read in the data
BASE = Path("/Users/martaespipou/Documents/tercer de carrera/visualisation in data science/project/VDS2526 Football")
OUTPUT = Path("/Users/martaespipou/Documents/tercer de carrera/visualisation in data science/project/data")
OUTPUT.mkdir(parents=True, exist_ok=True)

#load all data files to create the matches dataset
match = pd.read_csv(BASE / "Match.csv")

#need these since match does not store readable names for the teams, leagues and countries, only their ids
country = pd.read_csv(BASE / "Country.csv")
league = pd.read_csv(BASE / "League.csv")
team = pd.read_csv(BASE / "Team.csv")

possession = pd.read_csv(BASE / "Match_Possesion.csv")
goals = pd.read_csv(BASE / "Match_Goals.csv")
shots_on = pd.read_csv(BASE / "Match_Shots_On.csv")
shots_off = pd.read_csv(BASE / "Match_Shots_Off.csv")
corners = pd.read_csv(BASE / "Match_Corner.csv")
crosses = pd.read_csv(BASE / "Match_Cross.csv")
fouls = pd.read_csv(BASE / "Match_Fouls_Committed.csv")
cards = pd.read_csv(BASE / "Match_Cards.csv")

#columns we want to keep from the match dataset
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
        "away_team_goal"
    ]
].copy()

matches = matches.rename(columns={"id": "match_id"})

#rename the columns in the country dataset to be able to merge it with the matches dataset
country = country.rename(columns={"id": "country_id", "name": "country_name"})

#merge the matches dataset with the country dataset to get the country names instead of just the ids
matches = matches.merge(country, on="country_id", how="left")

league = league.rename(columns={"id": "league_id", "country_id": "country_id", "name": "league_name"})

#merge the matches dataset with the league dataset to get the league names instead of just the ids
matches = matches.merge(league, on="league_id", how="left")

home_team = team.rename(columns={
    "team_api_id": "home_team_api_id",
    "team_long_name": "home_team_name",
    "team_short_name": "home_team_short_name"
})

#merge the matches dataset with the team dataset to get the home team names instead of just the ids
matches = matches.merge(home_team, on="home_team_api_id", how="left")

away_team = team.rename(columns={
    "team_api_id": "away_team_api_id",
    "team_long_name": "away_team_name",
    "team_short_name": "away_team_short_name"
}) 

#merge the matches dataset with the team dataset to get the away team names instead of just the ids
matches = matches.merge(away_team, on="away_team_api_id", how="left")

#we'll add some results columns to the dataset to be able to make our visualisations
matches["goal_difference"] = matches["home_team_goal"] - matches["away_team_goal"]
matches["total_goals"] = matches["home_team_goal"] + matches["away_team_goal"]
matches["match_result"] = "Draw"
matches.loc[matches["home_team_goal"] > matches["away_team_goal"], "match_result"] = "Home Win"
matches.loc[matches["home_team_goal"] < matches["away_team_goal"], "match_result"] = "Away Win"

print(
    matches[
        [
            "match_id",
            "home_team_name",
            "away_team_name",
            "home_team_goal",
            "away_team_goal",
            "match_result"
        ]
    ].head()
)

#checks to see if everything is correct and if there are any missing values in the dataset
print("Number of rows:", len(matches))
print("Unique match IDs:", matches["match_id"].nunique())
print("Missing home team names:", matches["home_team_name"].isna().sum())
print("Missing away team names:", matches["away_team_name"].isna().sum())
print("Missing league names:", matches["league_name"].isna().sum())
print("Missing country names:", matches["country_name"].isna().sum())

# clean possession time columns before sorting
possession["elapsed"] = pd.to_numeric(possession["elapsed"], errors="coerce")
possession["elapsed_plus"] = pd.to_numeric(possession["elapsed_plus"], errors="coerce").fillna(0)

#get only the last possesion of each match
possession = possession.sort_values(["match_id", "elapsed", "elapsed_plus"]).groupby("match_id").last().reset_index()
#groupby creates groups based on the same match and last takes the last row of each group
possession = possession.rename(columns={"homepos": "home_possession", "awaypos": "away_possession"})
possession = possession[["match_id", "home_possession", "away_possession"]]

#merge the matches dataset with the possession dataset to get the possession information for each match
matches = matches.merge(possession, on="match_id", how="left")

# convert possession columns to numeric and keep missing values as missing
matches["home_possession"] = pd.to_numeric(matches["home_possession"], errors="coerce")
matches["away_possession"] = pd.to_numeric(matches["away_possession"], errors="coerce")
matches["has_possession_data"] = (matches["home_possession"].notna() & matches["away_possession"].notna())

#both rows should be equal
print("Number of rows after possession merge:", len(matches))
print("Unique match IDs after possession merge:", matches["match_id"].nunique())

shots_on = shots_on.groupby(["match_id", "team"]).size().reset_index(name="shots_on")

#split into home and away shots
shots_on_with_side = shots_on.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_shots_on = (shots_on_with_side[shots_on_with_side["team"] == shots_on_with_side["home_team_api_id"]][["match_id", "shots_on"]].rename(columns={"shots_on": "home_shots_on"}))
away_shots_on = (shots_on_with_side[shots_on_with_side["team"] == shots_on_with_side["away_team_api_id"]][["match_id", "shots_on"]].rename(columns={"shots_on": "away_shots_on"}))


matches = matches.merge(home_shots_on, on="match_id", how="left")
matches = matches.merge(away_shots_on, on="match_id", how="left")
matches["home_shots_on"] = matches["home_shots_on"].fillna(0)
matches["away_shots_on"] = matches["away_shots_on"].fillna(0)

#check everything is correct
print("Number of rows after shots-on merge:", len(matches))
print("Unique match IDs after shots-on merge:", matches["match_id"].nunique())

#shots off target
shots_off = shots_off.groupby(["match_id", "team"]).size().reset_index(name="shots_off")
shots_off_with_side = shots_off.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_shots_off = (shots_off_with_side[shots_off_with_side["team"] == shots_off_with_side["home_team_api_id"]][["match_id", "shots_off"]].rename(columns={"shots_off": "home_shots_off"}))
away_shots_off = (shots_off_with_side[shots_off_with_side["team"] == shots_off_with_side["away_team_api_id"]][["match_id", "shots_off"]].rename(columns={"shots_off": "away_shots_off"}))

matches = matches.merge(home_shots_off, on="match_id", how="left")
matches = matches.merge(away_shots_off, on="match_id", how="left")

#replace missing values with 0
matches["home_shots_off"] = matches["home_shots_off"].fillna(0)
matches["away_shots_off"] = matches["away_shots_off"].fillna(0)

#corners
corners = corners.groupby(["match_id", "team"]).size().reset_index(name="corners")
corners_with_side = corners.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_corners = (corners_with_side[corners_with_side["team"] == corners_with_side["home_team_api_id"]][["match_id", "corners"]].rename(columns={"corners": "home_corners"}))
away_corners = (corners_with_side[corners_with_side["team"] == corners_with_side["away_team_api_id"]][["match_id", "corners"]].rename(columns={"corners": "away_corners"}))

matches = matches.merge(home_corners, on="match_id", how="left")
matches = matches.merge(away_corners, on="match_id", how="left")

matches["home_corners"] = matches["home_corners"].fillna(0)
matches["away_corners"] = matches["away_corners"].fillna(0)

#crosses
crosses = crosses.groupby(["match_id", "team"]).size().reset_index(name="crosses")
crosses_with_side = crosses.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_crosses = (crosses_with_side[crosses_with_side["team"] == crosses_with_side["home_team_api_id"]][["match_id", "crosses"]].rename(columns={"crosses": "home_crosses"}))
away_crosses = (crosses_with_side[crosses_with_side["team"] == crosses_with_side["away_team_api_id"]][["match_id", "crosses"]].rename(columns={"crosses": "away_crosses"})) 

matches = matches.merge(home_crosses, on="match_id", how="left")
matches = matches.merge(away_crosses, on="match_id", how="left")

matches["home_crosses"] = matches["home_crosses"].fillna(0)
matches["away_crosses"] = matches["away_crosses"].fillna(0)

#fouls
fouls = fouls.groupby(["match_id", "team"]).size().reset_index(name="fouls")
fouls_with_side = fouls.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_fouls = (fouls_with_side[fouls_with_side["team"] == fouls_with_side["home_team_api_id"]][["match_id", "fouls"]].rename(columns={"fouls": "home_fouls"}))
away_fouls = (fouls_with_side[fouls_with_side["team"] == fouls_with_side["away_team_api_id"]][["match_id", "fouls"]].rename(columns={"fouls": "away_fouls"}))

matches = matches.merge(home_fouls, on="match_id", how="left")
matches = matches.merge(away_fouls, on="match_id", how="left")

matches["home_fouls"] = matches["home_fouls"].fillna(0)
matches["away_fouls"] = matches["away_fouls"].fillna(0)                     

#cards
yellow_cards = cards[cards["card_type"] == "y"].groupby(["match_id", "team"]).size().reset_index(name="yellow_cards")
red_cards = cards[cards["card_type"] == "r"].groupby(["match_id", "team"]).size().reset_index(name="red_cards")
yellow_cards_with_side = yellow_cards.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_yellow_cards = (yellow_cards_with_side[yellow_cards_with_side["team"] == yellow_cards_with_side["home_team_api_id"]][["match_id", "yellow_cards"]].rename(columns={"yellow_cards": "home_yellow_cards"}))
away_yellow_cards = (yellow_cards_with_side[yellow_cards_with_side["team"] == yellow_cards_with_side["away_team_api_id"]][["match_id", "yellow_cards"]].rename(columns={"yellow_cards": "away_yellow_cards"})) 

red_cards_with_side = red_cards.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_red_cards = (red_cards_with_side[red_cards_with_side["team"] == red_cards_with_side["home_team_api_id"]][["match_id", "red_cards"]].rename(columns={"red_cards": "home_red_cards"}))
away_red_cards = (red_cards_with_side[red_cards_with_side["team"] == red_cards_with_side["away_team_api_id"]][["match_id", "red_cards"]].rename(columns={"red_cards": "away_red_cards"}))

matches = matches.merge(home_yellow_cards, on="match_id", how="left")
matches = matches.merge(away_yellow_cards, on="match_id", how="left")
matches = matches.merge(home_red_cards, on="match_id", how="left")
matches = matches.merge(away_red_cards, on="match_id", how="left")

matches["home_yellow_cards"] = matches["home_yellow_cards"].fillna(0)
matches["away_yellow_cards"] = matches["away_yellow_cards"].fillna(0)
matches["home_red_cards"] = matches["home_red_cards"].fillna(0)
matches["away_red_cards"] = matches["away_red_cards"].fillna(0)

#goal events
goals = goals.groupby(["match_id", "team"]).size().reset_index(name="goal_events")
goals_with_side = goals.merge(matches[["match_id", "home_team_api_id", "away_team_api_id"]], on="match_id", how="left")
home_goal_events = (goals_with_side[goals_with_side["team"] == goals_with_side["home_team_api_id"]][["match_id", "goal_events"]].rename(columns={"goal_events": "home_goal_events"}))
away_goal_events = (goals_with_side[goals_with_side["team"] == goals_with_side["away_team_api_id"]][["match_id", "goal_events"]].rename(columns={"goal_events": "away_goal_events"}))

matches = matches.merge(home_goal_events, on="match_id", how="left")
matches = matches.merge(away_goal_events, on="match_id", how="left")

matches["home_goal_events"] = matches["home_goal_events"].fillna(0)
matches["away_goal_events"] = matches["away_goal_events"].fillna(0)

#derived columns for our visualisations
matches["home_total_shots"] = matches["home_shots_on"] + matches["home_shots_off"]
matches["away_total_shots"] = matches["away_shots_on"] + matches["away_shots_off"]

matches["possession_diff"] = pd.to_numeric(matches["home_possession"], errors="coerce") - pd.to_numeric(matches["away_possession"], errors="coerce")
matches["shots_on_diff"] = matches["home_shots_on"] - matches["away_shots_on"]
matches["total_shots_diff"] = matches["home_total_shots"] - matches["away_total_shots"]
matches["corners_diff"] = matches["home_corners"] - matches["away_corners"]
matches["fouls_diff"] = matches["home_fouls"] - matches["away_fouls"]

#quality check to see if there are any missing values in the dataset after all the merges
print("Final number of rows:", len(matches))
print("Final unique match IDs:", matches["match_id"].nunique())
print("Missing home possession:", matches["home_possession"].isna().sum())
print("Missing away possession:", matches["away_possession"].isna().sum())
print("Missing home shots on:", matches["home_shots_on"].isna().sum())
print("Missing away shots on:", matches["away_shots_on"].isna().sum())
print("Missing home shots off:", matches["home_shots_off"].isna().sum())
print("Missing away shots off:", matches["away_shots_off"].isna().sum())


print("Total matches in master table:", matches["match_id"].nunique())
print("Total matches in possession table:", possession["match_id"].nunique())
print("Matches with possession after merge:", matches["home_possession"].notna().sum())

matches.to_csv(OUTPUT / "master_matches.csv", index=False)
print("Saved master_matches.csv")