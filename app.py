import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="SaigonFlow Executive Dashboard",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
GUIDANCE_DIR = BASE_DIR / "project_guidance"

EXPECTED_CSVS = {
    "master_dataset": "master_dataset.csv",
    "vehicle_utilization": "vehicle_utilization.csv",
    "top10_vehicle_revenue": "top10_vehicle_revenue.csv",
    "bottom10_vehicle_revenue": "bottom10_vehicle_revenue.csv",
    "rain_vs_clear_analysis": "rain_vs_clear_analysis.csv",
    "churn_model_dataset": "churn_model_dataset.csv",
    "vehicle_model_dataset": "vehicle_model_dataset.csv",
    "churn_risk_predictions": "churn_risk_predictions.csv",
    "vehicle_risk_predictions": "vehicle_risk_predictions.csv",
    "balanced_scorecard": "balanced_scorecard.csv",
    "model_metrics_summary": "model_metrics_summary.csv",
}

COLOR_MAP = {
    "cyan": "#22d3ee",
    "teal": "#14b8a6",
    "amber": "#f59e0b",
    "red": "#ef4444",
    "green": "#22c55e",
    "purple": "#8b5cf6",
    "muted": "#9fb6c7",
}

RISK_COLOR_MAP = {
    "high": "#ef4444",
    "critical": "#ef4444",
    "medium": "#f59e0b",
    "watch": "#f59e0b",
    "low": "#22c55e",
    "healthy": "#14b8a6",
}


def normalize_name(name):
    if name is None:
        return ""
    return "".join(ch for ch in str(name).lower() if ch not in {" ", "_", "-"})


def find_col(df, candidates):
    if df is None or df.empty:
        return None
    normalized = {normalize_name(col): col for col in df.columns}
    for candidate in candidates:
        match = normalized.get(normalize_name(candidate))
        if match:
            return match
    return None


@st.cache_data(show_spinner=False)
def load_csv_safely(filename):
    path = OUTPUTS_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_text_safely(filename):
    path = OUTPUTS_DIR / filename
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def list_pngs():
    return sorted(OUTPUTS_DIR.glob("*.png"))


def format_vnd(value):
    if value is None or pd.isna(value):
        return "N/A"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B VND"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M VND"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K VND"
    return f"{int(round(value)):,} VND"


def format_pct(value):
    if value is None or pd.isna(value):
        return "N/A"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if 0 <= value <= 1:
        value *= 100
    return f"{value:.1f}%"


def safe_sum(df, candidates):
    if df is None or df.empty:
        return None
    col = find_col(df, candidates)
    if not col:
        return None
    series = pd.to_numeric(df[col], errors="coerce")
    if series.dropna().empty:
        return None
    return float(series.sum())


def safe_mean(df, candidates):
    if df is None or df.empty:
        return None
    col = find_col(df, candidates)
    if not col:
        return None
    series = pd.to_numeric(df[col], errors="coerce")
    if series.dropna().empty:
        return None
    return float(series.mean())


def safe_count_rows(df):
    if df is None or df.empty:
        return 0
    return int(len(df))


def safe_nunique(df, candidates):
    if df is None or df.empty:
        return None
    col = find_col(df, candidates)
    if not col:
        return None
    return int(df[col].nunique())


def safe_ratio(numerator, denominator):
    if numerator is None or denominator in (None, 0):
        return None
    try:
        return float(numerator) / float(denominator)
    except Exception:
        return None


def numeric_series(df, candidates):
    col = find_col(df, candidates)
    if not col:
        return None
    series = pd.to_numeric(df[col], errors="coerce")
    if series.dropna().empty:
        return None
    return series


@st.cache_data(show_spinner=False)
def prepare_master_dataset(df):
    if df.empty:
        return df.copy()
    prepared = df.copy()
    ts_col = find_col(prepared, ["Timestamp"])
    hour_col = find_col(prepared, ["Hour"])
    weekend_col = find_col(prepared, ["Is_Weekend"])
    peak_col = find_col(prepared, ["Is_Peak_Hour"])

    if ts_col:
        ts = pd.to_datetime(prepared[ts_col], errors="coerce")
        prepared["_parsed_timestamp"] = ts
    else:
        prepared["_parsed_timestamp"] = pd.NaT

    if hour_col:
        prepared["_hour"] = pd.to_numeric(prepared[hour_col], errors="coerce")
    elif "_parsed_timestamp" in prepared:
        prepared["_hour"] = prepared["_parsed_timestamp"].dt.hour
    else:
        prepared["_hour"] = np.nan

    if weekend_col:
        weekend_values = pd.to_numeric(prepared[weekend_col], errors="coerce")
        prepared["_weekend_label"] = np.where(weekend_values == 1, "Weekend", "Weekday")
        prepared["_is_weekend_num"] = weekend_values
    else:
        prepared["_weekend_label"] = "Unknown"
        prepared["_is_weekend_num"] = np.nan

    if peak_col:
        peak_values = pd.to_numeric(prepared[peak_col], errors="coerce")
        prepared["_peak_label"] = np.where(peak_values == 1, "Peak", "Non-Peak")
        prepared["_is_peak_num"] = peak_values
    elif "_hour" in prepared:
        peak_mask = prepared["_hour"].between(7, 9) | prepared["_hour"].between(17, 19)
        prepared["_peak_label"] = np.where(peak_mask, "Peak", "Non-Peak")
        prepared["_is_peak_num"] = np.where(peak_mask, 1, 0)
    else:
        prepared["_peak_label"] = "Unknown"
        prepared["_is_peak_num"] = np.nan

    return prepared


