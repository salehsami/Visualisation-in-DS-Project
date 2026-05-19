#!/usr/bin/env python
"""
Quick verification script to confirm all Part 4 deliverables are in place.
Run this to ensure everything is ready for final submission.
"""

import os
from pathlib import Path


def check_file(path, description):
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists


def check_dir(path, description):
    exists = Path(path).is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists


print("=" * 70)
print("PART 4 SUBMISSION VERIFICATION")
print("=" * 70)

print("\n📁 DIRECTORY STRUCTURE")
print("-" * 70)
all_good = True
all_good &= check_dir(".", "Project root")
all_good &= check_dir("data", "Data folder (processed CSVs)")
all_good &= check_dir("charts", "Charts folder (visualizations)")
all_good &= check_dir("report", "Report folder")
all_good &= check_dir("VDS2526 Football", "Raw data folder")

print("\n📄 CORE FILES")
print("-" * 70)
all_good &= check_file("index.html", "Main web page")
all_good &= check_file("app.js", "JavaScript interactivity")
all_good &= check_file("styles.css", "CSS styling")
all_good &= check_file("README.md", "Documentation")

print("\n🐍 PYTHON SCRIPTS")
print("-" * 70)
all_good &= check_file("process_data.py", "Data processing pipeline")
all_good &= check_file("build_visualizations.py", "Chart generation")
all_good &= check_file("generate_report_stats.py", "Statistics extraction")

print("\n📊 PROCESSED DATA")
print("-" * 70)
all_good &= check_file("data/master_matches.csv", "Master dataset (25,979 matches)")
all_good &= check_file("data/barcelona_matches.csv", "Barcelona dataset (304 matches)")

print("\n📈 VISUALIZATIONS")
print("-" * 70)
all_good &= check_file(
    "charts/act1_possession_vs_result.html", "Act 1: Possession analysis"
)
all_good &= check_file("charts/act2_hidden_gems"".html", "Act 2: Season trends")
all_good &= check_file(
    "charts/act3_kryptonite_heatmap.html", "Act 3: Difficult opponents"
)
all_good &= check_file("charts/act4_european_benchmark.html", "Act 4: Elite comparison")

print("\n📝 REPORTS")
print("-" * 70)
all_good &= check_file(
    "report/implementation-report-draft.md", "Final report (with real data)"
)
all_good &= check_file("SUBMISSION_CHECKLIST.md", "Submission checklist")

print("\n" + "=" * 70)
if all_good:
    print("✅ ALL DELIVERABLES PRESENT & READY FOR SUBMISSION")
else:
    print("⚠️ SOME FILES MISSING - PLEASE CHECK ABOVE")
print("=" * 70)

print("\n📊 QUICK STATISTICS")
print("-" * 70)

# Check file sizes
import os

for file in ["data/master_matches.csv", "data/barcelona_matches.csv"]:
    if Path(file).exists():
        size_mb = os.path.getsize(file) / (1024 * 1024)
        print(f"   {file}: {size_mb:.1f} MB")

print("\n🎯 NEXT STEPS")
print("-" * 70)
print("1. Run: python -m http.server 8000")
print("2. Visit: http://localhost:8000")
print("3. Test all 4 visualizations")
print("4. Record 3-5 minute video presentation")
print("5. Add YouTube link to report/implementation-report-draft.md (Part 7)")
print("6. Submit to Blackboard with:")
print("   - GitHub repository link")
print("   - Final report PDF")
print("   - Video URL")

print("\n" + "=" * 70)
