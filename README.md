# SaigonFlow Unified Flow Platform Dashboard

SaigonFlow Unified Flow Platform Dashboard is a local Streamlit project that turns exported analytics outputs into an executive-ready mobility operations dashboard. It combines descriptive analytics, a Balanced Scorecard, predictive churn and vehicle-risk views, a local deterministic AI copilot, and a Battery Rebalancing Advisor concept for MIS presentation and submission use.

## Business Context

SaigonFlow is framed as a smart urban mobility provider with fragmented E-Bike, Shuttle, and FlowPass systems. The project goal is to show how a Unified Flow Platform can connect users, trips, and vehicles into a Single Source of Truth for customer retention, fleet reliability, and revenue protection.

## Features

- Executive Overview with KPI and strategic narrative
- Balanced Scorecard tied to financial, customer, fleet, and AI perspectives
- Fleet Performance analysis for revenue concentration, battery condition, and maintenance priority
- Weather and demand analysis for rain behavior and peak-hour planning
- Predictive churn and vehicle-risk views based on exported notebook outputs
- Local deterministic AI Copilot for board-style Q and A
- Battery Rebalancing Advisor concept for route-level pre-positioning
- Data Evidence page anchored to exported notebook documentation

## Dashboard Pages

- Executive Overview
- Balanced Scorecard
- Fleet Performance
- Weather & Demand
- Predictive AI
- ROI Recommendations
- Data Evidence

## Predictive Analytics

The models were trained in `SaigonFlow_Phase3_Analytics_Modeling.ipynb`, and the dashboard reads the exported outputs from `outputs/`. The dashboard does not retrain models. The churn model is based on historical user behavior and profile features. The vehicle-risk target is simulated for MIS predictive analytics because true future failure labels are not available in the generated dataset.

## AI Copilot Note

The AI Copilot is local and deterministic. It uses keyword and intent matching over exported dashboard evidence. It does not call an external LLM or API.

## Battery Rebalancing Advisor Note

The Battery Rebalancing Advisor is a local recommendation layer based on exported route demand, peak pressure, and rain sensitivity evidence. It is not a live optimization engine.

## How To Run Locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The dashboard reads from `outputs/`.

## Folder Structure

- `app.py`: Streamlit dashboard entry point
- `requirements.txt`: Python dependencies
- `.streamlit/config.toml`: Streamlit configuration
- `outputs/`: Exported notebook evidence used by the dashboard
- `project_guidance/`: Rules, UI guidance, and change history
- `submission_package/`: Overleaf package, AI log, GitHub checklist, and copied evidence

## Academic Honesty

This repository keeps the notebook-based training workflow separate from the dashboard presentation layer. Exported outputs are used as evidence, and the report package includes an AI usage log. The vehicle-risk model is transparently described as a simulated predictive analytics exercise for MIS coursework.

## Limitations

- The dashboard depends on the quality of the exported outputs.
- The vehicle-risk model uses a simulated target rather than true future failure outcomes.
- The AI Copilot is explanatory only and should not be presented as a real LLM.
- The project is local-first and does not include live APIs, authentication, or deployment infrastructure.

## Authors

Student team: `722I0004` and `523K0078`
