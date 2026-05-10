# SaigonFlow Local Executive Dashboard

## 1. What Phase 3 adds

Phase 3 turns the Streamlit skeleton into a presentation-ready local executive dashboard.

This phase adds:

- fuller interactive Plotly charts
- richer KPI logic
- presentation-focused UI polish
- Presentation Mode toggle
- stronger Balanced Scorecard integration
- deeper Fleet Performance, Weather & Demand, and Predictive AI pages
- AI Board Assistant as a global local copilot for board/demo Q&A
- final ROI recommendation cards
- stronger data evidence and QA workflow
- responsive support for laptop and mobile

The dashboard still acts as a presentation layer only and reads from `outputs/`.

## 2. How to run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the dashboard:

```bash
python -m streamlit run app.py
```

## 3. Expected URL

The default local URL is:

`http://localhost:8501`

## 4. Dashboard page list

The dashboard includes:

- Executive Overview
- Balanced Scorecard
- Fleet Performance
- Weather & Demand
- Predictive AI
- ROI Recommendations
- Data Evidence

## 5. Interactive chart list

Phase 3 uses Plotly for the main interactive charts, including:

- Revenue by Mode
- Revenue Share by Mode
- Trips by Mode
- Executive Risk Snapshot
- Balanced Scorecard snapshot chart
- Top 10 Vehicles by Revenue
- Bottom 10 Vehicles by Revenue
- Battery Level Distribution
- Maintenance Risk Level Breakdown
- Revenue vs Battery
- Trip Count vs Battery
- Rain vs Clear Revenue
- Rain vs Clear Trip Count
- Trips by Weather Condition
- Revenue by Weather Condition
- Trips by Hour
- Revenue by Hour
- Weekend vs Weekday Trips
- Peak vs Non-Peak comparison
- User count by Churn Risk Level
- Churn probability distribution
- Churn probability by Preferred Mode
- Churn probability vs Loyalty Points
- Vehicle count by Maintenance Risk Level
- Action probability distribution
- Action probability by Type
- Action probability vs Battery Level
- Model metrics grouped chart

## 6. Presentation Mode explanation

Presentation Mode is a sidebar toggle that changes how the dashboard prioritizes information.

When Presentation Mode is ON:

- executive summaries appear first
- evidence tables stay collapsed by default
- raw inspection noise is reduced
- the layout is more screenshot- and demo-friendly
- Data Evidence emphasizes `codex_phase3_report.md`

When Presentation Mode is OFF:

- more detailed evidence is easier to inspect
- expanders open more aggressively where helpful
- the app is better suited to debugging and grading walkthroughs

## 7. Data source explanation

The dashboard reads only from exported notebook outputs in `outputs/`, including:

- `master_dataset.csv`
- `vehicle_utilization.csv`
- `top10_vehicle_revenue.csv`
- `bottom10_vehicle_revenue.csv`
- `rain_vs_clear_analysis.csv`
- `churn_model_dataset.csv`
- `vehicle_model_dataset.csv`
- `churn_risk_predictions.csv`
- `vehicle_risk_predictions.csv`
- `balanced_scorecard.csv`
- `model_metrics_summary.csv`
- `codex_phase3_report.md`
- exported PNG files may be detected, but they are intentionally hidden from web presentation view

The notebook is not modified by the dashboard.

## 8. Academic honesty note

The churn model uses historical user behavior and profile features from the generated outputs.

The vehicle risk model uses a simulated operational target because the generated dataset does not contain true future failure labels. This is acceptable for a Phase 3 predictive analytics simulation, but production deployment would require future maintenance or failure outcome data plus live monitoring.

## 9. AI Board Assistant

The dashboard includes a global local AI Board Assistant / copilot.

It:

- answers in English
- shows 4 suggested questions for a clean demo
- supports natural free typing beyond those suggestions
- uses keyword and intent matching against exported dashboard data
- uses exported dashboard metrics and prediction tables only
- does not call an external LLM or API
- helps explain churn risk, vehicle risk, ROI, Balanced Scorecard alignment, presentation talking points, and model limitations

It is meant for presentation Q&A and board-level explanation. It uses local keyword and intent matching, not an external API or real LLM.

Demo tip:

"Use the AI Board Assistant during presentation Q&A to explain churn risk, vehicle risk, ROI, and model limitations."

## 10. Troubleshooting

- If `streamlit` is missing, run `python -m pip install -r requirements.txt`.
- If a CSV file is missing, the app should show warnings and continue rendering other sections.
- If a column name differs slightly, the app tries flexible column matching before skipping a chart.
- If a Plotly chart cannot render because data is empty or non-numeric, the app should warn instead of crashing.
- If the app looks incomplete, verify the required exports exist in `outputs/`.

## 11. Debug log workflow

- Read the traceback carefully.
- Fix the smallest correct issue.
- Preserve working logic that is unrelated to the bug.
- Do not modify the notebook or `outputs/`.
- Log future dashboard bugs and fixes in `project_guidance/CHANGE_HISTORY.md`.

## 12. Submission/demo checklist

- Run notebook only if outputs are missing.
- Run Streamlit dashboard.
- Open Executive Overview first.
- Capture screenshots.
- Show Predictive AI page during presentation.
- Use the AI Board Assistant for live board-style Q&A.
- Include AI Usage Log in final submission.
- Include Executive Summary Report / Part 4.
