# VDS2526 Project Report — Implementation

## Part 1. Metadata

- Version: final (Part 4)
- Students: Usman Ahmed (2500039), Sefa Kayacan Citak (2505675), Mariona Espi Planet (2512208), Saleh Sami (2502333)
- Group number: Group 3
- Dataset: Football / FC Barcelona analysis (2008–2016)
- Repository: https://github.com/salehsami/Visualisation-in-DS-Project
- Data: European Soccer Database (adapted from Kaggle, curated by Inigo Bermejo for VDS2526)
- Video: https://youtu.be/V1OkavkefCk

---

## Part 2. Brief implementation overview

We built the project as a connected four-act story rather than four separate charts. The idea was to start by questioning Barcelona's identity — does their possession-heavy style actually deliver wins? — and then follow that thread through attacking efficiency over time, the opponents who most effectively disrupted that style, and finally a benchmarking view against other elite European clubs.

That structure came directly from peer feedback we received at the storyboard stage. Reviewers said the earlier version felt like four independent analyses with no clear reason to move from one to the next and no concluding recommendation. The final implementation addresses this by framing each chart as an answer to the natural next question: possession leads to wins, but how often? If it sometimes fails, is the attack still consistent? Which opponents cause the most problems? And how does all of this compare internationally?

---

## Part 3. Implemented visualisations

### Visual 1. Possession versus match outcome

#### Intended design

The goal of this visual was to open with a question rather than a summary. We wanted something that would immediately challenge the assumption that Barcelona's dominance in possession guarantees wins, especially away from home where conditions are harder to control.

#### Modification after peer feedback

This chart was not replaced, but it was reframed. In the earlier storyboard it appeared as a standalone analytical result. After feedback, we repositioned it as the opening tension in the narrative — the reason the audience should keep reading. The transitional text before the chart now explicitly sets up the question rather than just labeling the chart.

#### Actual implemented design

Each Barcelona match with available possession data appears as one circle. The y-axis separates results into three bands (Win, Draw, Loss) and horizontal position on that axis encodes possession percentage. Home and away matches use different marker shapes, and color distinguishes the three outcomes using green, amber, and red.

We chose individual marks rather than aggregates because averages would hide the cases that matter most — the high-possession losses that make the chart interesting. Position on a common scale lets readers directly compare possession values across outcomes without needing to consult a legend for the key encoding.

#### Interactions

A venue filter lets the user toggle between all matches, home matches, and away matches. Hover tooltips show the opponent, date, possession share, and final score for each match.

---

### Visual 2. Seasonal attacking efficiency

#### Intended design

The original concept here was a player development chart tracking individual scouting metrics over time. After working with the actual dataset, we found the player attribute data was not granular enough to support reliable season-by-season development curves, so we adapted the question: instead of asking which players improved, we asked whether Barcelona's team-level attacking output was consistent across the eight seasons.

#### Modification after peer feedback

Peer reviewers noted the original multi-line approach risked being visually crowded. The revised design reduces the number of series to three and uses a dual-axis layout so the shot count bars and the accuracy percentage line do not compete for the same scale.

#### Actual implemented design

Vertical bars encode average total shots per season. A solid line overlaid on the bars shows average goals per match for that season. A dotted line on a secondary right-hand axis tracks shot accuracy as a percentage. The chart title is "Turning control into chances: Barcelona by season."

This combination allows three related questions to be answered from one view: did Barcelona generate volume? Did they convert? Was there a particular season where efficiency stood out? The 2011/2012 season is the clearest peak — highest shot accuracy and goals per game in the dataset.

#### Interactions

Hover on any bar or point to see the exact figures for that season. The dual-axis design makes the accuracy line clearly distinguishable from the volume and goals lines.

---

### Visual 3. Opponents that suppress Barcelona's attack

#### Intended design

We wanted a matrix view that would let us compare across two categorical dimensions — opponent and season — to find structural patterns in where Barcelona's attack broke down rather than treating each difficult match as an isolated incident.

#### Modification after peer feedback

The main change here was the color scale direction. The earlier version used darker shades for higher goal values, which meant the "easier" games looked more intense. Peer feedback correctly identified this as counterintuitive. The final version flips this: lighter cells mean Barcelona scored more, darker cells mean fewer goals — so opponents that consistently appear dark are the ones that caused the most trouble.

#### Actual implemented design

The heatmap rows show the 12 opponents against whom Barcelona averaged the fewest goals. Columns represent seasons. Cell color encodes average Barcelona goal output, with numeric labels inside each cell for exact lookup. Rows are sorted so the most defensively effective opponents appear at the top.

This view makes Valencia CF and Hércules CF stand out immediately. Valencia appeared in multiple seasons and consistently limited Barcelona to below two goals per game despite Barcelona usually controlling possession. Hércules, a smaller club, were exceptionally hard to break down in the seasons they featured.

#### Interactions

Hovering over any cell shows the opponent, season, and exact average. The sorted row order means no extra interaction is needed to identify the most difficult opponents — they are at the top.

---

### Visual 4. Benchmarking against elite European clubs

#### Intended design

The final view needed to answer whether Barcelona's possession numbers and goal output were genuinely elite or just impressive relative to La Liga. Positioning them on a European scale gives the story a proper conclusion.

