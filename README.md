# VDS2526 Group 3 — FC Barcelona Data Visualisation

**Students:** Usman Ahmed (2500039), Sefa Kayacan Citak (2505675), Mariona Espi Planet (2512208), Saleh Sami (2502333)  
**Dataset:** European Soccer Database (2008–2016) | FC Barcelona | 304 matches

---

## What this project is

We built a four-part interactive data story around FC Barcelona's performance across the 2008–2016 La Liga seasons. The starting question was simple: does dominating possession actually translate into wins? From there, we followed that thread through seasonal efficiency trends, the handful of opponents who consistently gave Barcelona trouble, and finally a comparison against other top clubs in Europe.

The four acts answer:

1. Does high possession reliably translate into wins?
2. How consistently does that control become goals and shots on target?
3. Which opponents suppressed Barcelona's attack the most?
4. Where does Barcelona sit relative to Europe's elite clubs?

---

## Running the project

### Requirements

- Python 3.8 or later
- pip

### Steps

```bash
# Install dependencies
pip install pandas plotly numpy

# Place the raw CSV files from Blackboard into: VDS2526 Football/

# Build the processed datasets
python process_data.py

# Generate the four interactive charts
python build_visualizations.py

# Launch a local server
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

---

## Project structure

```
Visualisation-in-DS-Project/
├── index.html                          # Main page with narrative
├── app.js                              # Interactivity
├── styles.css                          # Layout and styling
│
├── process_data.py                     # Converts raw CSVs to analysis-ready datasets
├── build_visualizations.py             # Generates the four Plotly charts
├── generate_report_stats.py            # Pulls summary statistics for the report
│
├── data/
│   ├── master_matches.csv              # 25,979 matches across all leagues
│   └── barcelona_matches.csv           # 304 Barcelona matches with derived metrics
│
├── charts/
│   ├── act1_possession_vs_result.html  # Possession scatter by result and venue
│   ├── act2_hidden gems.html           # Season-by-season shot and goal trends
│   ├── act3_kryptonite_heatmap.html    # Goal output against difficult opponents
│   └── act4_european_benchmark.html    # Benchmarking against elite European clubs
│
├── VDS2526 Football/                   # Raw source files from Blackboard
│   ├── Match.csv
│   ├── Match_Possesion.csv
│   ├── Match_Shots_On.csv
│   ├── Match_Shots_Off.csv
│   ├── Match_Corner.csv
│   ├── Match_Cross.csv
│   ├── Match_Fouls_Committed.csv
│   ├── Match_Cards.csv
│   ├── Team.csv
│   ├── Teams_Datavs.csv
│   ├── League.csv
│   ├── Country.csv
│   └── (other supporting files)
│
└── report/
    └── implementation-report-draft.md
```

---

## Data pipeline

The raw dataset covers 25,979 European football matches across 11 leagues from the 2008/2009 to 2015/2016 seasons. It includes match results, possession percentages, shot counts (on and off target), corners, crosses, fouls, cards, and team/player metadata.

`process_data.py` merges the relevant CSVs and creates two output files. `master_matches.csv` keeps all 25,979 matches with computed columns. `barcelona_matches.csv` narrows to Barcelona's 304 matches and adds derived fields like result label, venue, shot accuracy, and points.

`build_visualizations.py` reads those two files and writes four standalone HTML charts using Plotly. The charts can be opened directly in a browser or served via the local server for the full narrative page.

---

## Barcelona at a glance (2008–2016)

| Metric              | Value            |
| ------------------- | ---------------- |
| Total matches       | 304              |
| Win rate            | 77.0% (234 wins) |
| Draw rate           | 14.1% (43 draws) |
| Loss rate           | 8.9% (27 losses) |
| Average possession  | 66.7%            |
| Average goals/game  | 2.79             |
| Shot accuracy       | 39.4%            |
| Home win rate       | 86.2%            |
| Away win rate       | 67.8%            |

A few things stand out in the data. Barcelona won 77% of matches, but still lost 15 games where they had more than 60% possession — possession alone does not close games. The venue gap is also notable: 86% wins at home versus 68% away. The 2011/2012 and 2012/2013 seasons were the peak in terms of goals per game and shot accuracy; later seasons show a slight decline, though the numbers stay elite by any reasonable measure. Against Valencia CF Barcelona averaged only 1.94 goals per game despite usually dominating the ball — Valencia were comfortably the hardest matchup in the dataset.

---

## Design decisions

**Act 1** uses a scatter plot with individual match circles. We separated them by result (Win / Draw / Loss) on the y-axis and mapped possession to the x-axis so you can immediately see whether high-possession matches cluster only around wins or also appear in losses. Venue (home vs away) is encoded with marker shape. Color follows win-green, draw-amber, loss-red.

**Act 2** is a combined bar and line chart. Bars show average total shots per season, the solid line tracks average goals, and the dotted line tracks shot accuracy on a secondary axis. It answers whether Barcelona's control was consistently converted into attacking output or whether there were seasons where efficiency dropped.

**Act 3** uses a heatmap where rows are the 12 opponents with the lowest average Barcelona goal output and columns are seasons. Darker cells mean fewer Barcelona goals — so the most dangerous opponents appear darkest. This was the main change from earlier peer feedback, which noted the original colour direction was counterintuitive.

**Act 4** is a bubble scatter. X encodes average possession, Y encodes goals per game, and bubble size encodes points per game. Barcelona is marked with a diamond so it stays readable even when other clubs overlap. It serves as the closing comparison and lets us see whether Barcelona's possession-heavy profile actually maps to elite-level outcomes.

---

## What changed after peer feedback

The earlier storyboard presented four separate tasks without a clear throughline. Peer reviewers noted there was no introduction, no explanation of why one chart followed another, and no conclusion. We restructured the whole thing as a four-act narrative and added transition text between each chart explaining what question it answers and why it follows from the previous one. Specific changes:

- Added a hero section and story cards to the landing page
- Inverted the heatmap colour scale (darker = harder opponent)
- Act 4 now explicitly functions as the conclusion rather than just another chart
- Applied direct labeling where possible to reduce legend lookups

---

## Dataset

Source: European Soccer Database (Kaggle)  
Hugo Mathien. (2016). Soccer. Kaggle.  
Adapted for VDS2526 by Inigo Bermejo.

25,979 matches | 11 leagues | 8 seasons (2008/2009 – 2015/2016)

---

**Group 3 repository:** https://github.com/salehsami/Visualisation-in-DS-Project
**Youtube Video Link:** https://youtu.be/V1OkavkefCk