def inject_global_css():
    st.markdown(
        """
        <style>
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

        .stApp {
          background:
            radial-gradient(circle at top right, rgba(34, 211, 238, 0.18), transparent 25%),
            radial-gradient(circle at left top, rgba(20, 184, 166, 0.16), transparent 20%),
            linear-gradient(180deg, #06111f 0%, #081521 45%, #06111f 100%);
          color: var(--text);
        }

        .block-container {
          padding-top: 1.8rem;
          padding-bottom: 2.5rem;
        }

        [data-testid="stSidebar"] {
          background: linear-gradient(180deg, rgba(9, 24, 39, 0.98), rgba(6, 17, 31, 0.98));
          border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
          color: var(--text);
        }

        [data-baseweb="select"] > div,
        [data-baseweb="radio"] > div,
        div[data-testid="stToggle"] label {
          color: var(--text);
        }

        .sf-hero {
          position: relative;
          overflow: hidden;
          background:
            linear-gradient(135deg, rgba(34, 211, 238, 0.20), rgba(139, 92, 246, 0.15)),
            rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.18);
          border-radius: 30px;
          padding: 30px 32px;
          backdrop-filter: blur(18px);
          box-shadow: 0 22px 60px rgba(0, 0, 0, 0.24);
          margin-bottom: 1.25rem;
        }

        .sf-hero::before {
          content: "";
          position: absolute;
          inset: auto auto -20% -5%;
          width: 220px;
          height: 220px;
          background: radial-gradient(circle, rgba(20, 184, 166, 0.24), transparent 70%);
          pointer-events: none;
        }

        .sf-kicker {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          padding: 0.38rem 0.82rem;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.12);
          color: var(--cyan);
          font-size: 0.78rem;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          margin-bottom: 1rem;
        }

        .sf-hero h1 {
          margin: 0;
          font-size: clamp(1.8rem, 5vw, 2.35rem);
          line-height: 1.05;
          letter-spacing: -0.04em;
        }

        .sf-hero p {
          margin: 0.75rem 0 0 0;
          max-width: 800px;
          color: var(--text-muted);
          line-height: 1.65;
          font-size: 1rem;
        }

        .sf-section {
          margin: 1.05rem 0 0.9rem 0;
        }

        .sf-section h2 {
          margin: 0;
          color: var(--text);
          font-size: 1.45rem;
          letter-spacing: -0.025em;
        }

        .sf-section p {
          margin: 0.35rem 0 0 0;
          color: var(--text-muted);
          line-height: 1.55;
        }

        .sf-panel,
        .sf-metric-card,
        .sf-insight,
        .sf-rec-card,
        .sf-scorecard,
        .sf-summary-box {
          background: rgba(255, 255, 255, 0.07);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 22px;
          backdrop-filter: blur(14px);
          box-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
        }

        .sf-metric-card {
          padding: 1rem 1rem 0.9rem 1rem;
          min-height: 136px;
          border-top: 3px solid var(--tone, var(--cyan));
        }

        .sf-metric-label {
          color: var(--text-muted);
          font-size: 0.78rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          margin-bottom: 0.7rem;
        }

        .sf-metric-value {
          color: var(--text);
          font-size: 1.72rem;
          font-weight: 700;
          line-height: 1.05;
        }

        .sf-metric-delta {
          margin-top: 0.65rem;
          color: var(--tone, var(--cyan));
          font-size: 0.9rem;
          line-height: 1.4;
        }

        .sf-summary-box {
          padding: 1rem 1.1rem;
          border-left: 4px solid var(--cyan);
          margin: 1rem 0 1.2rem 0;
        }

        .sf-summary-box strong {
          display: block;
          margin-bottom: 0.45rem;
          font-size: 0.95rem;
          color: var(--text);
        }

        .sf-summary-box span {
          color: var(--text-muted);
          line-height: 1.6;
        }

        .sf-panel {
          padding: 1rem;
          margin-bottom: 1rem;
        }

        .sf-scorecard {
          padding: 1rem;
          border-top: 3px solid var(--tone, var(--cyan));
          min-height: 260px;
        }

        .sf-card-title {
          color: var(--text);
          font-size: 1.05rem;
          font-weight: 700;
          margin-bottom: 0.6rem;
        }

        .sf-card-body {
          color: var(--text-muted);
          font-size: 0.95rem;
          line-height: 1.55;
        }

        .sf-card-kpi {
          color: var(--text);
          font-size: 1.5rem;
          font-weight: 700;
          margin: 0.45rem 0;
        }

        .sf-label {
          color: var(--text-muted);
          font-size: 0.74rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          margin-top: 0.6rem;
        }

        .sf-badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          padding: 0.26rem 0.72rem;
          font-size: 0.76rem;
          font-weight: 600;
          border: 1px solid rgba(255, 255, 255, 0.12);
          background: rgba(255, 255, 255, 0.08);
          color: var(--text);
        }

        .sf-insight,
        .sf-rec-card {
          padding: 1rem;
          border-left: 4px solid var(--tone, var(--cyan));
          height: 100%;
        }

        .sf-insight-title,
        .sf-rec-title {
          color: var(--text);
          font-size: 1.02rem;
          font-weight: 700;
          margin-bottom: 0.6rem;
        }

        .sf-insight-body,
        .sf-rec-body {
          color: var(--text-muted);
          font-size: 0.95rem;
          line-height: 1.62;
        }

        .sf-status-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 0.8rem;
          margin-top: 0.85rem;
        }

        .sf-status-item {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.10);
          border-radius: 16px;
          padding: 0.9rem;
        }

        .sf-status-label {
          color: var(--text-muted);
          font-size: 0.74rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }

        .sf-status-value {
          color: var(--text);
          font-size: 1.2rem;
          font-weight: 700;
          margin-top: 0.35rem;
        }

        .sf-note {
          color: var(--text-muted);
          font-size: 0.85rem;
          margin-top: 0.35rem;
        }

        .sf-flow-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 0.8rem;
          margin-top: 0.8rem;
        }

        .sf-flow-step {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 18px;
          padding: 0.95rem;
        }

        .sf-flow-step strong {
          display: block;
          color: var(--text);
          margin-bottom: 0.35rem;
        }

        .sf-flow-step span {
          color: var(--text-muted);
          font-size: 0.92rem;
          line-height: 1.55;
        }

        .sf-copilot-note {
          display: flex;
          justify-content: flex-end;
          margin: 0.15rem 0 0.8rem 0;
        }

        .sf-copilot-hint {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          padding: 0.5rem 0.8rem;
          border-radius: 999px;
          background: rgba(34, 211, 238, 0.10);
          border: 1px solid rgba(34, 211, 238, 0.28);
          color: var(--text);
          font-size: 0.84rem;
        }

        .sf-copilot-panel {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 18px;
          padding: 0.9rem;
          margin-bottom: 0.8rem;
        }

        .sf-copilot-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
          gap: 0.55rem;
          margin: 0.75rem 0;
        }

        .sf-chat-hint {
          color: var(--text-muted);
          font-size: 0.86rem;
          line-height: 1.5;
        }

        .stDataFrame, div[data-testid="stTable"], div[data-testid="stExpander"] {
          background: rgba(255, 255, 255, 0.04);
          border-radius: 18px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          overflow: hidden;
        }

        [data-testid="stSidebar"] .block-container {
          padding-bottom: 1.25rem;
        }

        div[data-testid="stAlert"] {
          border-radius: 16px;
        }

        @media (hover: hover) {
          .sf-metric-card,
          .sf-insight,
          .sf-rec-card,
          .sf-scorecard,
          .sf-panel {
            transition: transform 180ms ease, opacity 180ms ease;
          }

          .sf-metric-card:hover,
          .sf-insight:hover,
          .sf-rec-card:hover,
          .sf-scorecard:hover,
          .sf-panel:hover {
            transform: translateY(-2px);
          }
        }

        @media (max-width: 900px) {
          .sf-hero {
            padding: 24px;
          }
        }

        @media (max-width: 768px) {
          .block-container {
            padding-top: 1rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
          }

          .sf-hero {
            padding: 18px;
            border-radius: 22px;
          }

          .sf-metric-card,
          .sf-insight,
          .sf-rec-card,
          .sf-scorecard,
          .sf-panel,
          .sf-summary-box {
            padding: 0.9rem;
            border-radius: 18px;
          }

          .sf-status-grid,
          .sf-flow-grid,
          .sf-copilot-grid {
            grid-template-columns: 1fr;
          }

          .sf-metric-value {
            font-size: 1.45rem;
          }
        }

        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="sf-section">
          <h2>{title}</h2>
          {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, delta=None, tone="cyan"):
    st.markdown(
        f"""
        <div class="sf-metric-card" style="--tone: {COLOR_MAP.get(tone, COLOR_MAP['cyan'])};">
          <div class="sf-metric-label">{label}</div>
          <div class="sf-metric-value">{value}</div>
          <div class="sf-metric-delta">{delta or "&nbsp;"}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(title, body, tone="cyan"):
    st.markdown(
        f"""
        <div class="sf-insight" style="--tone: {COLOR_MAP.get(tone, COLOR_MAP['cyan'])};">
          <div class="sf-insight-title">{title}</div>
          <div class="sf-insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(label, tone="cyan"):
    color = COLOR_MAP.get(tone, COLOR_MAP["cyan"])
    return (
        "<span class='sf-badge' "
        f"style='border-color:{color}; color:{color}; background:rgba(255,255,255,0.06);'>{label}</span>"
    )


def scorecard_box(title, key_metric, current_value, target_value, interpretation, status_label, tone):
    st.markdown(
        f"""
        <div class="sf-scorecard" style="--tone: {COLOR_MAP.get(tone, COLOR_MAP['cyan'])};">
          <div class="sf-card-title">{title}</div>
          <div>{status_badge(status_label, tone)}</div>
          <div class="sf-label">Key Metric</div>
          <div class="sf-card-kpi">{key_metric}</div>
          <div class="sf-label">Current Value</div>
          <div class="sf-card-body">{current_value}</div>
          <div class="sf-label">Target</div>
          <div class="sf-card-body">{target_value}</div>
          <div class="sf-label">Interpretation</div>
          <div class="sf-card-body">{interpretation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_fig(fig, title=None):
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#edf7ff"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(6,17,31,0.55)",
            bordercolor="rgba(255,255,255,0.10)",
            borderwidth=1,
        ),
        margin=dict(t=58 if title else 20, l=20, r=20, b=20),
        hoverlabel=dict(bgcolor="#091827", font_color="#edf7ff"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)")
    return fig


def render_plotly(fig, key=None):
    try:
        st.plotly_chart(fig, width="stretch", key=key)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, key=key)


def render_dataframe(df, key=None):
    try:
        st.dataframe(df, width="stretch")
    except TypeError:
        st.dataframe(df, use_container_width=True)


def render_image(image, caption=None):
    try:
        st.image(image, caption=caption, width="stretch")
    except TypeError:
        st.image(image, caption=caption, use_container_width=True)


def render_file_status(dataframes, pngs):
    loaded = sum(1 for df in dataframes.values() if not df.empty)
    missing = len(dataframes) - loaded
    st.markdown(
        f"""
        <div class="sf-panel">
          <div>{status_badge('Output Status', 'cyan')}</div>
          <div class="sf-status-grid">
            <div class="sf-status-item">
              <div class="sf-status-label">CSV Loaded</div>
              <div class="sf-status-value">{loaded}</div>
            </div>
            <div class="sf-status-item">
              <div class="sf-status-label">CSV Missing</div>
              <div class="sf-status-value">{missing}</div>
            </div>
            <div class="sf-status-item">
              <div class="sf-status-label">PNG Charts</div>
              <div class="sf-status-value">{len(pngs)}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_master_filters(df, mode_value, weather_value):
    if df.empty:
        return df.copy()
    filtered = df.copy()
    mode_col = find_col(filtered, ["Mode"])
    weather_col = find_col(filtered, ["Weather_Condition"])
    if mode_value != "All" and mode_col:
        filtered = filtered[filtered[mode_col].astype(str) == mode_value]
    if weather_value != "All" and weather_col:
        filtered = filtered[filtered[weather_col].astype(str) == weather_value]
    return filtered


def apply_filter_if_exists(df, value, candidates):
    if df.empty or value == "All":
        return df.copy()
    col = find_col(df, candidates)
    if not col:
        return df.copy()
    return df[df[col].astype(str) == value].copy()


def risk_priority_value(value):
    text = str(value).strip().lower()
    if text == "critical":
        return 0
    if text in {"watch", "medium"}:
        return 1
    if text in {"healthy", "low"}:
        return 2
    if text == "high":
        return 0
    return 3


def make_level_counts(df, candidates):
    if df.empty:
        return pd.DataFrame()
    col = find_col(df, candidates)
    if not col:
        return pd.DataFrame()
    counts = df[col].astype(str).fillna("Unknown").value_counts().rename_axis("Level").reset_index(name="Count")
    counts["Priority"] = counts["Level"].map(risk_priority_value)
    return counts.sort_values(["Priority", "Level"]).drop(columns="Priority")


def build_metric_row(label, value, tone="cyan", delta=None):
    return {"label": label, "value": value, "tone": tone, "delta": delta}


def format_float(value, digits=1):
    if value is None or pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "N/A"


def parse_first_number(text):
    if text is None or pd.isna(text):
        return None
    digits = []
    current = ""
    for ch in str(text):
        if ch.isdigit() or ch in {".", ","}:
            current += ch
        elif current:
            digits.append(current)
            current = ""
    if current:
        digits.append(current)
    if not digits:
        return None
    try:
        return float(digits[0].replace(",", ""))
    except Exception:
        return None


def scorecard_status(name, summary_metrics):
    name_n = normalize_name(name)
    if "financial" in name_n:
        ebike_share = summary_metrics.get("ebike_revenue_share")
        if ebike_share is not None and ebike_share > 0.65:
            return "Concentrated revenue", "amber"
        return "On track", "teal"
    if "customer" in name_n:
        churn_rate = summary_metrics.get("churn_rate")
        if churn_rate is not None and churn_rate >= 0.10:
            return "Needs retention action", "red"
        return "On track", "green"
    if "internal" in name_n or "fleet" in name_n:
        critical_count = summary_metrics.get("critical_battery_vehicles")
        if critical_count is not None and critical_count > 0:
            return "Fleet attention required", "amber"
        return "Healthy", "green"
    return "AI active", "purple"


def make_download_button(filename):
    path = OUTPUTS_DIR / filename
    if path.exists():
        st.download_button(
            label=f"Download {filename}",
            data=path.read_bytes(),
            file_name=filename,
            mime="text/csv",
            key=f"download_{filename}",
        )


def render_workflow_panel():
    st.markdown(
        """
        <div class="sf-panel">
          <div class="sf-card-title">How the trained predictive workflow works</div>
          <div class="sf-card-body">The dashboard does not retrain models. It displays the already-generated trained model outputs.</div>
          <div class="sf-flow-grid">
            <div class="sf-flow-step"><strong>1. Data Integration</strong><span>Users, Trips, and Vehicles are joined into a Single Source of Truth.</span></div>
            <div class="sf-flow-step"><strong>2. Feature Engineering</strong><span>The notebook creates user behavior features and vehicle utilization/risk features.</span></div>
            <div class="sf-flow-step"><strong>3. Model Training</strong><span>The notebook trains classification models and selects the best model based on risk-detection metrics.</span></div>
            <div class="sf-flow-step"><strong>4. Prediction Output</strong><span>The dashboard reads `churn_risk_predictions.csv` and `vehicle_risk_predictions.csv`.</span></div>
            <div class="sf-flow-step"><strong>5. Business Action</strong><span>Managers use risk levels to trigger retention, charging, maintenance, and redistribution actions.</span></div>
          </div>
          <div class="sf-note">Data → Features → Model → Risk Scores → Business Action</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def detect_assistant_intent(question: str) -> str:
    q = (question or "").strip().lower()
    if not q:
        return "help"

    replacements = {
        "what's": "what is",
        "whats": "what is",
        "pre-position": "pre position",
        "30-second": "30 second",
        "30-seconds": "30 seconds",
    }
    for old, new in replacements.items():
        q = q.replace(old, new)

    cleaned = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in q)
    normalized = " ".join(cleaned.split())

    def has_phrase(phrase):
        return phrase in normalized

    def has_any(words):
        return any(word in normalized for word in words)

    def has_all(words):
        return all(word in normalized for word in words)

    if (
        has_any(["pitch", "summary"])
        or has_all(["executive", "pitch"])
        or has_all(["30", "second"])
        or has_all(["30", "seconds"])
        or has_all(["thirty", "second"])
        or has_phrase("what should i say")
    ):
        return "executive_pitch"

    if has_any(["limitation", "limitations", "limits", "simulated", "production", "caveat"]) or has_phrase("academic honesty") or has_phrase("future label"):
        return "limitations"

    if has_phrase("balanced scorecard") or has_any(["scorecard", "kpi", "target", "perspective"]):
        return "scorecard"

    if has_any(["rain", "weather", "clear", "storm"]) or (has_any(["demand"]) and has_any(["rain", "weather", "clear"])):
        return "weather"

    if (
        has_any(["route", "routes", "station", "rebalance", "rebalancing", "supply"])
        or has_phrase("pre position")
        or has_phrase("battery supply")
        or has_phrase("where should")
    ):
        return "route"

    if has_any(["roi", "return", "financial", "money", "revenue", "business value"]) and has_any(["battery", "failure"]):
        return "battery_roi"

    if has_phrase("vehicle risk") or has_phrase("fleet risk") or has_phrase("vehicle model"):
        return "vehicle_model"

    if has_any(["maintenance", "battery", "failure", "charging", "fleet risk"]) and not has_any(["user", "customer", "churn"]):
        return "vehicle_priority"

    if (has_any(["churn", "leave"]) and not has_any(["vehicle", "battery", "fleet"])) or has_phrase("churn model"):
        return "churn_model"

    if has_phrase("customer risk") or has_phrase("user risk") or has_any(["retention", "users"]) or has_phrase("which users"):
        return "churn_target"

    if has_any(["presentation", "demo", "talk", "say", "script", "speaking"]):
        return "presentation"

    return "help"


def answer_board_question(question, assistant_data):
    q = (question or "").strip().lower()
    if not q:
        return "Ask a board-level question about churn risk, vehicle risk, battery rebalancing, ROI, or model limitations."

    summary = assistant_data.get("summary_metrics", {})
    churn_df = assistant_data.get("churn_df", pd.DataFrame())
    vehicle_df = assistant_data.get("vehicle_df", pd.DataFrame())
    rain_df = assistant_data.get("rain_df", pd.DataFrame())
    master_df = assistant_data.get("master_df", pd.DataFrame())

    high_users = summary.get("high_risk_users")
    high_vehicles = summary.get("high_risk_vehicles")
    watch_vehicles = summary.get("watch_vehicles")
    healthy_vehicles = summary.get("healthy_vehicles")
    churn_rate = summary.get("churn_rate")
    intent = detect_assistant_intent(q)

    if intent == "executive_pitch":
        return (
            "SaigonFlow should operationalize the Unified Flow Platform as a decision engine. "
            "The dashboard shows where revenue comes from, how weather and peak hours affect demand, "
            "and which users or vehicles need intervention. Predictive AI helps managers act before "
            "churn or vehicle failure harms revenue, creating measurable ROI through retention and fleet reliability."
        )

    if intent == "presentation":
        return (
            "Our dashboard turns SaigonFlow's fragmented trip, user, and vehicle data into a single decision view. "
            "The descriptive analytics show revenue concentration, weather-sensitive demand, and fleet risk. "
            "The predictive outputs identify churn-prone users and vehicles needing charging or maintenance. "
            "This supports ROI by improving retention, fleet uptime, and operational decision-making."
        )

    if intent == "churn_model":
        count_text = (
            f"The exported predictions currently flag {high_users} high-risk users. "
            if high_users is not None
            else "That exact high-risk count is not available in the exported dashboard files. "
        )
        return (
            "The churn model scores users by churn probability and groups them into risk levels using "
            "`churn_risk_predictions.csv`. "
            + count_text +
            "High-risk users should receive retention offers or proactive service recovery first."
        )

    if intent == "vehicle_model":
        parts = []
        if high_vehicles is not None:
            parts.append(f"{high_vehicles} critical vehicles")
        if watch_vehicles is not None:
            parts.append(f"{watch_vehicles} watch vehicles")
        if healthy_vehicles is not None:
            parts.append(f"{healthy_vehicles} healthy vehicles")
        count_text = ", ".join(parts) if parts else "That exact vehicle risk breakdown is not available in the exported dashboard files."
        return (
            "The vehicle risk model prioritizes vehicles for charging or maintenance using "
            "`vehicle_risk_predictions.csv`. It uses battery level, maintenance age, utilization, "
            "and revenue contribution where available. Current exported counts show "
            f"{count_text}."
        )

    if intent == "battery_roi":
        return (
            "Low-battery or unavailable vehicles create failed trips, reduce fleet uptime, and weaken customer trust. "
            "Predictive maintenance protects high-revenue vehicles first and reduces churn risk caused by service failures."
        )

    if intent == "churn_target":
        action_col = find_col(churn_df, ["Recommended_Action"])
        action_text = "retention offer plus proactive service recovery" if action_col else "proactive retention treatment"
        return (
            "SaigonFlow should target the highest-risk churn users first, sorted by predicted churn probability in the "
            "top-20 high-risk table. The recommended action is usually "
            f"{action_text}."
        )

    if intent == "vehicle_priority":
        return (
            "Managers should prioritize Critical vehicles first, then Watch vehicles. Within those groups, sort by "
            "Predicted_Action_Probability, lower battery level, and higher revenue contribution. "
            "The immediate action is charging or maintenance before the next deployment window."
        )

    if intent == "weather":
        trip_col = find_col(rain_df, ["Trip_Count"])
        category_col = find_col(rain_df, ["Rain_Category"])
        if not rain_df.empty and trip_col and category_col:
            clear_val = rain_df.loc[rain_df[category_col].astype(str).str.lower() == "clear", trip_col]
            rain_val = rain_df.loc[rain_df[category_col].astype(str).str.lower() == "rain", trip_col]
            detail = ""
            if not clear_val.empty and not rain_val.empty:
                detail = f" In the exported weather analysis, clear trips are {int(clear_val.iloc[0]):,} and rain trips are {int(rain_val.iloc[0]):,}."
            return (
                "Rain affects SaigonFlow demand and supports weather-responsive pricing or targeted shuttle incentives." + detail
            )
        return "Rain-sensitive demand is visible in the exported weather analysis. That exact value is not available in the exported dashboard files."

    if intent == "scorecard":
        return (
            "The Balanced Scorecard connects AI to four management objectives: Financial protects revenue, "
            "Customer reduces churn, Internal Process or Fleet improves uptime, and Learning & Growth or AI "
            "deploys predictive alerts and monitoring."
        )

    if intent == "route":
        station_col = find_col(master_df, ["Start_Station"])
        mode_col = find_col(master_df, ["Mode"])
        if station_col and not master_df.empty:
            temp = master_df.copy()
            if mode_col:
                temp = temp[temp[mode_col].astype(str) == "E-Bike"]
            top_stations = temp[station_col].astype(str).value_counts().head(3).index.tolist()
            if top_stations:
                joined = ", ".join(top_stations)
                return (
                    "Battery supply and pre-positioning should focus on the busiest visible launch points first. "
                    f"In the current filtered demand view, the top start stations are {joined}. "
                    "Management action: route charged vehicles toward these stations before peak windows and rebalance from lower-demand areas."
                )
        return (
            "Use the busiest stations and peak-hour demand view to decide where more battery supply or vehicle rebalancing is needed. "
            "That exact ranked route list is not available in the exported dashboard files."
        )

    if intent == "limitations":
        churn_text = (
            f"The churn rate shown in the filtered dashboard view is {format_pct(churn_rate)}. "
            if churn_rate is not None else ""
        )
        return (
            f"{churn_text}The churn model depends on historical generated data. "
            "The vehicle risk model uses a simulated operational target because no true future failure label exists "
            "in the generated dataset. A production system would require live telemetry, future failure outcomes, "
            "drift monitoring, and human oversight."
        )

    return (
        "I can answer board-level questions about churn risk, vehicle risk, route rebalancing, rain demand, ROI, Balanced Scorecard, model limitations, and presentation talking points. Try asking: 'What is the 30-second executive pitch?' or 'Which routes need more battery supply?'"
    )


def reset_assistant_history():
    st.session_state.assistant_messages = [
        {
            "role": "assistant",
            "content": "Hi, I can help explain SaigonFlow's churn risk, vehicle risk, battery rebalancing, ROI, and model limitations. Ask me a board-level question.",
        }
    ]
    st.session_state.assistant_last_question = ""


def ensure_assistant_state():
    if "assistant_messages" not in st.session_state:
        reset_assistant_history()
    if "assistant_last_question" not in st.session_state:
        st.session_state.assistant_last_question = ""


def handle_assistant_prompt(question, assistant_data):
    question = (question or "").strip()
    if not question:
        return
    st.session_state.assistant_messages.append({"role": "user", "content": question})
    st.session_state.assistant_messages.append(
        {"role": "assistant", "content": answer_board_question(question, assistant_data)}
    )
    st.session_state.assistant_last_question = question


def render_ai_copilot(assistant_data, presentation_mode=False):
    ensure_assistant_state()
    suggested_questions = [
        "What is the 30-second executive pitch?",
        "What did the churn model predict?",
        "Which routes need more battery supply?",
        "What are the model limitations?",
    ]

    st.markdown(
        """
        <div class="sf-copilot-note">
          <div class="sf-copilot-hint">💬 Global AI Board Assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    right_col = st.columns([4, 1.3])[1]
    with right_col:
        # Streamlit does not provide a native fixed floating widget. This uses st.popover as a safe local copilot pattern.
        with st.popover("💬 AI Board Assistant"):
            st.markdown(
                """
                <div class="sf-copilot-panel">
                  <div class="sf-card-title">AI Board Assistant</div>
                  <div class="sf-chat-hint">Ask board-level questions about churn, vehicle risk, routes, ROI, and model limits.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if not presentation_mode:
                st.caption("This is a deterministic local assistant based on exported model outputs. It is not an external LLM.")

            st.markdown("**Suggested questions**")
            cols = st.columns(2)
            for idx, question in enumerate(suggested_questions):
                with cols[idx % 2]:
                    if st.button(question, key=f"copilot_q_{idx}", use_container_width=True):
                        handle_assistant_prompt(question, assistant_data)
            st.caption("Or type your own question about vehicle risk, rain demand, ROI, route rebalancing, or presentation talking points.")
            st.caption("Try typing: 'What's the 30 seconds executive pitch?', 'Where should vehicles be pre-positioned?', or 'Explain model limitations.'")

            for message in st.session_state.assistant_messages[-8:]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            user_prompt = st.chat_input("Ask about churn risk, vehicle risk, routes, ROI, or presentation talking points...", key="global_copilot_input")
            if user_prompt:
                handle_assistant_prompt(user_prompt, assistant_data)
                st.rerun()

            if st.button("Clear chat", key="copilot_clear", use_container_width=True):
                reset_assistant_history()
                st.rerun()


inject_global_css()

data = {key: load_csv_safely(filename) for key, filename in EXPECTED_CSVS.items()}
codex_report = load_text_safely("codex_phase3_report.md")
pngs = list_pngs()

master_raw = data["master_dataset"]
master_dataset = prepare_master_dataset(master_raw)

with st.sidebar:
    st.markdown("## SaigonFlow")
    st.markdown("### Phase 3 Command Center")
    st.caption("Unified Flow Platform for executive decision support")

    presentation_mode = st.toggle("Presentation Mode", value=True, help="Prioritize executive summaries and minimize raw evidence by default.")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Balanced Scorecard",
            "Fleet Performance",
            "Weather & Demand",
            "Predictive AI",
            "ROI Recommendations",
            "Data Evidence",
        ],
    )

    st.divider()
    st.markdown("#### Global Filters")

    mode_options = ["All"]
    weather_options = ["All"]
    vehicle_type_options = ["All"]
    customer_risk_options = ["All"]
    vehicle_risk_options = ["All"]

    mode_col = find_col(master_dataset, ["Mode"])
    weather_col = find_col(master_dataset, ["Weather_Condition"])
    if mode_col and not master_dataset.empty:
        mode_options += sorted(master_dataset[mode_col].dropna().astype(str).unique().tolist())
    if weather_col and not master_dataset.empty:
        weather_options += sorted(master_dataset[weather_col].dropna().astype(str).unique().tolist())

    for vehicle_df in [data["vehicle_utilization"], data["vehicle_risk_predictions"], data["top10_vehicle_revenue"], data["bottom10_vehicle_revenue"]]:
        type_col = find_col(vehicle_df, ["Type"])
        if type_col and not vehicle_df.empty:
            vehicle_type_options += vehicle_df[type_col].dropna().astype(str).unique().tolist()

    churn_risk_col_raw = find_col(data["churn_risk_predictions"], ["Churn_Risk_Level"])
    if churn_risk_col_raw and not data["churn_risk_predictions"].empty:
        customer_risk_options += sorted(data["churn_risk_predictions"][churn_risk_col_raw].dropna().astype(str).unique().tolist())

    vehicle_risk_col_raw = find_col(data["vehicle_risk_predictions"], ["Maintenance_Risk_Level"])
    if vehicle_risk_col_raw and not data["vehicle_risk_predictions"].empty:
        vehicle_risk_options += sorted(data["vehicle_risk_predictions"][vehicle_risk_col_raw].dropna().astype(str).unique().tolist())

    mode_filter = st.selectbox("Mode", sorted(set(mode_options)))
    weather_filter = st.selectbox("Weather", sorted(set(weather_options)))
    vehicle_type_filter = st.selectbox("Vehicle Type", sorted(set(vehicle_type_options)))
    customer_risk_filter = st.selectbox("Customer Risk", sorted(set(customer_risk_options)))
    vehicle_risk_filter = st.selectbox("Vehicle Risk", sorted(set(vehicle_risk_options)))

    st.caption("Filters are applied where matching columns exist.")
    st.divider()
    st.caption(f"CSV files loaded: {sum(1 for df in data.values() if not df.empty)}/{len(data)}")
    st.caption(f"PNG charts found: {len(pngs)}")
    st.caption(f"Last run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

master_filtered = apply_master_filters(master_dataset, mode_filter, weather_filter)
vehicle_util_filtered = apply_filter_if_exists(data["vehicle_utilization"], vehicle_type_filter, ["Type"])
top10_filtered = apply_filter_if_exists(data["top10_vehicle_revenue"], vehicle_type_filter, ["Type"])
bottom10_filtered = apply_filter_if_exists(data["bottom10_vehicle_revenue"], vehicle_type_filter, ["Type"])
churn_filtered = apply_filter_if_exists(data["churn_risk_predictions"], customer_risk_filter, ["Churn_Risk_Level"])
vehicle_risk_filtered = apply_filter_if_exists(data["vehicle_risk_predictions"], vehicle_type_filter, ["Type"])
vehicle_risk_filtered = apply_filter_if_exists(vehicle_risk_filtered, vehicle_risk_filter, ["Maintenance_Risk_Level"])

summary_metrics = {}
summary_metrics["total_revenue"] = safe_sum(master_filtered, ["Fare_VND", "Fare", "Revenue"])
summary_metrics["total_trips"] = safe_count_rows(master_filtered)
summary_metrics["users"] = safe_nunique(master_filtered, ["UserID"])
summary_metrics["vehicles"] = safe_nunique(vehicle_util_filtered, ["VehicleID"])

churn_flag_col = find_col(master_filtered, ["Has_Churned"])
if churn_flag_col and not master_filtered.empty:
    churn_flag = pd.to_numeric(master_filtered[churn_flag_col], errors="coerce")
    if not churn_flag.dropna().empty:
        summary_metrics["churn_rate"] = float(churn_flag.mean())

battery_series_util = numeric_series(vehicle_util_filtered, ["Battery_Level_Pct"])
if battery_series_util is not None:
    summary_metrics["critical_battery_vehicles"] = int((battery_series_util < 20).sum())

churn_risk_col = find_col(churn_filtered, ["Churn_Risk_Level"])
if churn_risk_col and not churn_filtered.empty:
    risk_series = churn_filtered[churn_risk_col].astype(str).str.lower()
    summary_metrics["high_risk_users"] = int(risk_series.isin(["high", "critical"]).sum())
    summary_metrics["medium_risk_users"] = int(risk_series.isin(["medium", "watch"]).sum())
    summary_metrics["low_risk_users"] = int(risk_series.isin(["low", "healthy"]).sum())

vehicle_risk_col = find_col(vehicle_risk_filtered, ["Maintenance_Risk_Level"])
if vehicle_risk_col and not vehicle_risk_filtered.empty:
    risk_series = vehicle_risk_filtered[vehicle_risk_col].astype(str).str.lower()
    summary_metrics["high_risk_vehicles"] = int(risk_series.isin(["high", "critical"]).sum())
    summary_metrics["watch_vehicles"] = int(risk_series.isin(["watch", "medium"]).sum())
    summary_metrics["healthy_vehicles"] = int(risk_series.isin(["healthy", "low"]).sum())

if mode_col and not master_filtered.empty:
    fare_col = find_col(master_filtered, ["Fare_VND", "Fare", "Revenue"])
    if fare_col:
        total_revenue = pd.to_numeric(master_filtered[fare_col], errors="coerce").sum()
        ebike_revenue = pd.to_numeric(master_filtered.loc[master_filtered[mode_col].astype(str) == "E-Bike", fare_col], errors="coerce").sum()
        summary_metrics["ebike_revenue_share"] = safe_ratio(ebike_revenue, total_revenue)

weekend_col = find_col(master_filtered, ["Is_Weekend"])
if weekend_col and not master_filtered.empty:
    weekend_num = pd.to_numeric(master_filtered[weekend_col], errors="coerce")
    if not weekend_num.dropna().empty:
        summary_metrics["weekend_trip_share"] = float(weekend_num.mean())

st.markdown(
    f"""
    <div class="sf-hero">
      <div class="sf-kicker">Glassmorphism Pro • Executive Mobility Command Center</div>
      <h1>SaigonFlow Executive Dashboard</h1>
      <p>
        The Unified Flow Platform converts fragmented trip, user, weather, and vehicle outputs into
        retention, reliability, and ROI decisions for a non-technical executive audience.
      </p>
      <p class="sf-note">
        {'Presentation Mode is ON: summaries are prioritized and raw evidence is collapsed by default.' if presentation_mode else 'Presentation Mode is OFF: detailed evidence and inspection views are expanded where useful.'}
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

assistant_data = {
    "summary_metrics": summary_metrics,
    "churn_df": churn_filtered,
    "vehicle_df": vehicle_risk_filtered,
    "rain_df": data["rain_vs_clear_analysis"],
    "master_df": master_filtered,
}

render_ai_copilot(assistant_data, presentation_mode=presentation_mode)


if page == "Executive Overview":
    section_header(
        "Executive Overview",
        "Board-level summary of business performance, risk, demand mix, and the current evidence available from exported analytics outputs.",
    )

    metric_rows = [
        build_metric_row("Total Revenue", format_vnd(summary_metrics.get("total_revenue")), "cyan", "Filtered master dataset"),
        build_metric_row("Total Trips", f"{summary_metrics.get('total_trips', 0):,}" if summary_metrics.get("total_trips") else "N/A", "teal", "Trips in current scope"),
        build_metric_row("Users", f"{summary_metrics.get('users', 0):,}" if summary_metrics.get("users") is not None else "N/A", "green", "Unique users"),
        build_metric_row("Vehicles", f"{summary_metrics.get('vehicles', 0):,}" if summary_metrics.get("vehicles") is not None else "N/A", "amber", "Unique vehicles"),
        build_metric_row("Churn Rate", format_pct(summary_metrics.get("churn_rate")), "purple", "Historical churn signal"),
        build_metric_row("Critical Battery Vehicles", f"{summary_metrics.get('critical_battery_vehicles', 0):,}" if summary_metrics.get("critical_battery_vehicles") is not None else "N/A", "red", "Battery below 20%"),
        build_metric_row("High Risk Users", f"{summary_metrics.get('high_risk_users', 0):,}" if summary_metrics.get("high_risk_users") is not None else "N/A", "purple", "High or critical churn risk"),
        build_metric_row("High Risk Vehicles", f"{summary_metrics.get('high_risk_vehicles', 0):,}" if summary_metrics.get("high_risk_vehicles") is not None else "N/A", "red", "Critical maintenance risk"),
        build_metric_row("E-Bike Revenue Share", format_pct(summary_metrics.get("ebike_revenue_share")), "cyan", "Revenue concentration"),
        build_metric_row("Weekend Trip Share", format_pct(summary_metrics.get("weekend_trip_share")), "amber", "Weekend demand mix"),
    ]

    for row_group in [metric_rows[i:i + 5] for i in range(0, len(metric_rows), 5)]:
        cols = st.columns(len(row_group))
        for col, item in zip(cols, row_group):
            with col:
                metric_card(item["label"], item["value"], item["delta"], item["tone"])

    st.markdown(
        """
        <div class="sf-summary-box">
          <strong>Board-Level Summary</strong>
          <span>
            The Unified Flow Platform links users, trips, weather conditions, and fleet telemetry into one presentation layer.
            Management can use this dashboard to protect revenue concentration, intervene on churn risk, prioritize maintenance,
            and connect analytics outputs to concrete ROI decisions.
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(2)
    fare_col = find_col(master_filtered, ["Fare_VND", "Fare", "Revenue"])
    if mode_col and fare_col and not master_filtered.empty:
        mode_rev = (
            master_filtered.assign(_revenue=pd.to_numeric(master_filtered[fare_col], errors="coerce"))
            .groupby(mode_col, dropna=False)["_revenue"]
            .sum()
            .reset_index()
            .sort_values("_revenue", ascending=False)
        )
    else:
        mode_rev = pd.DataFrame()

    with row1[0]:
        section_header("Revenue by Mode", "What this shows: the absolute revenue contribution by mobility mode.")
        if mode_rev.empty:
            st.warning("Revenue by Mode is unavailable because the required columns are missing.")
        else:
            fig = px.bar(
                mode_rev,
                x=mode_col,
                y="_revenue",
                color=mode_col,
                color_discrete_sequence=["#22d3ee", "#14b8a6", "#8b5cf6", "#f59e0b"],
            )
            render_plotly(style_fig(fig, "Revenue by Mode"), key="overview_revenue_mode")
            st.caption("Management action: protect the modes that carry the largest revenue concentration.")

    with row1[1]:
        section_header("Revenue Share by Mode", "What this shows: mode dependency and diversification pressure.")
        if mode_rev.empty:
            st.warning("Revenue Share by Mode is unavailable because the required columns are missing.")
        else:
            fig = px.pie(
                mode_rev,
                names=mode_col,
                values="_revenue",
                hole=0.58,
                color=mode_col,
                color_discrete_sequence=["#22d3ee", "#14b8a6", "#8b5cf6", "#f59e0b"],
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            render_plotly(style_fig(fig, "Revenue Share by Mode"), key="overview_revenue_share")
            st.caption("Management action: reduce overdependence if one mode dominates earnings.")

    row2 = st.columns(2)
    with row2[0]:
        section_header("Trips by Mode", "What this shows: trip volume mix across exported modes.")
        if mode_col and not master_filtered.empty:
            trips_by_mode = master_filtered.groupby(mode_col, dropna=False).size().reset_index(name="Trip_Count")
            fig = px.bar(
                trips_by_mode.sort_values("Trip_Count", ascending=False),
                x=mode_col,
                y="Trip_Count",
                color=mode_col,
                color_discrete_sequence=["#14b8a6", "#22d3ee", "#f59e0b", "#8b5cf6"],
            )
            render_plotly(style_fig(fig, "Trips by Mode"), key="overview_trips_mode")
            st.caption("Management action: compare trip volume to revenue to see which modes monetize best.")
        else:
            st.warning("Trips by Mode is unavailable because the required columns are missing.")

    with row2[1]:
        section_header("Executive Risk Snapshot", "What this shows: current risk mix across customers and fleet.")
        churn_counts = make_level_counts(churn_filtered, ["Churn_Risk_Level"])
        vehicle_counts = make_level_counts(vehicle_risk_filtered, ["Maintenance_Risk_Level"])
        if churn_counts.empty and vehicle_counts.empty:
            st.warning("Risk snapshot is unavailable because the prediction outputs or risk columns are missing.")
        else:
            combined = []
            if not churn_counts.empty:
                temp = churn_counts.copy()
                temp["Category"] = "Customer Churn"
                combined.append(temp.rename(columns={"Level": "Risk_Level"}))
            if not vehicle_counts.empty:
                temp = vehicle_counts.copy()
                temp["Category"] = "Vehicle Maintenance"
                combined.append(temp.rename(columns={"Level": "Risk_Level"}))
            risk_df = pd.concat(combined, ignore_index=True)
            fig = px.bar(
                risk_df,
                x="Risk_Level",
                y="Count",
                color="Category",
                barmode="group",
                color_discrete_sequence=["#8b5cf6", "#ef4444"],
            )
            render_plotly(style_fig(fig, "Executive Risk Snapshot"), key="overview_risk_snapshot")
            st.caption("Management action: combine retention and maintenance interventions instead of treating them separately.")


elif page == "Balanced Scorecard":
    section_header(
        "Balanced Scorecard",
        "The Balanced Scorecard connects technical metrics to executive targets: financial performance, customer retention, fleet reliability, and AI-enabled learning.",
    )

    bsc = data["balanced_scorecard"]
    if bsc.empty:
        st.warning("`balanced_scorecard.csv` is missing or unreadable.")
    else:
        perspective_col = find_col(bsc, ["Perspective"])
        metric_col = find_col(bsc, ["Metrics", "Metric"])
        target_col = find_col(bsc, ["Target"])
        interpretation_col = find_col(bsc, ["MIS Interpretation", "Interpretation"])

        if not all([perspective_col, metric_col, target_col, interpretation_col]):
            st.warning("Balanced Scorecard columns could not be inferred safely. Showing the raw scorecard table.")
            render_dataframe(bsc)
        else:
            perspective_details = []
            for _, row in bsc.iterrows():
                perspective = str(row[perspective_col])
                metric_text = str(row[metric_col])
                target_text = str(row[target_col])
                interpretation = str(row[interpretation_col])
                status_label, tone = scorecard_status(perspective, summary_metrics)

                current_value = metric_text
                key_metric = metric_text.split(";")[0] if ";" in metric_text else metric_text
                if "financial" in normalize_name(perspective):
                    current_value = (
                        f"Revenue {format_vnd(summary_metrics.get('total_revenue'))}; "
                        f"E-Bike share {format_pct(summary_metrics.get('ebike_revenue_share'))}"
                    )
                elif "customer" in normalize_name(perspective):
                    current_value = (
                        f"Churn rate {format_pct(summary_metrics.get('churn_rate'))}; "
                        f"high-risk users {summary_metrics.get('high_risk_users', 'N/A')}"
                    )
                elif "internal" in normalize_name(perspective) or "fleet" in normalize_name(perspective):
                    current_value = (
                        f"Critical battery vehicles {summary_metrics.get('critical_battery_vehicles', 'N/A')}; "
                        f"high-risk vehicles {summary_metrics.get('high_risk_vehicles', 'N/A')}"
                    )
                else:
                    metrics_df = data["model_metrics_summary"]
                    f1_col = find_col(metrics_df, ["F1"])
                    model_col = find_col(metrics_df, ["Model"])
                    current_value = "Predictive outputs active"
                    if f1_col and model_col and not metrics_df.empty:
                        top_f1 = metrics_df.assign(_f1=pd.to_numeric(metrics_df[f1_col], errors="coerce")).sort_values("_f1", ascending=False).head(1)
                        if not top_f1.empty:
                            current_value = f"Best F1 {format_float(top_f1['_f1'].iloc[0], 3)} from {top_f1[model_col].iloc[0]}"

                perspective_details.append(
                    {
                        "perspective": perspective,
                        "key_metric": key_metric,
                        "current_value": current_value,
                        "target": target_text,
                        "interpretation": interpretation,
                        "status": status_label,
                        "tone": tone,
                    }
                )

            cards = st.columns(4)
            for col, detail in zip(cards, perspective_details[:4]):
                with col:
                    scorecard_box(
                        detail["perspective"],
                        detail["key_metric"],
                        detail["current_value"],
                        detail["target"],
                        detail["interpretation"],
                        detail["status"],
                        detail["tone"],
                    )

            chart_records = []
            for detail in perspective_details:
                numeric_hint = parse_first_number(detail["current_value"])
                if numeric_hint is not None:
                    chart_records.append(
                        {
                            "Perspective": detail["perspective"],
                            "Current": numeric_hint,
                            "Target": parse_first_number(detail["target"]),
                        }
                    )

            if chart_records:
                section_header("Scorecard Snapshot", "What this shows: side-by-side numeric hints from the scorecard text where inference is safe.")
                chart_df = pd.DataFrame(chart_records).melt(id_vars="Perspective", value_vars=["Current", "Target"], var_name="Type", value_name="Value").dropna()
                if not chart_df.empty:
                    fig = px.bar(
                        chart_df,
                        x="Perspective",
                        y="Value",
                        color="Type",
                        barmode="group",
                        color_discrete_sequence=["#22d3ee", "#f59e0b"],
                    )
                    render_plotly(style_fig(fig, "Balanced Scorecard Snapshot"), key="bsc_snapshot")
                else:
                    st.info("No numeric scorecard snapshot could be inferred safely.")
            else:
                st.info("The scorecard is primarily text-based, so the raw table remains the most reliable evidence.")

            evidence_expanded = not presentation_mode
            with st.expander("Balanced Scorecard source table", expanded=evidence_expanded):
                render_dataframe(bsc)


elif page == "Fleet Performance":
    section_header(
        "Fleet Performance",
        "Use revenue, battery, and maintenance evidence together so operational priorities align with uptime and revenue protection.",
    )

    row1 = st.columns(2)
    with row1[0]:
        section_header("Top 10 Vehicles by Revenue", "What this shows: the assets worth protecting first.")
        id_col = find_col(top10_filtered, ["VehicleID"])
        rev_col = find_col(top10_filtered, ["Total_Revenue", "Revenue"])
        if not top10_filtered.empty and id_col and rev_col:
            fig = px.bar(
                top10_filtered.sort_values(rev_col, ascending=True),
                x=rev_col,
                y=id_col,
                orientation="h",
                color=rev_col,
                color_continuous_scale=["#0f3445", "#22d3ee"],
            )
            render_plotly(style_fig(fig, "Top 10 Vehicles by Revenue"), key="fleet_top10")
            st.caption("Management action: protect these vehicles first because downtime has higher revenue impact.")
        else:
            st.warning("Top 10 vehicle revenue chart is unavailable.")

    with row1[1]:
        section_header("Bottom 10 Vehicles by Revenue", "What this shows: assets that may be poorly placed or underutilized.")
        id_col = find_col(bottom10_filtered, ["VehicleID"])
        rev_col = find_col(bottom10_filtered, ["Total_Revenue", "Revenue"])
        if not bottom10_filtered.empty and id_col and rev_col:
            fig = px.bar(
                bottom10_filtered.sort_values(rev_col, ascending=True),
                x=rev_col,
                y=id_col,
                orientation="h",
                color=rev_col,
                color_continuous_scale=["#40131a", "#ef4444"],
            )
            render_plotly(style_fig(fig, "Bottom 10 Vehicles by Revenue"), key="fleet_bottom10")
            st.caption("Management action: investigate placement, battery readiness, and mode-specific demand.")
        else:
            st.warning("Bottom 10 vehicle revenue chart is unavailable.")

    row2 = st.columns(2)
    with row2[0]:
        section_header("Battery Level Distribution", "What this shows: how much of the fleet is operating near critical thresholds.")
        battery_col = find_col(vehicle_util_filtered, ["Battery_Level_Pct"])
        if battery_col and not vehicle_util_filtered.empty:
            battery_df = vehicle_util_filtered.copy()
            battery_df["_battery"] = pd.to_numeric(battery_df[battery_col], errors="coerce")
            battery_df = battery_df.dropna(subset=["_battery"])
            if not battery_df.empty:
                fig = px.histogram(
                    battery_df,
                    x="_battery",
                    nbins=20,
                    color_discrete_sequence=["#22d3ee"],
                )
                render_plotly(style_fig(fig, "Battery Level Distribution"), key="fleet_battery_hist")
            else:
                st.warning("Battery values are present but could not be parsed safely.")
        else:
            st.warning("Battery distribution is unavailable.")

    with row2[1]:
        section_header("Maintenance Risk Breakdown", "What this shows: where fleet maintenance pressure is concentrated.")
        risk_counts = make_level_counts(vehicle_risk_filtered, ["Maintenance_Risk_Level"])
        if not risk_counts.empty:
            fig = px.pie(
                risk_counts,
                names="Level",
                values="Count",
                hole=0.55,
                color="Level",
                color_discrete_map={
                    "Critical": "#ef4444",
                    "Watch": "#f59e0b",
                    "Healthy": "#14b8a6",
                },
            )
            fig.update_traces(textinfo="percent+label")
            render_plotly(style_fig(fig, "Maintenance Risk Level Breakdown"), key="fleet_risk_donut")
        else:
            st.warning("Maintenance risk breakdown is unavailable.")

    row3 = st.columns(2)
    battery_col_v = find_col(vehicle_risk_filtered, ["Battery_Level_Pct"])
    revenue_col_v = find_col(vehicle_risk_filtered, ["Total_Revenue", "Revenue"])
    trip_col_v = find_col(vehicle_risk_filtered, ["Trip_Count"])
    type_col_v = find_col(vehicle_risk_filtered, ["Type"])

    with row3[0]:
        section_header("Revenue vs Battery", "What this shows: whether high-earning vehicles are operating with weak battery health.")
        if battery_col_v and revenue_col_v and not vehicle_risk_filtered.empty:
            scatter_df = vehicle_risk_filtered.copy()
            scatter_df["_battery"] = pd.to_numeric(scatter_df[battery_col_v], errors="coerce")
            scatter_df["_revenue"] = pd.to_numeric(scatter_df[revenue_col_v], errors="coerce")
            scatter_df = scatter_df.dropna(subset=["_battery", "_revenue"])
            if not scatter_df.empty:
                fig = px.scatter(
                    scatter_df,
                    x="_battery",
                    y="_revenue",
                    color=type_col_v if type_col_v else None,
                    hover_name=find_col(scatter_df, ["VehicleID"]),
                    color_discrete_sequence=["#22d3ee", "#14b8a6", "#8b5cf6"],
                )
                render_plotly(style_fig(fig, "Revenue vs Battery"), key="fleet_rev_battery")
            else:
                st.warning("Revenue vs Battery could not be rendered safely.")
        else:
            st.warning("Revenue vs Battery is unavailable.")

    with row3[1]:
        section_header("Trip Count vs Battery", "What this shows: whether low-battery assets are still carrying demand.")
        if battery_col_v and trip_col_v and not vehicle_risk_filtered.empty:
            scatter_df = vehicle_risk_filtered.copy()
            scatter_df["_battery"] = pd.to_numeric(scatter_df[battery_col_v], errors="coerce")
            scatter_df["_trip_count"] = pd.to_numeric(scatter_df[trip_col_v], errors="coerce")
            scatter_df = scatter_df.dropna(subset=["_battery", "_trip_count"])
            if not scatter_df.empty:
                fig = px.scatter(
                    scatter_df,
                    x="_battery",
                    y="_trip_count",
                    color=type_col_v if type_col_v else None,
                    hover_name=find_col(scatter_df, ["VehicleID"]),
                    color_discrete_sequence=["#14b8a6", "#22d3ee", "#8b5cf6"],
                )
                render_plotly(style_fig(fig, "Trip Count vs Battery"), key="fleet_trips_battery")
            else:
                st.warning("Trip Count vs Battery could not be rendered safely.")
        else:
            st.warning("Trip Count vs Battery is unavailable.")

    priority_df = vehicle_risk_filtered.copy()
    if not priority_df.empty:
        risk_col = find_col(priority_df, ["Maintenance_Risk_Level"])
        prob_col = find_col(priority_df, ["Predicted_Action_Probability"])
        battery_col = find_col(priority_df, ["Battery_Level_Pct"])
        revenue_col = find_col(priority_df, ["Total_Revenue", "Revenue"])
        if risk_col:
            priority_df["_risk_priority"] = priority_df[risk_col].map(risk_priority_value)
        else:
            priority_df["_risk_priority"] = 99
        priority_df["_prob"] = pd.to_numeric(priority_df[prob_col], errors="coerce") if prob_col else np.nan
        priority_df["_battery"] = pd.to_numeric(priority_df[battery_col], errors="coerce") if battery_col else np.nan
        priority_df["_revenue"] = pd.to_numeric(priority_df[revenue_col], errors="coerce") if revenue_col else np.nan
        priority_df = priority_df.sort_values(
            by=["_risk_priority", "_prob", "_battery", "_revenue"],
            ascending=[True, False, True, False],
        )

    section_header("Maintenance-Priority Vehicles", "What this shows: the top 20 vehicles that should move first in the maintenance queue.")
    priority_columns = [
        find_col(priority_df, ["VehicleID"]),
        find_col(priority_df, ["Type"]),
        find_col(priority_df, ["Battery_Level_Pct"]),
        find_col(priority_df, ["Days_Since_Maintenance"]),
        find_col(priority_df, ["Trip_Count"]),
        find_col(priority_df, ["Total_Revenue", "Revenue"]),
        find_col(priority_df, ["Predicted_Action_Probability"]),
        find_col(priority_df, ["Maintenance_Risk_Level"]),
        find_col(priority_df, ["Recommended_Action"]),
    ]
    priority_columns = [col for col in priority_columns if col]
    if priority_df.empty or not priority_columns:
        st.warning("Maintenance-priority table is unavailable.")
    else:
        render_dataframe(priority_df[priority_columns].head(20))

    callouts = st.columns(3)
    with callouts[0]:
        insight_box("Protect High-Revenue Vehicles First", "High-revenue vehicles should be protected first because every downtime event creates higher opportunity cost.", "cyan")
    with callouts[1]:
        insight_box("Low-Revenue Vehicles Need Diagnosis", "Low-revenue vehicles may indicate poor placement, weak demand, or battery availability issues.", "amber")
    with callouts[2]:
        insight_box("Critical Battery Assets Hurt Reliability", "Critical battery vehicles increase both churn risk and service reliability pressure.", "red")


elif page == "Weather & Demand":
    section_header(
        "Weather & Demand",
        "Weather sensitivity and commute concentration should shape pricing, pre-positioning, and mode-specific demand recovery decisions.",
    )

    rain_df = data["rain_vs_clear_analysis"]
    fare_col = find_col(master_filtered, ["Fare_VND", "Fare", "Revenue"])

    row1 = st.columns(2)
    with row1[0]:
        section_header("Rain vs Clear Revenue", "What this shows: exported revenue comparison between rain and clear conditions.")
        cat_col = find_col(rain_df, ["Rain_Category"])
        rev_col = find_col(rain_df, ["Total_Revenue", "Revenue"])
        if not rain_df.empty and cat_col and rev_col:
            chart_df = rain_df.copy()
            chart_df["_revenue"] = pd.to_numeric(chart_df[rev_col], errors="coerce")
            fig = px.bar(
                chart_df,
                x=cat_col,
                y="_revenue",
                color=cat_col,
                color_discrete_sequence=["#22d3ee", "#f59e0b"],
            )
            render_plotly(style_fig(fig, "Rain vs Clear Revenue"), key="weather_rain_revenue")
        else:
            st.warning("Rain vs Clear revenue chart is unavailable.")

    with row1[1]:
        section_header("Rain vs Clear Trip Count", "What this shows: exported demand drop between weather categories.")
        trip_col = find_col(rain_df, ["Trip_Count"])
        if not rain_df.empty and cat_col and trip_col:
            chart_df = rain_df.copy()
            chart_df["_trip_count"] = pd.to_numeric(chart_df[trip_col], errors="coerce")
            fig = px.bar(
                chart_df,
                x=cat_col,
                y="_trip_count",
                color=cat_col,
                color_discrete_sequence=["#14b8a6", "#f59e0b"],
            )
            render_plotly(style_fig(fig, "Rain vs Clear Trip Count"), key="weather_rain_trips")
        else:
            st.warning("Rain vs Clear trip count chart is unavailable.")

    row2 = st.columns(2)
    with row2[0]:
        section_header("Trips by Weather Condition", "What this shows: trip volume by detailed weather category.")
        if weather_col and not master_filtered.empty:
            weather_chart_df = master_filtered.groupby(weather_col, dropna=False).size().reset_index(name="Trip_Count")
            fig = px.bar(
                weather_chart_df.sort_values("Trip_Count", ascending=False),
                x=weather_col,
                y="Trip_Count",
                color=weather_col,
                color_discrete_sequence=["#22d3ee", "#14b8a6", "#f59e0b", "#8b5cf6"],
            )
            render_plotly(style_fig(fig, "Trips by Weather Condition"), key="weather_trips_by_condition")
        else:
            st.warning("Trips by Weather Condition is unavailable.")

    with row2[1]:
        section_header("Revenue by Weather Condition", "What this shows: revenue resilience or weakness across weather conditions.")
        if weather_col and fare_col and not master_filtered.empty:
            temp = master_filtered.copy()
            temp["_revenue"] = pd.to_numeric(temp[fare_col], errors="coerce")
            weather_rev_df = temp.groupby(weather_col, dropna=False)["_revenue"].sum().reset_index()
            fig = px.bar(
                weather_rev_df.sort_values("_revenue", ascending=False),
                x=weather_col,
                y="_revenue",
                color=weather_col,
                color_discrete_sequence=["#22d3ee", "#14b8a6", "#f59e0b", "#8b5cf6"],
            )
            render_plotly(style_fig(fig, "Revenue by Weather Condition"), key="weather_revenue_condition")
        else:
            st.warning("Revenue by Weather Condition is unavailable.")

    row3 = st.columns(2)
    hour_series = master_filtered["_hour"] if "_hour" in master_filtered.columns and not master_filtered.empty else pd.Series(dtype=float)
    with row3[0]:
        section_header("Trips by Hour", "What this shows: demand concentration across the day.")
        if not master_filtered.empty and not hour_series.dropna().empty:
            trips_by_hour = (
                pd.DataFrame({"Hour": hour_series})
                .dropna()
                .assign(Hour=lambda df_: df_["Hour"].astype(int))
                .groupby("Hour")
                .size()
                .reset_index(name="Trip_Count")
            )
            fig = px.line(
                trips_by_hour,
                x="Hour",
                y="Trip_Count",
                markers=True,
                color_discrete_sequence=["#22d3ee"],
            )
            render_plotly(style_fig(fig, "Trips by Hour"), key="weather_trips_hour")
        else:
            st.warning("Trips by Hour is unavailable.")

    with row3[1]:
        section_header("Revenue by Hour", "What this shows: which parts of the day create the most revenue.")
        if not master_filtered.empty and fare_col and not hour_series.dropna().empty:
            temp = master_filtered.copy()
            temp["_hour_numeric"] = pd.to_numeric(temp["_hour"], errors="coerce")
            temp["_revenue"] = pd.to_numeric(temp[fare_col], errors="coerce")
            hour_rev = temp.dropna(subset=["_hour_numeric", "_revenue"]).assign(Hour=lambda df_: df_["_hour_numeric"].astype(int)).groupby("Hour")["_revenue"].sum().reset_index()
            fig = px.bar(hour_rev, x="Hour", y="_revenue", color_discrete_sequence=["#14b8a6"])
            render_plotly(style_fig(fig, "Revenue by Hour"), key="weather_revenue_hour")
        else:
            st.warning("Revenue by Hour is unavailable.")

    row4 = st.columns(2)
    with row4[0]:
        section_header("Weekend vs Weekday Trips", "What this shows: weekend mix in the filtered demand view.")
        if weekend_col and not master_filtered.empty:
            weekend_df = master_filtered.groupby("_weekend_label").size().reset_index(name="Trip_Count")
            fig = px.bar(
                weekend_df,
                x="_weekend_label",
                y="Trip_Count",
                color="_weekend_label",
                color_discrete_sequence=["#22d3ee", "#8b5cf6"],
            )
            render_plotly(style_fig(fig, "Weekend vs Weekday Trips"), key="weather_weekend")
        else:
            st.warning("Weekend vs Weekday chart is unavailable.")

    with row4[1]:
        section_header("Peak vs Non-Peak Demand", "What this shows: commute concentration for pre-positioning decisions.")
        if not master_filtered.empty and "_peak_label" in master_filtered.columns:
            peak_df = master_filtered.groupby("_peak_label").size().reset_index(name="Trip_Count")
            fig = px.bar(
                peak_df,
                x="_peak_label",
                y="Trip_Count",
                color="_peak_label",
                color_discrete_sequence=["#f59e0b", "#14b8a6"],
            )
            render_plotly(style_fig(fig, "Peak vs Non-Peak Comparison"), key="weather_peak")
        else:
            st.warning("Peak vs Non-Peak comparison is unavailable.")

    callouts = st.columns(3)
    with callouts[0]:
        insight_box("Weather-Responsive Pricing", "Rain-sensitive demand supports weather-responsive pricing to protect margins when usage drops.", "amber")
    with callouts[1]:
        insight_box("Rain Recovery via Shuttle Incentives", "Shuttle incentives during rain can help recover demand when E-Bike usage weakens.", "teal")
    with callouts[2]:
        insight_box("Peak-Hour Pre-Positioning", "Peak-hour demand supports pre-positioning before 7–9 AM and 5–7 PM.", "cyan")


elif page == "Predictive AI":
    section_header(
        "Predictive AI",
        "These prediction pages convert exported model outputs into management actions for customer retention and vehicle uptime.",
    )

    render_workflow_panel()
    st.info("Use the floating AI Board Assistant button to ask board-level questions. The main assistant is now available as a global local copilot.")

    tab1, tab2, tab3 = st.tabs(["Customer Churn AI", "Vehicle Risk AI", "Model Evidence"])

    with tab1:
        section_header(
            "Customer Churn AI",
            "This model estimates which users are more likely to churn based on historical trip behavior, weather exposure, peak-hour usage, loyalty points, and profile signals.",
        )
        if churn_filtered.empty:
            st.warning("`churn_risk_predictions.csv` is missing or unreadable.")
        else:
            risk_col = find_col(churn_filtered, ["Churn_Risk_Level"])
            prob_col = find_col(churn_filtered, ["Predicted_Churn_Probability"])
            mode_pref_col = find_col(churn_filtered, ["Preferred_Mode"])
            loyalty_col = find_col(churn_filtered, ["Loyalty_Points"])

            churn_kpis = [
                build_metric_row("High Risk Users", f"{summary_metrics.get('high_risk_users', 0):,}" if summary_metrics.get("high_risk_users") is not None else "N/A", "red"),
                build_metric_row("Medium Risk Users", f"{summary_metrics.get('medium_risk_users', 0):,}" if summary_metrics.get("medium_risk_users") is not None else "N/A", "amber"),
                build_metric_row("Low Risk Users", f"{summary_metrics.get('low_risk_users', 0):,}" if summary_metrics.get("low_risk_users") is not None else "N/A", "green"),
                build_metric_row("Average Churn Probability", format_pct(safe_mean(churn_filtered, ["Predicted_Churn_Probability"])), "purple"),
            ]
            churn_cols = st.columns(4)
            for col, metric in zip(churn_cols, churn_kpis):
                with col:
                    metric_card(metric["label"], metric["value"], metric.get("delta"), metric["tone"])

            row1 = st.columns(2)
            with row1[0]:
                section_header("Users by Churn Risk Level", "What this shows: how many users are currently in each retention segment.")
                counts = make_level_counts(churn_filtered, ["Churn_Risk_Level"])
                if not counts.empty:
                    fig = px.bar(
                        counts,
                        x="Level",
                        y="Count",
                        color="Level",
                        color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"},
                    )
                    render_plotly(style_fig(fig, "User Count by Churn Risk Level"), key="ai_churn_counts")
                else:
                    st.warning("Churn risk level chart is unavailable.")

            with row1[1]:
                section_header("Churn Probability Distribution", "What this shows: how concentrated the model's churn probabilities are.")
                if prob_col:
                    temp = churn_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob"])
                    if not temp.empty:
                        fig = px.histogram(temp, x="_prob", nbins=25, color_discrete_sequence=["#8b5cf6"])
                        render_plotly(style_fig(fig, "Distribution of Predicted Churn Probability"), key="ai_churn_dist")
                    else:
                        st.warning("Churn probability distribution is unavailable.")
                else:
                    st.warning("Churn probability distribution is unavailable.")

            row2 = st.columns(2)
            with row2[0]:
                section_header("Churn Probability by Preferred Mode", "What this shows: whether some modes are associated with higher churn exposure.")
                if prob_col and mode_pref_col:
                    temp = churn_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob"])
                    if not temp.empty:
                        fig = px.box(
                            temp,
                            x=mode_pref_col,
                            y="_prob",
                            color=mode_pref_col,
                            color_discrete_sequence=["#22d3ee", "#14b8a6", "#8b5cf6", "#f59e0b"],
                        )
                        render_plotly(style_fig(fig, "Churn Probability by Preferred Mode"), key="ai_churn_mode")
                    else:
                        st.warning("Churn probability by preferred mode is unavailable.")
                else:
                    st.warning("Churn probability by preferred mode is unavailable.")

            with row2[1]:
                section_header("Churn Probability vs Loyalty Points", "What this shows: whether loyalty strength offsets predicted churn pressure.")
                if prob_col and loyalty_col:
                    temp = churn_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp["_loyalty"] = pd.to_numeric(temp[loyalty_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob", "_loyalty"])
                    if not temp.empty:
                        fig = px.scatter(
                            temp,
                            x="_loyalty",
                            y="_prob",
                            color=risk_col if risk_col else None,
                            hover_name=find_col(temp, ["UserID"]),
                            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"},
                        )
                        render_plotly(style_fig(fig, "Churn Probability vs Loyalty Points"), key="ai_churn_loyalty")
                    else:
                        st.warning("Churn probability vs loyalty points is unavailable.")
                else:
                    st.warning("Churn probability vs loyalty points is unavailable.")

            section_header("Top 20 High-Risk Users", "What this shows: the users who should receive proactive retention treatment first.")
            if prob_col:
                preview = churn_filtered.assign(_prob=pd.to_numeric(churn_filtered[prob_col], errors="coerce")).sort_values("_prob", ascending=False)
            else:
                preview = churn_filtered.copy()
            render_dataframe(preview.head(20))

    with tab2:
        section_header(
            "Vehicle Risk AI",
            "This model prioritizes vehicles for charging or maintenance based on battery level, maintenance age, utilization, revenue contribution, and demand exposure.",
        )
        if vehicle_risk_filtered.empty:
            st.warning("`vehicle_risk_predictions.csv` is missing or unreadable.")
        else:
            risk_col = find_col(vehicle_risk_filtered, ["Maintenance_Risk_Level"])
            prob_col = find_col(vehicle_risk_filtered, ["Predicted_Action_Probability"])
            type_col = find_col(vehicle_risk_filtered, ["Type"])
            battery_col = find_col(vehicle_risk_filtered, ["Battery_Level_Pct"])

            vehicle_kpis = [
                build_metric_row("Critical Vehicles", f"{summary_metrics.get('high_risk_vehicles', 0):,}" if summary_metrics.get("high_risk_vehicles") is not None else "N/A", "red"),
                build_metric_row("Watch Vehicles", f"{summary_metrics.get('watch_vehicles', 0):,}" if summary_metrics.get("watch_vehicles") is not None else "N/A", "amber"),
                build_metric_row("Healthy Vehicles", f"{summary_metrics.get('healthy_vehicles', 0):,}" if summary_metrics.get("healthy_vehicles") is not None else "N/A", "green"),
                build_metric_row("Average Action Probability", format_pct(safe_mean(vehicle_risk_filtered, ["Predicted_Action_Probability"])), "purple"),
            ]
            vehicle_cols = st.columns(4)
            for col, metric in zip(vehicle_cols, vehicle_kpis):
                with col:
                    metric_card(metric["label"], metric["value"], metric.get("delta"), metric["tone"])

            row1 = st.columns(2)
            with row1[0]:
                section_header("Vehicles by Maintenance Risk Level", "What this shows: how much of the fleet needs attention first.")
                counts = make_level_counts(vehicle_risk_filtered, ["Maintenance_Risk_Level"])
                if not counts.empty:
                    fig = px.bar(
                        counts,
                        x="Level",
                        y="Count",
                        color="Level",
                        color_discrete_map={"Critical": "#ef4444", "Watch": "#f59e0b", "Healthy": "#14b8a6"},
                    )
                    render_plotly(style_fig(fig, "Vehicle Count by Maintenance Risk Level"), key="ai_vehicle_counts")
                else:
                    st.warning("Vehicle maintenance risk chart is unavailable.")

            with row1[1]:
                section_header("Action Probability Distribution", "What this shows: how concentrated predicted maintenance urgency is.")
                if prob_col:
                    temp = vehicle_risk_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob"])
                    if not temp.empty:
                        fig = px.histogram(temp, x="_prob", nbins=25, color_discrete_sequence=["#8b5cf6"])
                        render_plotly(style_fig(fig, "Distribution of Predicted Action Probability"), key="ai_vehicle_dist")
                    else:
                        st.warning("Action probability distribution is unavailable.")
                else:
                    st.warning("Action probability distribution is unavailable.")

            row2 = st.columns(2)
            with row2[0]:
                section_header("Action Probability by Vehicle Type", "What this shows: whether one asset class carries more maintenance urgency.")
                if prob_col and type_col:
                    temp = vehicle_risk_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob"])
                    if not temp.empty:
                        fig = px.box(
                            temp,
                            x=type_col,
                            y="_prob",
                            color=type_col,
                            color_discrete_sequence=["#22d3ee", "#14b8a6", "#8b5cf6"],
                        )
                        render_plotly(style_fig(fig, "Action Probability by Type"), key="ai_vehicle_type")
                    else:
                        st.warning("Action probability by vehicle type is unavailable.")
                else:
                    st.warning("Action probability by vehicle type is unavailable.")

            with row2[1]:
                section_header("Action Probability vs Battery Level", "What this shows: whether low battery is aligning with maintenance urgency.")
                if prob_col and battery_col:
                    temp = vehicle_risk_filtered.copy()
                    temp["_prob"] = pd.to_numeric(temp[prob_col], errors="coerce")
                    temp["_battery"] = pd.to_numeric(temp[battery_col], errors="coerce")
                    temp = temp.dropna(subset=["_prob", "_battery"])
                    if not temp.empty:
                        fig = px.scatter(
                            temp,
                            x="_battery",
                            y="_prob",
                            color=risk_col if risk_col else None,
                            hover_name=find_col(temp, ["VehicleID"]),
                            color_discrete_map={"Critical": "#ef4444", "Watch": "#f59e0b", "Healthy": "#14b8a6"},
                        )
                        render_plotly(style_fig(fig, "Action Probability vs Battery Level"), key="ai_vehicle_battery")
                    else:
                        st.warning("Action probability vs battery level is unavailable.")
                else:
                    st.warning("Action probability vs battery level is unavailable.")

            section_header("Top 20 Maintenance-Priority Vehicles", "What this shows: the vehicle queue management should review first, sorted by risk, urgency, and battery pressure.")
            vehicle_preview = vehicle_risk_filtered.copy()
            if risk_col:
                vehicle_preview["_risk_priority"] = vehicle_preview[risk_col].map(risk_priority_value)
            else:
                vehicle_preview["_risk_priority"] = 99
            if prob_col:
                vehicle_preview["_prob"] = pd.to_numeric(vehicle_preview[prob_col], errors="coerce")
            else:
                vehicle_preview["_prob"] = np.nan
            if battery_col:
                vehicle_preview["_battery"] = pd.to_numeric(vehicle_preview[battery_col], errors="coerce")
            else:
                vehicle_preview["_battery"] = np.nan
            vehicle_preview = vehicle_preview.sort_values(
                by=["_risk_priority", "_prob", "_battery"],
                ascending=[True, False, True],
            )
            render_dataframe(vehicle_preview.head(20))

    with tab3:
        section_header("Model Evidence", "F1 matters here because risk detection is more important than broad accuracy alone.")
        metrics_df = data["model_metrics_summary"]
        if metrics_df.empty:
            st.warning("`model_metrics_summary.csv` is missing or unreadable.")
        else:
            render_dataframe(metrics_df)
            metric_columns = [find_col(metrics_df, [name]) for name in ["Accuracy", "Precision", "Recall", "F1", "ROC_AUC"]]
            metric_columns = [col for col in metric_columns if col]
            task_col = find_col(metrics_df, ["Task"])
            model_col = find_col(metrics_df, ["Model"])
            if task_col and model_col and metric_columns:
                chart_df = metrics_df.copy()
                for col in metric_columns:
                    chart_df[col] = pd.to_numeric(chart_df[col], errors="coerce")
                melted = chart_df.melt(id_vars=[task_col, model_col], value_vars=metric_columns, var_name="Metric", value_name="Value").dropna()
                if not melted.empty:
                    fig = px.bar(
                        melted,
                        x="Metric",
                        y="Value",
                        color=model_col,
                        barmode="group",
                        facet_col=task_col,
                        facet_col_wrap=1,
                    )
                    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                    render_plotly(style_fig(fig, "Model Metrics by Task and Model"), key="ai_metrics_chart")
            st.info(
                "The vehicle risk model uses a simulated operational target because the generated dataset does not contain true future failure labels. This is appropriate for Phase 3 predictive analytics simulation, but production deployment would require future maintenance/failure outcome data."
            )


elif page == "ROI Recommendations":
    section_header(
        "ROI Recommendations",
        "Each recommendation connects exported evidence to a management action and a business outcome.",
    )

    top10_revenue = safe_sum(top10_filtered, ["Total_Revenue", "Revenue"])
    bottom10_revenue = safe_sum(bottom10_filtered, ["Total_Revenue", "Revenue"])
    rain_trip_text = "Rain vs clear demand evidence is available in exported weather analysis." if not data["rain_vs_clear_analysis"].empty else "Weather export is unavailable."
    recommendations = [
        (
            "Protect High-Revenue Vehicles",
            "High-value assets create outsized revenue exposure when they go offline.",
            f"Top 10 vehicles contribute {format_vnd(top10_revenue)} in the current evidence." if top10_revenue is not None else "Top vehicle revenue export identifies revenue-leading assets.",
            "Prioritize charging, maintenance, and uptime protection for the highest-revenue vehicles first.",
            "Protects concentrated revenue and reduces expensive downtime.",
            "cyan",
        ),
        (
            "Reduce Churn with Proactive Offers",
            "High-risk users can churn before operations responds.",
            f"Current high-risk users in filtered churn predictions: {summary_metrics.get('high_risk_users', 'N/A')}." if summary_metrics.get("high_risk_users") is not None else "Churn-risk predictions are available for prioritization.",
            "Trigger retention offers, loyalty recovery, and service recovery messaging for the highest-risk users.",
            "Protects customer lifetime value and lowers reacquisition cost.",
            "purple",
        ),
        (
            "Weather-Responsive Pricing",
            "Weather-sensitive demand can reduce realized revenue while operating costs remain.",
            rain_trip_text,
            "Use weather-responsive pricing and targeted incentives during rainy conditions to stabilize demand and margin.",
            "Improves rainy-day margin protection and supports better utilization.",
            "amber",
        ),
        (
            "Peak-Hour Fleet Redistribution",
            "Peak commuting windows create concentrated demand and stockout risk.",
            f"Peak-hour share in the filtered master dataset: {format_pct(safe_mean(master_filtered, ['Is_Peak_Hour']))}." if find_col(master_filtered, ["Is_Peak_Hour"]) else "Peak-hour evidence is available through hourly demand patterns.",
            "Pre-position inventory before the morning and evening commute peaks.",
            "Improves trip capture, asset productivity, and service reliability.",
            "teal",
        ),
        (
            "Deploy AI Alerts in Fleet Dashboard",
            "Predictive outputs lose value if they remain buried in raw exports.",
            "Both churn and vehicle-risk prediction outputs are available for operational review.",
            "Embed risk alerts into routine management review so interventions happen before churn or downtime escalates.",
            "Raises the ROI of predictive analytics by shortening response time.",
            "red",
        ),
    ]

    cols = st.columns(2)
    for idx, item in enumerate(recommendations):
        title, problem, evidence, action, impact, tone = item
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="sf-rec-card" style="--tone: {COLOR_MAP.get(tone, COLOR_MAP['cyan'])};">
                  <div class="sf-rec-title">{title}</div>
                  <div class="sf-rec-body">
                    <strong>Problem</strong><br>{problem}<br><br>
                    <strong>Data Evidence</strong><br>{evidence}<br><br>
                    <strong>Management Action</strong><br>{action}<br><br>
                    <strong>Expected ROI Impact</strong><br>{impact}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="sf-summary-box">
          <strong>Executive Callout</strong>
          <span>
            SaigonFlow should treat the Unified Flow Platform not only as a database integration project,
            but as a decision engine that converts data into retention, reliability, and revenue protection.
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


elif page == "Data Evidence":
    section_header(
        "Data Evidence",
        "Audit the exported evidence, confirm file availability, and inspect source tables without touching the notebook or outputs.",
    )

    render_file_status(data, pngs)

    records = []
    for key, filename in EXPECTED_CSVS.items():
        df = data[key]
        records.append(
            {
                "file": filename,
                "status": "found" if not df.empty else "missing",
                "rows": safe_count_rows(df),
                "columns": 0 if df.empty else len(df.columns),
            }
        )
    status_df = pd.DataFrame(records)
    render_dataframe(status_df)

    with st.expander("Phase 3 Execution Report", expanded=True):
        if codex_report:
            st.markdown(codex_report)
        else:
            st.warning("codex_phase3_report.md not found in outputs/.")

    if not presentation_mode:
        evidence_expanded = False
        for key, filename in EXPECTED_CSVS.items():
            df = data[key]
            with st.expander(filename, expanded=evidence_expanded and not df.empty):
                if df.empty:
                    st.warning(f"`{filename}` is missing or unreadable.")
                else:
                    render_dataframe(df.head(20))
                    make_download_button(filename)

    if pngs:
        with st.expander("PNG files detected but hidden from presentation view.", expanded=False):
            for png_path in pngs:
                st.write(png_path.name)
