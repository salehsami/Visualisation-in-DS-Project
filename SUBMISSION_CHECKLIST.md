# PART 4 SUBMISSION CHECKLIST

**Project:** Visualisation in Data Science 2025/2026  
**Group:** 3  
**Students:** Usman Ahmed (2500039), Sefa Kayacan Citak (2505675), Mariona Espi Planet (2512208), Saleh Sami (2502333)  
**Submission Date:** May 2026

---

## ✅ DELIVERABLES COMPLETED

### 1. Data Processing Pipeline

- [x] `process_data.py` — Processes 25,979 matches into structured datasets
  - [x] `data/master_matches.csv` — All 25,979 matches with all metrics
  - [x] `data/barcelona_matches.csv` — 304 Barcelona matches extracted
  - [x] Computed metrics: possession, shots, goals, results, points
  - [x] Data validation: 227 matches with possession data

### 2. Visualization Generation

- [x] `build_visualizations.py` — Generates 4 interactive Plotly charts
  - [x] `charts/act1_possession_vs_result.html` — Scatter with jitter (227 data points)
  - [x] `charts/act2_control_into_chances.html` — Combo chart (8 seasons)
  - [x] `charts/act3_kryptonite_heatmap.html` — Heatmap (12 opponents × 8 seasons)
  - [x] `charts/act4_european_benchmark.html` — Bubble chart (6 elite clubs)

### 3. Web Application

- [x] `index.html` — Responsive landing page with narrative
  - [x] Hero section explaining project context
  - [x] Story cards describing 4-act narrative
  - [x] Question strip showing guiding questions
  - [x] Embedded visualizations with interactions
  - [x] Mobile-optimized design

- [x] `app.js` — JavaScript interactivity (updated for production data)
  - [x] Tooltip handlers
  - [x] Filter controls
  - [x] Event listeners

- [x] `styles.css` — Professional styling
  - [x] Responsive breakpoints (mobile, tablet, desktop)
  - [x] Custom color palette (green/amber/red)
  - [x] Typography (DM Serif Display + Inter)

### 4. Documentation

- [x] `README.md` — Comprehensive guide
  - [x] Quick start instructions
  - [x] File structure explained
  - [x] Data pipeline documentation
  - [x] Barcelona performance summary with real statistics
  - [x] Key findings from analysis
  - [x] Design rationale
  - [x] Peer feedback implementation

- [x] `report/implementation-report-draft.md` — Final report
  - [x] Part 1: Metadata (all student names, group, dataset)
  - [x] Part 2: Implementation overview
  - [x] Part 3: Visualization descriptions with design rationale
  - [x] Part 4: Design continuity and storytelling
  - [x] Part 5: Reproduction instructions (step-by-step)
  - [x] Part 6: Key findings with real data
  - [x] Part 7: Video link placeholder

### 5. Supporting Scripts

- [x] `generate_report_stats.py` — Generates Barcelona statistics
  - [x] Match statistics (304 matches total)
  - [x] Results breakdown (77% wins)
  - [x] Possession analysis
  - [x] Shooting statistics
  - [x] Season breakdown
  - [x] Difficult opponents identified
  - [x] Venue comparison

---

## 📊 DATA SUMMARY

| Metric                  | Value            |
| ----------------------- | ---------------- |
| Total matches processed | 25,979           |
| Barcelona matches       | 304              |
| Home matches            | 152              |
| Away matches            | 152              |
| Win rate                | 77.0% (234 wins) |
| Draw rate               | 14.1%            |
| Loss rate               | 8.9%             |
| Avg possession          | 66.7%            |
| Avg goals/game          | 2.79             |
| Shot accuracy           | 39.4%            |
| Home win rate           | 86.2%            |
| Away win rate           | 67.8%            |

---

## 🎯 NARRATIVE STRUCTURE

### Act 1: Challenge the Identity (Possession vs Result)

- **Question:** Does high possession reliably translate into wins?
- **Finding:** Barcelona wins 77% overall, but 15 losses with >60% possession
- **Interaction:** Filter by home/away to see venue difference
- **Data points:** 227 matches with possession data

### Act 2: Look at Conversion (Season Trends)

- **Question:** Does control become attacking output and shot quality?
- **Finding:** Consistent 2.5–3.0 goals/game across 8 seasons; peak in 2011/2012
- **Interaction:** Hover to see year-by-year metrics
- **Trend:** Slight decline in later seasons but still elite

### Act 3: Name the Difficult Opponents (Heatmap)

- **Question:** Which opponents suppress Barcelona's attack the most?
- **Finding:** Valencia CF (1.94 avg goals), Hércules CF (1.50 avg goals) most defensive
- **Interaction:** Hover cells for exact values; sorted by difficulty
- **Insight:** Defensive specialists consistently reduce Barcelona's output

### Act 4: End with Context (European Benchmark)

- **Question:** How does Barcelona compare with Europe's biggest clubs?
- **Finding:** Possession aligns with Man City/Bayern; comparable goal-scoring rate
- **Interaction:** Bubble size shows efficiency; click league filters
- **Strategic Context:** Barcelona is elite by European standards

---

## 🎨 DESIGN DECISIONS

### Color Palette

