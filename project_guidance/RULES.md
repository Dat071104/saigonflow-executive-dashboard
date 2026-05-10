# SaigonFlow Dashboard Build Rules

## Purpose

This file defines the non-negotiable rules for building the SaigonFlow Phase 3 local executive dashboard.

The dashboard will be built in later phases using the existing notebook outputs. The dashboard must act as a presentation layer only.

## Source of truth

The source of truth is the existing analytics output folder:

`outputs/`

The dashboard may read these files if available:

- `outputs/master_dataset.csv`
- `outputs/vehicle_utilization.csv`
- `outputs/top10_vehicle_revenue.csv`
- `outputs/bottom10_vehicle_revenue.csv`
- `outputs/rain_vs_clear_analysis.csv`
- `outputs/churn_model_dataset.csv`
- `outputs/vehicle_model_dataset.csv`
- `outputs/churn_risk_predictions.csv`
- `outputs/vehicle_risk_predictions.csv`
- `outputs/balanced_scorecard.csv`
- `outputs/model_metrics_summary.csv`
- `outputs/codex_phase3_report.md`
- `outputs/*.png`

## Non-negotiable rules

1. Do not edit `SaigonFlow_Phase3_Analytics_Modeling.ipynb`.
2. Do not rerun training unless the user explicitly asks.
3. Do not modify original generated CSV files.
4. Do not overwrite existing output CSVs.
5. Do not overwrite existing output PNGs.
6. Do not fabricate metrics or exact numbers.
7. If a metric is unavailable, show `"N/A"` or a clear warning.
8. Do not call external APIs.
9. Do not require login.
10. Do not create a cloud deployment.
11. Do not add a database.
12. Do not use FastAPI, Flask, React, Next.js, or backend servers unless explicitly requested later.
13. Keep the dashboard local-first.
14. Keep the dashboard presentation-ready for a non-technical MIS audience.
15. All dashboard code must read from exported outputs, not from hidden notebook state.

## Dashboard objective

The final dashboard must help a non-technical executive, professor, or fleet manager understand:

- Total business performance
- Balanced Scorecard metrics
- Revenue by mode
- Top 10 and bottom 10 vehicles by revenue
- Rain vs Clear behavior
- Peak-hour demand
- Battery and maintenance risk
- Customer churn prediction
- Vehicle maintenance/failure risk prediction
- ROI recommendations

## MIS grading alignment

The dashboard must support MIS Phase 3 and Tier 4 by showing:

- Descriptive analytics
- Top 10 most profitable vehicles
- Bottom 10 least profitable vehicles
- Rain vs Clear customer behavior
- Predictive output
- Balanced Scorecard targets
- Business ROI interpretation

## Data handling rules

When loading files:

1. Use safe file loading.
2. If a file is missing, do not crash.
3. Show a warning inside the dashboard.
4. Continue rendering other available sections.
5. Log missing files in `project_guidance/CHANGE_HISTORY.md`.

When loading columns:

1. Use flexible column matching when possible.
2. Match case-insensitively.
3. Ignore spaces, underscores, and hyphens when matching.
4. If a required column is missing, show a warning instead of crashing.
5. Do not invent substitute values.

## Debug discipline

When an error happens:

1. Read the traceback carefully.
2. Identify the root cause.
3. Fix the smallest correct thing.
4. Do not rewrite unrelated working code.
5. Do not repeat the same failed fix twice.
6. Update `project_guidance/CHANGE_HISTORY.md` with:
   - timestamp
   - error or symptom
   - root cause
   - fix
   - prevention rule
7. Run the check again.

## Phase discipline

This project is phase-based.

### Phase 1
Create guidance files only:
- `RULES.md`
- `SAIGONFLOW_UI_SKILL.md`
- `CHANGE_HISTORY.md`

Do not build the dashboard in Phase 1.

### Phase 2
Create dashboard skeleton:
- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `README_DASHBOARD.md`

Phase 2 should focus on layout, navigation, safe data loading, and UI shell.

### Phase 3
Add interactive charts and final UX polish:
- Plotly interactive charts
- KPI cards
- Balanced Scorecard
- Predictive AI pages
- ROI recommendations
- Data evidence page
- Debug and final report

## Final rule

If unsure, preserve existing analysis and ask through the final report instead of editing the notebook or outputs.