#### Modification after peer feedback

The chart type did not change significantly, but its role in the narrative did. Previously it was one of four parallel tasks. Now it explicitly functions as the closing argument: here is where Barcelona stands after everything we have shown.

#### Actual implemented design

Each club appears as a bubble. Horizontal position encodes average possession, vertical position encodes goals per game, and bubble size encodes points per game. Barcelona is highlighted with a diamond marker in a stronger color so it is always the reference point regardless of where other clubs appear. Clubs are colored by league.

Using position for the two most important variables and size for points per game keeps the chart readable without adding a fourth encoding. The visual makes it easy to see that Barcelona's possession profile aligns with Manchester City and Bayern Munich, and that their goal-scoring rate is competitive with the group.

#### Interactions

Hovering over any point shows the club name, average possession, goals per match, and shot accuracy. The Barcelona marker also has a persistent label so it is never ambiguous.

---

## Part 4. Design continuity and storytelling

The clearest change between our earlier work and the final implementation is that the four charts now answer a sequence of questions rather than sitting side by side as independent analyses.

The sequence goes: Does Barcelona's style deliver results reliably? (Act 1) How consistent is the attacking output across seasons? (Act 2) Which opponents most effectively neutralised that style? (Act 3) And how does any of this compare to the rest of Europe's elite? (Act 4)

Each chart motivates the next one. Act 1 shows that possession does not always equal wins, which raises the question of whether the attack is at least consistent — that is what Act 2 answers. Act 2 shows consistency at the season level, which prompts the question of whether certain opponents break that consistency — that is Act 3. Act 3 identifies vulnerability, but without context it is hard to know whether this is a Barcelona-specific issue or common across elite clubs — that is where Act 4 comes in.

This structure also makes the video presentation straightforward, since each transition has an explicit narrative hook.

---

## Part 5. Reproduction instructions

### Step-by-step

1. Clone the repository

   ```
   git clone https://github.com/salehsami/Visualisation-in-DS-Project.git
   cd Visualisation-in-DS-Project
   ```

2. Download the raw data from Blackboard (Project → Data folder) and place all CSV files into the `VDS2526 Football/` directory.

3. Install dependencies

   ```
   pip install pandas plotly numpy
   ```

4. Process raw data

   ```
   python process_data.py
   ```

   Output: `data/master_matches.csv` (25,979 rows) and `data/barcelona_matches.csv` (304 rows).

5. Generate charts

   ```
   python build_visualizations.py
   ```

   Output: four HTML files in `charts/`.

6. View in browser

   ```
   python -m http.server 8000
   ```

   Open `http://localhost:8000` and navigate through the four acts.

---

## Part 6. Key findings from data

### Barcelona in numbers (2008–2016)

| Metric              | Value            |
| ------------------- | ---------------- |
| Total matches       | 304              |
| Home matches        | 152              |
| Away matches        | 152              |
| Win rate            | 77.0% (234 wins) |
| Draw rate           | 14.1% (43 draws) |
| Loss rate           | 8.9% (27 losses) |
| Average possession  | 66.7%            |
| Average goals/game  | 2.79             |
| Average shots on target | 5.30         |
| Shot accuracy       | 39.4%            |

### What the data shows

**Act 1 — Possession is not sufficient on its own.** Barcelona won 77% of their matches, which is an exceptional record. But 15 of those losses came in games where they had more than 60% possession. The venue difference is also meaningful: home win rate is 86.2% against 67.8% away, an 18-point gap that suggests the style is somewhat more fragile in hostile conditions.

**Act 2 — The attack was consistent but not uniform.** Average goals across the eight seasons ranged from roughly 2.5 to 3.0 per game. The peak came in 2011/2012 when shot accuracy reached 56% and goals per game hit 3.0. Later seasons show a modest decline in accuracy, though goal output stayed above 2.5 throughout. The shot volume (bars) tells a similar story — volume stayed roughly stable while efficiency fluctuated.

**Act 3 — A small group of opponents solved the puzzle repeatedly.** Valencia CF averaged just 1.94 Barcelona goals per game across multiple seasons, the lowest in the dataset despite featuring in many meetings. Hércules CF were even more restrictive on a per-game basis (1.50 average), though they appeared in fewer seasons. Athletic Bilbao and Real Madrid also appear in the top section of difficult opponents consistently. These clubs share a tendency to defend deep and frustrate Barcelona's usual build-up patterns.

**Act 4 — Barcelona is elite in European context.** The benchmark chart shows Barcelona's 66.7% average possession is comparable to Manchester City and Bayern Munich. Their 2.79 goals per game sits in the upper cluster of European clubs. On both dimensions, they are clearly positioned among the top five or six clubs in the comparison group.

---

## Part 7. Video link

https://youtu.be/V1OkavkefCk

The video runs around 6 minutes and follows the same narrative order as the web implementation. Suggested structure:

1. Open with the possession question (Act 1) — show the home/away filter
2. Transition to the season trends (Act 2) — point out the 2011/2012 peak
3. Show the heatmap (Act 3) — name Valencia and Hércules specifically
4. Close with the benchmark (Act 4) — position Barcelona relative to Man City and Bayern
