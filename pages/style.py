"""
Shared styling for NEXDOM — injected at the top of every page.
"""
import streamlit as st


NEXDOM_CSS = """
<style>
/* ================================================
   GLOBAL THEME — NEXDOM
   Primary: #1A56DB (deep blue)
   Accent:  #F59E0B (amber)
   Surface: #F8FAFC
   Text:    #1E293B
================================================ */

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
}
[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #EF4444, #DC2626) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #DC2626, #B91C1C) !important;
    transform: translateY(-1px);
}
[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}
[data-testid="stSidebar"] .stSuccess {
    background-color: #064E3B !important;
    border: 1px solid #065F46 !important;
    color: #D1FAE5 !important;
}
[data-testid="stSidebar"] .stInfo {
    background-color: #1E3A5F !important;
    border: 1px solid #1D4ED8 !important;
    color: #BFDBFE !important;
}

/* ---- Main area background ---- */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* ---- Page title style ---- */
h1 {
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    font-size: 2rem !important;
    border-bottom: 3px solid #1A56DB;
    padding-bottom: 0.4rem;
    margin-bottom: 0.5rem !important;
}

h2 {
    color: #1E293B !important;
    font-weight: 700 !important;
}

h3 {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* ---- Metric cards ---- */
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
}

/* ---- Primary action buttons ---- */
div.stButton > button[kind="primary"],
div.stButton > button {
    background: linear-gradient(135deg, #1A56DB, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 6px rgba(26, 86, 219, 0.25) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
    box-shadow: 0 4px 12px rgba(26, 86, 219, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* ---- Form inputs ---- */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] {
    border-radius: 8px !important;
    border: 1.5px solid #CBD5E1 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="textarea"] textarea:focus {
    border-color: #1A56DB !important;
    box-shadow: 0 0 0 3px rgba(26,86,219,0.12) !important;
}

/* ---- Expanders ---- */
[data-testid="stExpander"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    background: white !important;
    margin-bottom: 0.6rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    background: #F8FAFC !important;
    font-weight: 600 !important;
    padding: 0.8rem 1rem !important;
    color: #1E293B !important;
}
[data-testid="stExpander"] summary:hover {
    background: #EFF6FF !important;
}

/* ---- Tabs ---- */
[data-baseweb="tab-list"] {
    background: #F1F5F9 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    border-radius: 7px !important;
    font-weight: 500 !important;
    color: #64748B !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: white !important;
    color: #1A56DB !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* ---- Alerts ---- */
.stSuccess {
    background-color: #ECFDF5 !important;
    border-left: 4px solid #10B981 !important;
    border-radius: 8px !important;
    color: #065F46 !important;
}
.stWarning {
    background-color: #FFFBEB !important;
    border-left: 4px solid #F59E0B !important;
    border-radius: 8px !important;
    color: #78350F !important;
}
.stError {
    background-color: #FEF2F2 !important;
    border-left: 4px solid #EF4444 !important;
    border-radius: 8px !important;
    color: #7F1D1D !important;
}
.stInfo {
    background-color: #EFF6FF !important;
    border-left: 4px solid #1A56DB !important;
    border-radius: 8px !important;
    color: #1E3A8A !important;
}

/* ---- DataFrames ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ---- Divider ---- */
hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 1.25rem 0 !important;
}

/* ---- Container borders ---- */
[data-testid="stContainer"] {
    border-radius: 12px !important;
}

/* ---- Selectbox ---- */
div[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border: 1.5px solid #CBD5E1 !important;
}
</style>
"""


def inject_global_css():
    """Call this at the top of every page to apply the shared theme."""
    st.markdown(NEXDOM_CSS, unsafe_allow_html=True)


# Helper: Styled section header (replaces plain st.subheader)

def section_header(title: str, subtitle: str = ""):
    subtitle_html = f"<p style='color:#64748B; font-size:0.9rem; margin:0 0 0.5rem 0;'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div style='margin: 1.2rem 0 0.8rem 0;'>
          <h3 style='color:#0F172A; font-weight:700; margin:0 0 2px 0;'>{title}</h3>
          {subtitle_html}
          <div style='width:40px; height:3px; background:linear-gradient(90deg,#1A56DB,#60A5FA);
                      border-radius:2px; margin-top:4px;'></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Helper: Styled info/stat card

def stat_card(label: str, value, icon: str = "", color: str = "#1A56DB"):
    st.markdown(
        f"""
        <div style='background:white; border:1px solid #E2E8F0; border-radius:12px;
                    padding:1rem 1.2rem; box-shadow:0 1px 4px rgba(0,0,0,0.06);
                    border-top: 3px solid {color};'>
          <div style='font-size:1.6rem; margin-bottom:2px;'>{icon}</div>
          <div style='font-size:1.8rem; font-weight:800; color:#0F172A;'>{value}</div>
          <div style='font-size:0.75rem; font-weight:600; color:#64748B;
                      text-transform:uppercase; letter-spacing:0.5px;'>{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Helper: Page banner / hero block

def page_banner(title: str, subtitle: str, icon: str = "🏠"):
    st.markdown(
        f"""
        <div style='
            background: white;
            border: 1px solid #E2E8F0;
            border-left: 5px solid #1A56DB;
            border-radius: 12px;
            padding: 1.4rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            display: flex;
            align-items: center;
            gap: 1.2rem;
        '>
          <div style='font-size: 2.2rem; flex-shrink: 0;'>{icon}</div>
          <div>
            <h1 style='
                color: #0F172A !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 0 4px 0 !important;
                font-size: 1.6rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.3px;
            '>{title}</h1>
            <p style='
                color: #64748B;
                margin: 0;
                font-size: 0.9rem;
                line-height: 1.4;
            '>{subtitle}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
