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

# Barcelona Performance Story Prototype

This repository gives you a strong starting point for the Visualisation in Data Science football project. It is designed around the main issue from the peer feedback: your analyses should read like one connected story instead of four isolated tasks.

## Storyline

The proposed narrative flow is:

1. `Act 1`: challenge the assumption that possession guarantees wins.
2. `Act 2`: move from problem to response by scouting players who support the style.
3. `Act 3`: identify the opponents that consistently reduce Barcelona's attacking output.
4. `Act 4`: close with a benchmark against elite European clubs and a recommendation.

This flow gives you:

- a clear introduction
- a reason to move from one chart to the next
- a conclusion panel instead of stopping at analysis

## Project structure

- `index.html`: the narrative structure and all report-facing copy blocks
- `styles.css`: shared visual language, layout, colour palette, and responsive behaviour
- `app.js`: SVG rendering logic and lightweight interactions in vanilla JavaScript
- `data/sample-data.js`: placeholder data so the prototype works immediately
- `report/implementation-report-draft.md`: a ready-to-adapt draft for the implementation report

## Recommended design changes

### Keep, but improve

- `Task 1`: keep the possession analysis, but present it as the opening tension instead of a standalone result.
- `Task 3`: keep the heatmap, but invert the colour logic so higher values are darker and easier to interpret.
- `Task 4`: keep the benchmark scatterplot as the final view because it resolves the story well.

### Change

- `Task 2`: replace the crowded multi-line chart with direct labels and filtering. If your real player set is large, consider either:
  - a filtered line chart for selected players, or
  - a ranked table with small sparklines

## How to adapt this to your real data

1. Replace the mock arrays in `data/sample-data.js` with your real processed data.
2. Keep the same field names where possible so the rendering functions need minimal changes.
3. If your source data is in CSV format, either:
   - convert it to JSON before loading it, or
   - add a small CSV parsing helper in `app.js`
4. Save final screenshots for each visual once the real data is connected.
5. Copy the text from `report/implementation-report-draft.md` into your course report template and replace the placeholders.

## Suggested next dataset tasks

Before polishing the visuals, prepare these analysis tables:

1. Match-level table with opponent, venue, possession, result, goals for, goals against, and season.
2. Player development table with player, season, and the exact scouting metric you decide to use.
3. Opponent summary table with Barcelona goals scored by opponent and season.
4. Club benchmark table with one row per elite club and the final comparison metrics.

## Important note

The current prototype uses sample values because the dataset itself was not in the workspace yet. Once you place the real processed data in the project, we can wire it in and tune each chart to your exact variables.
