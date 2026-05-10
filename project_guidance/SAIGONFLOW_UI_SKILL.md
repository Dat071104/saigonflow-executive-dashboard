# SaigonFlow UI Skill

Use this skill whenever building, styling, reviewing, or debugging the SaigonFlow Phase 3 dashboard UI.

## Core design direction

Commit to this aesthetic:

**Glassmorphism Pro + Executive Mobility Command Center**

The dashboard should feel like:

- A premium MaaS operations dashboard
- A Ho Chi Minh City smart mobility command center
- An investor-grade consulting analytics product
- A non-technical executive dashboard
- A polished MIS final project deliverable

Do not make it look like a default Streamlit demo or a boring school spreadsheet.

## Product story

The dashboard should communicate this story within the first 10 seconds:

1. SaigonFlow has strong traction.
2. The fleet has operational risk.
3. Weather and peak-hour demand affect usage.
4. Predictive AI creates business value.
5. The Unified Flow Platform turns fragmented data into management decisions.

## Visual identity

Use a dark navy mobility theme with cyan, teal, amber, red, and soft glass surfaces.

Recommended CSS tokens:

```css
:root {
  --bg: #06111f;
  --bg-2: #091827;
  --surface: rgba(255, 255, 255, 0.075);
  --surface-strong: rgba(255, 255, 255, 0.12);
  --border: rgba(255, 255, 255, 0.14);
  --text: #edf7ff;
  --text-muted: #9fb6c7;
  --cyan: #22d3ee;
  --teal: #14b8a6;
  --amber: #f59e0b;
  --red: #ef4444;
  --green: #22c55e;
  --purple: #8b5cf6;
}
```
Typography

Use strong visual hierarchy.

Preferred style:

Heading font: Space Grotesk, Plus Jakarta Sans, or a strong geometric sans
Body font: Plus Jakarta Sans, DM Sans, or clean sans-serif
Number/label font: JetBrains Mono or a mono-like style

If external font loading is not used, preserve hierarchy through:

large headings
tight letter spacing
high contrast
clear labels
strong number cards

Avoid:

tiny headings
default-looking metric blocks
generic gray UI
walls of tables
Layout principles

Use:

wide layout
sidebar navigation
hero command-center header
bento KPI grid
glass cards
executive callout boxes
tabs for detailed analytics
expandable evidence sections
responsive layouts
clear page titles
short explanations under charts

Every page should answer:

What should management do next?

Required dashboard sections

The final dashboard should eventually include:

Executive Overview
Balanced Scorecard
Fleet Performance
Weather & Demand
Predictive AI
ROI Recommendations
Data Evidence
UI component rules

Create reusable UI functions in app.py during later phases:

inject_global_css()
section_header()
metric_card()
glass_card()
status_badge()
insight_box()
warning_box()
render_data_status()
format_vnd()
format_pct()
load_csv_safely()
find_col()
style_fig()
HTML and CSS rules

Use HTML/CSS for:

hero section
KPI cards
glass panels
badges
dividers
recommendation cards
executive callouts
status labels

Do not use JavaScript for chart logic.

For Streamlit:

use st.html or st.markdown(..., unsafe_allow_html=True) for controlled HTML/CSS
use Plotly through st.plotly_chart for interactive charts
do not embed unsafe external scripts
do not rely on custom JavaScript for core functionality
Chart rules

Use Plotly for main interactive charts.

Charts must:

be interactive
have hover labels
use full container width
use clear titles
use readable axis labels
use consistent colors
avoid unnecessary grid clutter
use dark transparent backgrounds
support non-technical interpretation

Recommended chart mapping:

Revenue by Mode: bar chart or donut chart
Trips by Mode: bar chart
Top 10 Vehicles by Revenue: horizontal bar chart
Bottom 10 Vehicles by Revenue: horizontal bar chart
Battery Distribution: histogram
Rain vs Clear Revenue: grouped bar chart
Trips by Hour: line or bar chart
Churn Risk Levels: donut or bar chart
Vehicle Maintenance Risk Levels: donut or bar chart
Model Metrics: grouped bar chart
Color semantics

Use consistent meaning:

Healthy / Low Risk: green or teal
Watch / Medium Risk: amber
Critical / High Risk: red
Revenue: cyan or teal
AI / Prediction: purple
Neutral: muted blue-gray

Do not use color alone. Include labels.

Animation rules

Use lightweight animation only:

Allowed:

opacity
transform
subtle translateY hover
subtle glow through opacity
entrance fade

Avoid:

animating width
animating height
animating top/left
animating margin/padding
directly animating box-shadow
heavy blur on too many elements

Include reduced motion support:

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
Performance rules
Cache CSV loading with st.cache_data.
Do not load huge tables by default.
Put large tables inside expanders.
Preview top 20 rows for high-risk tables.
Use top/bottom summaries before raw data.
Avoid external APIs.
Avoid unnecessary reruns.
Keep chart transformations simple.
Accessibility rules
Maintain strong contrast.
Use readable font sizes.
Use plain-language headings.
Provide text interpretation for charts.
Use labels in addition to colors.
Keep touch targets reasonable.
Ensure mobile layout is not broken.
Business interpretation rules

Every important chart should include a short explanation:

What it shows
Why it matters
What management should do

Use this pattern:

What this means:
[Plain-English insight]

Management action:
[Specific decision or action]

Required executive messages

The final dashboard should reinforce these messages:

The Single Source of Truth connects Users, Trips, and Vehicles.
Top revenue vehicles should be protected first.
Bottom revenue vehicles may indicate poor placement or availability issues.
Rain changes commuter behavior and can justify weather-responsive pricing.
Peak-hour demand supports fleet pre-positioning.
Churn risk predictions support proactive retention.
Vehicle risk predictions support maintenance prioritization.
Predictive analytics creates ROI by reducing churn, protecting revenue, and improving uptime.
Academic honesty

The dashboard must clearly state:

The churn model uses historical user behavior and profile features.
The vehicle risk model uses a simulated operational target if true future failure labels are not available.
This is acceptable for an MIS predictive analytics simulation.
A production model would require future outcome labels, live telemetry, and monitoring.
Anti-patterns

Never produce:

default Streamlit-only styling
plain white background with generic charts
fake map visuals without coordinate data
fabricated metrics
raw tables as the main dashboard experience
chart dumps without interpretation
vague AI wording
hidden model limitations
hardcoded numbers that should be read from data

Instead:

use evidence from CSV outputs
explain business meaning
connect chart to decision
connect decision to ROI
keep UI polished but readable
Pre-submit UI checklist

Before finishing any dashboard phase, check:

Does the first screen look executive-ready?
Are KPIs visible without scrolling too much?
Are charts interactive where possible?
Are risk levels color-coded consistently?
Are chart titles readable?
Are business explanations included?
Are missing files handled gracefully?
Is the notebook untouched?
Is CHANGE_HISTORY.md updated?
Can a non-technical viewer understand what to do next?
