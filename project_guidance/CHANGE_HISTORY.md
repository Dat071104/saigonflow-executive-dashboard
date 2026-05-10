SaigonFlow Dashboard Change History

This file records changes, bugs, fixes, and debugging lessons across dashboard build phases.

Log format

Each entry must use this format:

YYYY-MM-DD HH:MM — Short title

Changed

...

Why

...

Error / Symptom

...

Root Cause

...

Fix

...

Prevention Rule

...
Entries
Current session — Phase 1 guidance initialized

Changed

Created project_guidance/RULES.md.
Created project_guidance/SAIGONFLOW_UI_SKILL.md.
Created project_guidance/CHANGE_HISTORY.md.

Why

Establish project rules before building the local dashboard.
Prevent accidental edits to the analytics notebook or exported outputs.
Define a reusable UI design system for the SaigonFlow dashboard.
Create a debugging log so future fixes are not repeated blindly.

Error / Symptom

None.

Root Cause

Not applicable.

Fix

Not applicable.

Prevention Rule

Future dashboard phases must read RULES.md and SAIGONFLOW_UI_SKILL.md before editing or creating dashboard files.
Every bug fix must be recorded in this file.

### 2026-05-10 13:26 — Phase 2 dashboard skeleton

**Changed**
- Created/updated `app.py`.
- Created/updated `requirements.txt`.
- Created/updated `.streamlit/config.toml`.
- Created/updated `README_DASHBOARD.md`.
- Added dashboard skeleton, safe data loading, sidebar, basic pages, and simple Plotly charts.

**Why**
- Establish a working local dashboard foundation before adding full chart polish in Phase 3.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep Phase 2 limited to skeleton and safe loading.
- Do not add complex chart logic until Phase 3.
- Preserve notebook and outputs.

### 2026-05-10 13:37 — Phase 3 final dashboard polish

**Changed**
- Improved `app.py` with full interactive chart integration.
- Added or improved final UI/UX polish.
- Added Presentation Mode.
- Strengthened Balanced Scorecard, Fleet Performance, Weather & Demand, Predictive AI, ROI, and Data Evidence pages.
- Updated `README_DASHBOARD.md`.
- Ran final QA checks.

**Why**
- Make the dashboard presentation-ready and aligned with MIS Phase 3 / Tier 4 expectations.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep dashboard as a presentation layer over outputs/.
- Do not modify notebook/model outputs during UI polish.
- Add future bugs to this change history before applying repeated fixes.

### 2026-05-10 14:04 — Final dashboard edit review

**Changed**
- Reviewed Executive Overview, Balanced Scorecard, Fleet Performance, Weather & Demand, Predictive AI, ROI Recommendations, Data Evidence, and Presentation Mode behavior.
- Updated `app.py` with small final polish only.
- Replaced remaining `use_container_width` table/image calls with safer stretch-width helpers where supported.
- Improved a small section label for the maintenance-priority vehicle review area.
- Improved the model metrics chart title for presentation clarity.

**Why**
- Remove small presentation and compatibility issues without changing dashboard scope or underlying analytics logic.

**Error / Symptom**
- Streamlit review runs showed compatibility warnings encouraging `width="stretch"` instead of `use_container_width` for some rendered elements.

**Root Cause**
- Some final table and image rendering calls still used older width arguments.

**Fix**
- Added small rendering helpers and switched the remaining affected dataframe and image calls to the newer stretch-width path with safe fallback behavior.

**Prevention Rule**
- Keep final edits limited to clarity, formatting, and small bug fixes.
- Prefer shared render helpers for future Streamlit compatibility adjustments.
- Preserve notebook and outputs while polishing the dashboard layer.

### 2026-05-10 14:17 — Phase 3.1 evidence cleanup and AI assistant patch

**Changed**
- Hid PNG image rendering from Data Evidence.
- Kept codex_phase3_report.md as the main evidence artifact.
- Added AI Board Assistant to Predictive AI page.
- Added model workflow explanation.
- Improved responsive layout behavior.

**Why**
- Keep dashboard presentation clean.
- Make trained model outputs easier to explain during presentation.
- Support simple board-level Q&A without external APIs.
- Improve usability on laptop and mobile.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep evidence page presentation-focused.
- Do not render noisy PNG artifacts unless explicitly requested.
- Keep AI assistant deterministic and grounded in exported outputs.

### 2026-05-10 14:31 — Phase 3.3 Global AI Copilot UI

**Changed**
- Converted AI Board Assistant into a global local copilot / chat bubble pattern.
- Added free-typed question support with keyword intent matching.
- Added suggested question chips/buttons.
- Preserved deterministic local answers based on exported outputs.
- Updated README.

**Why**
- Make the assistant feel more natural and impressive during presentation.
- Allow users to type board-level questions instead of only selecting from a dropdown.
- Keep the system local, transparent, and non-hallucinating.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep assistant local and deterministic.
- Do not add external API dependencies unless explicitly requested.
- Do not present keyword-based answers as a real LLM.

### 2026-05-10 14:41 — Phase 3.4 AI Copilot UX refinement

**Changed**
- Reduced suggested AI Copilot questions to four high-value prompts.
- Improved free-typed keyword and intent matching.
- Added examples for natural typed questions.
- Improved fallback guidance.
- Updated README.

**Why**
- Make the assistant feel more natural and less like a dropdown.
- Keep the demo clean while preserving flexible Q&A.
- Avoid external API/LLM dependencies.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep assistant deterministic and grounded.
- Prefer flexible local matching over exact hardcoded question matching.

### 2026-05-10 14:48 - Phase 4 Overleaf report and GitHub cleanup

**Changed**
- Created Overleaf-ready LaTeX report package.
- Created screenshot placeholder structure.
- Created AI usage log.
- Created or updated GitHub README.
- Created or updated `.gitignore`.
- Created GitHub readiness checklist.

**Why**
- Prepare the completed dashboard and analytics work for submission, Overleaf compilation, and GitHub upload.

**Error / Symptom**
- None.

**Root Cause**
- Not applicable.

**Fix**
- Not applicable.

**Prevention Rule**
- Keep source code, report assets, screenshots, and evidence organized separately.
- Do not commit secrets, cache files, virtual environments, or temporary build outputs.
