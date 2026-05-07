# VDS2526 Project Report - Implementation Draft

## Part 1. Metadata

- Version: draft 1
- Students: `[add names and student numbers]`
- Group number: `Group 3`
- Dataset: Football / FC Barcelona analysis

## Part 2. Brief implementation overview

Our implementation presents the football project as a connected story rather than four independent charts. The narrative begins by testing whether Barcelona's possession-heavy style actually leads to strong results, especially away from home. It then moves toward recruitment and squad planning, identifies opponents that most effectively suppress Barcelona's attack, and closes by benchmarking Barcelona against other elite European clubs.

This sequence was chosen in response to peer feedback stating that the earlier storyboard lacked a clear introduction, transitions between tasks, and a concluding recommendation. The final implementation therefore includes an explicit narrative arc: diagnosis, response, vulnerability, and context.

## Part 3. Implemented visualisations

### Visual 1. Possession versus match outcome

#### Intended design

The intended design was an analytical opening visual that could immediately challenge the assumption that dominating possession guarantees success. The goal was to show match-level variability rather than only averages, with special attention to away games.

`[Insert sketch or mock-up image here]`

#### Modification after peer feedback

This visual was not fundamentally replaced, but it was repositioned within a stronger story. Instead of appearing as one separate task, it now acts as the opening tension in the narrative. This addresses the feedback that the original storyboard lacked a clear introductory slide and a reason for moving from one task to the next.

#### Actual implemented design

The implemented design uses individual circles to encode matches. Horizontal grouping separates results into wins, draws, and losses, while horizontal position on a common scale encodes possession percentage. Colour is used to distinguish outcomes, with green for wins, amber for draws, and red for losses.

This encoding was chosen because position on a common scale is an accurate channel for quantitative comparison, allowing the audience to quickly assess whether high-possession matches cluster only around wins or also appear among losses. Plotting individual matches also preserves variation that would be hidden by simple averages.

#### Interactions

The visual includes a venue filter that allows the user to switch between all matches, home matches, and away matches. Hover tooltips show opponent, venue, possession share, and final score for each match.

#### Implementation note

This view should be connected to a match-level table containing opponent, venue, possession, result, goals scored, goals conceded, and season.

---

### Visual 2. Scouting and player development

#### Intended design

The original intended design was a multi-line chart showing how players developed over time according to a scouting metric related to short passing and vision.

`[Insert sketch or mock-up image here]`

#### Modification after peer feedback

This visual was significantly improved following peer feedback. The feedback noted that a large multi-line chart could become overcrowded and that the visual did not directly support ranking players. To address this, the implementation uses direct labels at the end of lines and filtering controls so that only a manageable number of players need to be compared at one time.

#### Actual implemented design

The implemented design uses lines to encode player development across seasons and point markers to indicate the score in each season. Horizontal position encodes season and vertical position encodes the development score. Player names are placed directly at the end of each line, which reduces the cognitive load of repeatedly consulting an external legend.

This design follows visualisation principles of reducing unnecessary eye movement and improving readability through direct labelling. It also supports the analytical goal better than the original concept because it makes both trend and latest rank more visible.

#### Interactions

The user can toggle players on and off to focus on specific comparisons. Hover interactions reveal the player name, season, and metric value for each point.

#### Implementation note

Before finalising this view, the report should explicitly define the scouting metric. For example, it could be a composite score derived from short passing, vision, ball retention, and progression, or a simpler single-metric trend if the data is limited.

---

### Visual 3. Kryptonite opponents heatmap

#### Intended design

The intended design was a heatmap showing which opponents most effectively shut down Barcelona's attack across seasons.

`[Insert sketch or mock-up image here]`

#### Modification after peer feedback

Peer feedback suggested that the original colour scale was counterintuitive because darker tones represented lower values. The implemented version corrects this by applying a more standard interpretation where higher values are darker and visually heavier. The heatmap rows are also ordered so the most problematic opponents appear first.

#### Actual implemented design

The implemented heatmap uses rectangular cells as marks. The two dimensions are opponent and season, while colour intensity encodes Barcelona's attacking output against that opponent. Numeric labels inside the cells provide exact values, allowing the visual to function for both overview and lookup.

The design was chosen because heatmaps are effective for finding clusters and contrasts across two categorical dimensions. Sorting the rows by average goal output helps reveal the strongest “kryptonite” opponents immediately.

#### Interactions

Hover interaction reveals the opponent, season, and exact value. In a fuller version, the heatmap could also support sorting or filtering by venue or competition.

#### Implementation note

The report should define what “shutting down the attack” means. In our current implementation, it is operationalised as low Barcelona goal output against a given opponent.

---

### Visual 4. Benchmarking against elite clubs

#### Intended design

The intended design was a comparative summary visual positioning Barcelona against top European clubs.

`[Insert sketch or mock-up image here]`

#### Modification after peer feedback

This visual mainly changed in narrative role rather than chart type. Instead of being one isolated comparison task, it now serves as the concluding panel that answers the larger question of where Barcelona stands relative to other elite teams.

#### Actual implemented design

The implemented design uses a scatterplot. Horizontal position encodes average possession, vertical position encodes goals per game, and circle size encodes points per game. Barcelona is highlighted with a stronger colour so it remains the focal reference point.

This visual encoding is effective because it supports multivariate comparison while maintaining interpretability. Position is used for the two most important measures and size is used for a secondary performance summary.

#### Interactions

Hovering over any point reveals the club name and all key metrics. In a more advanced version, the chart could support filtering by league or season.

#### Implementation note

This final view should support the concluding argument in the video and report by making clear whether Barcelona's possession profile is accompanied by elite-level outcomes.

## Part 4. Design continuity and storytelling

The strongest implementation change compared with the earlier design work is the continuity between visuals. The four charts are now framed as answers to one strategic sequence of questions:

1. Does Barcelona's style reliably deliver results?
2. If not always, which players can help sustain the style?
3. Against which opponents does the style break down the most?
4. How serious is the problem when Barcelona is compared with elite clubs?

This continuity directly addresses the peer feedback that the original storyboard lacked intermediate explanations and a coherent narrative flow. It also improves the final video presentation because each visual naturally motivates the next one.

## Part 5. Reproduction instructions

`[Replace this section with your final repository link and exact steps]`

Suggested wording:

1. Clone or download the repository.
2. Open the project folder.
3. Launch a local server from the root directory.
4. Open `index.html` in the browser through the local server.
5. Interact with the four visualisations using the filters and hover tooltips.

## Part 6. Video link

`[Paste full YouTube URL here]`

In the 3 to 5 minute video, structure the demonstration using the same narrative order as the web implementation: opening problem, scouting response, kryptonite opponents, and final benchmark conclusion.
