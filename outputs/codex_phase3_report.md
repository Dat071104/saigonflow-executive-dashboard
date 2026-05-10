
# SaigonFlow Phase 3 Analytics & Predictive Modeling — Codex Execution Report

## 1. What was built
This notebook uses the group's unique CSV files to build a complete Phase 3 analytics and predictive modeling workflow for SaigonFlow. It loads, validates, cleans, joins, analyzes, models, visualizes, and exports operational decision-support outputs for ROI, retention, fleet reliability, and Balanced Scorecard reporting.

## 2. Dataset validation summary
The notebook validated the required columns for Trips, Users, and Vehicles. The observed shapes are Trips `(10000, 18)`, Users `(2200, 5)`, and Vehicles `(2100, 4)`. Timestamp and maintenance date fields were converted to datetime, and derived fields were created for trip date, hour, month, peak hour, and rain category.

## 3. How the SSOT join works
Trips join to Users via UserID. Trips join to Vehicles via VehicleID where available. Missing VehicleID in Metro/Bus trips is expected because Metro/Bus trips do not use SaigonFlow-owned vehicles. These rows are retained in `master_df` for customer, weather, and revenue analysis, while `vehicle_trip_df` filters to owned-vehicle trips for fleet-specific analysis. This join simulates the Unified Flow Platform as a Single Source of Truth across previously fragmented systems.

## 4. Descriptive analytics completed
The notebook produced KPI summaries, revenue and trip tables by mode, top and bottom vehicle revenue tables, vehicle utilization segments, maintenance risk levels, rain vs clear analysis, weather comparisons, trips and revenue by hour, peak vs non-peak behavior, and weekend vs weekday behavior. It also saved the required PNG charts into `./outputs`.

## 5. Churn model logic
The churn model uses historical user behavior and profile features including trip count, total revenue, average fare, average duration, mode usage, weekend share, rain share, peak share, station diversity, recency, tenure, temperature, age, preferred mode, and loyalty points. The target is `Has_Churned`, and the model avoids using the target as a feature.

## 6. Vehicle risk model logic
The vehicle model uses a simulated operational risk label because true future failure data is not available. `Vehicle_Needs_Action` is flagged when battery is below 20%, maintenance age exceeds 30 days, or battery is below 40% while utilization is above the median. This still satisfies the project requirement because Phase 3 asks for predictive analytics proposal/simulation and ROI explanation.

## 7. Balanced Scorecard logic
The Balanced Scorecard maps analytics outputs to Financial, Customer, Internal Process / Fleet, and Learning & Growth / AI perspectives. The table links revenue, churn, weather behavior, fleet battery status, peak utilization, model F1 scores, and AI-generated recommendations to management targets.

## 8. Files exported
- balanced_scorecard.csv
- battery_distribution.png
- bottom10_vehicle_revenue.csv
- churn_model_confusion_matrix.png
- churn_model_dataset.csv
- churn_risk_predictions.csv
- master_dataset.csv
- model_metrics_summary.csv
- rain_vs_clear_analysis.csv
- rain_vs_clear_revenue.png
- revenue_by_mode.png
- top10_vehicle_revenue.csv
- top10_vehicle_revenue.png
- trips_by_hour.png
- vehicle_model_confusion_matrix.png
- vehicle_model_dataset.csv
- vehicle_risk_predictions.csv
- vehicle_utilization.csv
- weather_trip_count.png

## 9. How this satisfies MIS Phase 3 Tier 4
The notebook goes beyond static descriptive reporting by creating a validated Single Source of Truth, business KPI layer, chart exports, two predictive analytics outputs, model comparison tables, confusion matrices, feature importance outputs, risk recommendations, ROI logic, and a Balanced Scorecard. The work is runnable top-to-bottom in VS Code with direct kernel outputs.

## 10. Limitations and academic honesty notes
The churn model depends on the quality and design of the generated historical dataset. The vehicle model is partly rule-based because true future failure labels are not available. Therefore, the vehicle output should be presented as a transparent predictive analytics simulation and maintenance-priority prototype rather than a production telemetry model.

## 11. Next step: how to convert outputs into Power BI/slides later
The exported CSV files can be loaded into Power BI as fact and dimension tables, while the PNG charts and Markdown report can be reused in slides. Recommended next visuals are a KPI dashboard, churn-risk customer table, vehicle maintenance queue, weather-demand view, and Balanced Scorecard executive page.

**Consulting conclusion.** SaigonFlow should use the Unified Flow Platform as a Single Source of Truth to connect customer, trip, and vehicle data. The descriptive analytics identify revenue concentration, weather-sensitive behavior, peak-hour demand, and underperforming vehicles. The predictive outputs allow SaigonFlow to flag churn-prone users and maintenance-priority vehicles before revenue is lost. This creates measurable ROI through improved retention, higher fleet uptime, smarter redistribution, and better customer intimacy.
