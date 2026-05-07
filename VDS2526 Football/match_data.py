#File used to create a matches dataset with information about all matches together, joining them based on the id
from pathlib import Path
from sys import displayhook
import pandas as pd
import pytest


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

#get only the last possesion of each match
possession = possession.sort_values(["match_id", "elapsed", "elapsed_plus"]).groupby("match_id").last().reset_index()
#groupby creates groups based on the same match and last takes the last row of each group
possession = possession.rename(columns={"homepos": "home_possession", "awaypos": "away_possession"})
possession = possession[["match_id", "home_possession", "away_possession"]]