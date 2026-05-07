# VDS2526 Group 3 — FC Barcelona Data Visualisation

**Students:** Usman Ahmed (2500039), Sefa Kayacan Citak (2505675), Mariona Espi Planet (2512208), Saleh Sami (2502333)

## Dataset

**The dataset is NOT included in this repository.**
Download the "Football" dataset from Blackboard -> Project folder -> Data folder
(provided by Prof. Inigo Bermejo, VDS2526 2025/2026).

It is a CSV export of the European Soccer Database covering 11 European leagues,
seasons 2008-2016. Our project analyses FC Barcelona (Spain LIGA BBVA).

Files required — place all CSVs in one folder before running:

| File | Used by |
|------|---------|
| Match.csv | Tasks 1, 3, 4 |
| Match_Possesion.csv | Tasks 1, 4 (note: one 's' in filename) |
| Team.csv | Tasks 1, 3, 4 |
| League.csv | Task 4 |
| Player.csv | Task 2 |
| Player_Attributes.csv | Task 2 |

## Setup

```bash
pip install pandas numpy matplotlib seaborn plotly
```

Python 3.9+ required.

## How to Run

```bash
# With real dataset (recommended):
python code/task1_boxplot.py     --data /path/to/csvs --out figures/
python code/task2_multiline.py   --data /path/to/csvs --out figures/
python code/task3_heatmap.py     --data /path/to/csvs --out figures/
python code/task4_scatterplot.py --data /path/to/csvs --out figures/

# Without dataset (uses realistic simulated data to test the scripts):
python code/task1_boxplot.py     --out figures/
python code/task2_multiline.py   --out figures/
python code/task3_heatmap.py     --out figures/
python code/task4_scatterplot.py --out figures/
```

Each script outputs both an interactive .html and a static .png.

## Key Column Mappings

### Match.csv
- id = match identifier (= match_id in Match_Possesion etc.)
- home_team_api_id / away_team_api_id -> Team.team_api_id
- home_team_goal / away_team_goal = full-time goals
- season = "2008/2009" format

### Match_Possesion.csv
- match_id -> Match.id
- homepos = home possession % at this timestamp
- awaypos = away possession % at this timestamp
- elapsed = minute (script uses max per match_id for final reading)

### Player_Attributes.csv
- player_api_id -> Player.player_api_id
- short_passing, vision = 0-100 FIFA attribute scores

## Interactions (HTML versions)
| Task | Interaction |
|------|-------------|
| 1 Boxplot | Hover any match point -> opponent, date, season |
| 2 Multi-line | Click legend -> highlight/hide one player |
| 3 Heatmap | Hover any cell -> opponent, season, avg goals |
| 4 Scatterplot | Hover -> full team stats; click league name to filter |

## Project Structure
```
barca_viz/
├── code/
│   ├── task1_boxplot.py       # Task 1: Tactical Reality Check
│   ├── task2_multiline.py     # Task 2: Scouting for Hidden Gems
│   ├── task3_heatmap.py       # Task 3: Identifying Kryptonite
│   └── task4_scatterplot.py   # Task 4: Comparative Benchmarking
├── figures/                   # generated PNGs + HTMLs go here
├── generate_figures.py        # generate all static PNGs at once (simulated data)
└── README.md
```
