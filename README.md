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