- **#2f7d60** = Win (green, positive connotation)
- **#d6a74d** = Draw (amber, neutral)
- **#bb4d4d** = Loss (red, negative)
- **#912f40** = Accent/highlight (burgundy)
- **#1f2a30** = Text (ink black for contrast)

### Encoding Principles

- **Position on common scale** → Possession % (accurate for quantitative comparison)
- **Hue** → Result (categorical, color-blind friendly)
- **Mark type (circle/diamond)** → Venue (home vs away)
- **Bubble size** → Efficiency/performance (secondary variable)

### Interaction Design

- **Hover tooltips** → Detailed data without chart clutter
- **Venue filters** → Compare home/away patterns easily
- **Direct labeling** → Reduce cognitive load (eye movement to legend)
- **Sorted heatmap rows** → Immediate visual hierarchy

---

## 📁 FILE MANIFEST

```
Root Directory:
├── ✅ index.html (main page)
├── ✅ app.js (interactions)
├── ✅ styles.css (styling)
├── ✅ README.md (full documentation)
├── ✅ process_data.py (data pipeline)
├── ✅ build_visualizations.py (chart generation)
├── ✅ generate_report_stats.py (statistics)
│
├── data/ (processed datasets)
│   ├── ✅ master_matches.csv (25,979 records)
│   ├── ✅ barcelona_matches.csv (304 records)
│   └── (sample-data.js removed — was legacy placeholder)
│
├── charts/ (generated interactive charts)
│   ├── ✅ act1_possession_vs_result.html
│   ├── ✅ act2_control_into_chances.html
│   |__ ✅ act3_kryptonite_heatmap.html
│   └── ✅ act4_european_benchmark.html
│
├── report/
│   └── ✅ implementation-report-draft.md (FINAL)
│
└── VDS2526 Football/ (raw data from Blackboard)
    ├── Match.csv
    ├── Match_Possesion.csv
    ├── Match_Shots_On.csv
    ├── ... (13 CSV files total)
```

---

## 🔄 REPRODUCIBILITY

**Anyone can reproduce this project in 4 steps:**

```bash
1. pip install pandas plotly numpy
2. python process_data.py          # Creates CSV datasets
3. python build_visualizations.py  # Generates 4 HTML charts
4. python -m http.server 8000      # Launch web server
```

Then navigate to `http://localhost:8000` in browser.

---

## 📹 VIDEO PRESENTATION

**Status:** Not recorded yet — required before submission  
**Required sections (3–5 minutes):**

1. Introduction: "FC Barcelona's passing style under scrutiny"
2. Act 1 demo: Show possession-result relationship, home vs away
3. Act 2 demo: Season-by-season consistency in shots and goals
4. Act 3 demo: Identify the hardest opponents using heatmap
5. Act 4 demo: European benchmarking conclusion
6. Wrap-up: "Barcelona is elite, but certain opponents neutralize possession"

_Record, upload to YouTube, and add URL to report Part 7 before submission_

---

## ✨ PEER FEEDBACK IMPLEMENTATION

| Original Feedback                   | Action Taken                             | Result                                                     |
| ----------------------------------- | ---------------------------------------- | ---------------------------------------------------------- |
| Lacked clear introduction           | Added hero section + story cards         | Audience immediately understands narrative                 |
| 4 isolated tasks                    | Reframed as 4-act story with transitions | Logical flow: problem → response → vulnerability → context |
| Unclear motivations between visuals | Added transitional text explaining "why" | Each chart answers a natural follow-up question            |
| No concluding recommendation        | Act 4 now serves as strategic takeaway   | Ends with actionable insight about European positioning    |
| Chart felt crowded                  | Applied filtering + direct labeling      | Reduced cognitive load, cleaner visuals                    |
| Heatmap color scale unintuitive     | Inverted scale (darker = harder)         | Immediate comprehension without legend reading             |

---

## 📋 FINAL CHECKLIST

- [x] All 4 visualizations generated with real data
- [x] Web application complete and functional
- [x] Data pipeline fully documented
- [x] Report filled with real statistics and findings
- [x] README comprehensive and clear
- [x] Design rationale explained
- [x] Peer feedback explicitly addressed
- [x] Repository clean and organized
- [x] All student names and IDs included
- [x] Links to GitHub repository added
- [x] Dataset attribution included
- [x] Reproduction instructions tested and verified
- [ ] Video recorded and YouTube link added to report Part 7

---

## 🎯 NEXT STEPS FOR SUBMISSION

1. **Record video presentation** (3–5 minutes)
   - Demonstrate all 4 visualizations
   - Explain narrative flow and design choices
   - Present key findings
   - Add YouTube link to report Part 7

2. **Final quality review**
   - Test web application on multiple browsers
   - Verify all chart interactions work
   - Check responsive design on mobile
   - Proofread all documentation

3. **Submit to Blackboard**
   - Repository link (GitHub)
   - ZIP file with all code
   - Final report PDF
   - Video link

---

**Data Processed:** ✅ 25,979 matches  
**Visualizations Generated:** ✅ 4 interactive charts  
**Report Completed:** ✅ With real metrics  
**Video:** ❌ Not recorded yet  
**Ready for Submission:** ⚠️ Pending video
