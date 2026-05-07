# VDS2526 Group 3 — FC Barcelona Data Visualisation

**Students:** Usman Ahmed (2500039), Sefa Kayacan Citak (2505675), Mariona Espi Planet (2512208), Saleh Sami (2502333)

## Dataset

Professor-provided CSV export of the European Soccer Database (2008–2016).

Files required (place all in one folder):
| File | Used by |
|------|---------|
| Match.csv | Tasks 1, 3, 4 |
| Match_Possesion.csv | Tasks 1, 4 (note: one 's') |
| Team.csv | Tasks 1, 3, 4 |
| League.csv | Task 4 |
| Player.csv | Task 2 |
| Player_Attributes.csv | Task 2 |

## Setup

```bash
pip install pandas numpy matplotlib seaborn plotly
```

## How to Run

```bash
# With real dataset:
python code/task1_boxplot.py     --data /path/to/csvs --out figures/
python code/task2_multiline.py   --data /path/to/csvs --out figures/
python code/task3_heatmap.py     --data /path/to/csvs --out figures/
python code/task4_scatterplot.py --data /path/to/csvs --out figures/

# Without dataset (realistic simulated data):
python generate_figures.py
```

Each script outputs both an interactive .html and a static .png.

## Key Column Mappings

### Match.csv
- id = match identifier (= match_id in Match_Possesion etc.)
- home_team_api_id / away_team_api_id -> Team.team_api_id
- home_team_goal / away_team_goal = full-time goals
- season = "2008/2009" format
- league_id -> League.id

### Match_Possesion.csv
- match_id -> Match.id
- homepos = home possession % at this timestamp
- awaypos = away possession % at this timestamp
- elapsed = minute (use max per match_id for final reading)

### Player_Attributes.csv
- player_api_id -> Player.player_api_id
- date = FIFA snapshot date
- short_passing, vision = 0-100 scores

## Interactions (HTML versions)
| Task | Interaction |
|------|-------------|
| 1 Boxplot | Hover point -> opponent, date, season |
| 2 Multi-line | Click legend -> highlight player |
| 3 Heatmap | Hover cell -> opponent, season, goals |
| 4 Scatterplot | Hover -> full team stats; click league to filter |
