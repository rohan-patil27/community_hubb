import streamlit as st

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700&display=swap');

/* ── Hide 'Press Enter to apply' Streamlit Input Instructions ── */
[data-testid="stInputInstructions"],
.stInputInstructions,
[aria-label="Input instructions"],
div[data-baseweb="input"] + div,
small[data-testid="stInputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    pointer-events: none !important;
}

/* ── Hide map attribution gray box ── */
.deck-widget-attribution, .mapboxgl-ctrl-attrib, .deck-widget {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
"""

THEME_MIDNIGHT = """
/* ── Midnight Dark (Default Theme) ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0d1117 !important;
    color: #e6edf3 !important;
}
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1200px; }

/* ── Streamlit Chrome Overrides ── */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    z-index: 999999 !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    color: #60a5fa !important;
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar User Card ── */
.sidebar-user-card {
    background: #1a2332;
    border: 1px solid #2d4a8a;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.sidebar-user-card .user-card-name {
    font-weight: 600;
    color: #e6edf3 !important;
    margin-top: 0.3rem;
    font-size: 0.95rem;
}
.sidebar-user-card .user-card-loc {
    color: #8b949e !important;
    font-size: 0.8rem;
}
.sidebar-user-card .user-card-role {
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: #60a5fa !important;
    font-weight: 600;
}

/* ── Main Header ── */
.main-header {
    background: linear-gradient(135deg, #1a2744 0%, #0d1b3e 50%, #1a1a3e 100%);
    border: 1px solid #2d4a8a;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 32px rgba(59,130,246,0.15);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -10%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.header-content {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    position: relative;
    z-index: 1;
}
.header-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px rgba(59,130,246,0.6));
}
.main-header h1 {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
    line-height: 1.2;
    background: linear-gradient(90deg, #fff 60%, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.main-header p {
    color: #94a3b8 !important;
    font-size: 0.9rem;
    margin: 0.25rem 0 0;
}

/* ── Buttons ── */
[data-testid="stButton"] > button,
[data-testid="stFormSubmitButton"] > button {
    background: #161b22;
    color: #e6edf3 !important;
    border: 1px solid #30363d;
    border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
    transition: all 0.2s ease;
    width: 100%;
}
[data-testid="stButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: #1f2937;
    border-color: #3b82f6;
    color: #60a5fa !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(59,130,246,0.2);
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    border: 1px solid #3b82f6 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1.5rem !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    box-shadow: 0 6px 24px rgba(59,130,246,0.4) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stButton"] > button {
    white-space: nowrap !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 0.5rem !important;
    text-overflow: ellipsis !important;
    overflow: hidden !important;
}

/* ── Hero Section ── */
.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(180deg, #0d1117 0%, #0d1b3e 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid #1e3a5f;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 400px;
    background: radial-gradient(ellipse, rgba(59,130,246,0.12) 0%, transparent 70%);
}
.hero-section h2 {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 0.75rem !important;
    position: relative;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-section p {
    font-size: 1.1rem;
    color: #94a3b8 !important;
    max-width: 600px;
    margin: 0 auto !important;
    position: relative;
}

/* ── Stat Cards ── */
.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.25s ease;
    cursor: default;
}
.stat-card:hover {
    border-color: #3b82f6;
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(59,130,246,0.2);
    background: #1a2332;
}
.stat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #60a5fa;
}
.stat-label { font-size: 0.8rem; color: #8b949e; margin-top: 0.2rem; }

/* ── Feature Cards ── */
.feature-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.feature-card:hover {
    border-color: #3b82f6;
    transform: translateX(4px);
    box-shadow: -4px 0 20px rgba(59,130,246,0.15);
    background: #1a2332;
}
.feature-card h3 {
    color: #e6edf3 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}
.feature-card p { color: #8b949e; font-size: 0.88rem; margin: 0; }

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #21262d;
}
.section-header-icon {
    font-size: 1.6rem;
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #1e3a5f, #1a2744);
    border: 1px solid #2d4a8a;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
}
.section-header h2 {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #e6edf3 !important;
    margin: 0 !important;
}
.section-header p { color: #8b949e; font-size: 0.85rem; margin: 0; }

/* ── Job Cards ── */
.job-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.job-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 3px 0 0 3px;
}
.job-card:hover {
    border-color: #2d4a8a;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(59,130,246,0.15);
    background: #1a2332;
}
.job-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.3rem;
}
.job-company { color: #60a5fa; font-size: 0.9rem; font-weight: 500; }
.job-desc { color: #cbd5e1; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.6rem; }
.job-why-match {
    background: #0d1117;
    border-left: 3px solid #3b82f6;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 0.6rem 0;
    font-size: 0.82rem;
    color: #94a3b8;
}
.why-match-skills {
    color: #34d399 !important;
    font-weight: 600;
}
.job-meta {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin: 0.75rem 0;
}
.badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
}
.badge-blue { background: #1e3a5f; color: #60a5fa; border: 1px solid #2d4a8a; }
.badge-green { background: #0d2d1a; color: #34d399; border: 1px solid #065f46; }
.badge-purple { background: #2d1b69; color: #a78bfa; border: 1px solid #4c1d95; }
.badge-orange { background: #3d1f00; color: #fb923c; border: 1px solid #7c2d12; }
.badge-red { background: #2d1515; color: #f87171; border: 1px solid #7f1d1d; }
.match-score {
    position: absolute; top: 1rem; right: 1rem;
    background: linear-gradient(135deg, #1e3a5f, #2d1b69);
    border: 1px solid #3b82f6;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: #60a5fa;
}
.match-bar-container {
    background: #21262d;
    border-radius: 4px;
    height: 6px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.match-bar {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transition: width 0.6s ease;
}

/* ── Scheme Cards ── */
.scheme-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.scheme-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #34d399, #059669);
    border-radius: 3px 0 0 3px;
}
.scheme-card:hover {
    border-color: #065f46;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(52,211,153,0.1);
    background: #0d2018;
}
.scheme-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #e6edf3;
}
.scheme-benefit {
    background: #0d2d1a;
    border: 1px solid #065f46;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    color: #34d399;
}

/* ── Emergency Cards ── */
.emergency-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.emergency-card.critical {
    border-color: #7f1d1d;
}
.emergency-card.critical::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #ef4444, #dc2626);
}
.emergency-card:not(.critical)::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #f59e0b, #d97706);
}
.emergency-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(239,68,68,0.1);
}
.phone-badge {
    display: inline-block;
    background: #1a2744;
    border: 1px solid #2d4a8a;
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: #60a5fa;
    margin: 0.3rem 0;
}

/* ── Forms ── */
.form-container {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 2rem;
    max-width: 600px;
    margin: 0 auto;
}
.form-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e6edf3;
    margin-bottom: 1.5rem;
    text-align: center;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextArea"] textarea {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Streamlit Expander ── */
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    background: #161b22 !important;
    color: #e6edf3 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary:hover {
    background: #1f2937 !important;
    color: #60a5fa !important;
}
[data-testid="stExpander"] summary svg {
    fill: #60a5fa !important;
    color: #60a5fa !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #e6edf3 !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #161b22 !important;
    color: #e6edf3 !important;
}

/* ── Admin Dashboard & Metrics ── */
.metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
    transition: all 0.2s;
}
.metric-card:hover { border-color: #3b82f6; transform: translateY(-3px); }
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label { color: #8b949e; font-size: 0.85rem; margin-top: 0.3rem; }
.metric-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }

/* ── Info/Success/Warning boxes ── */
.info-box {
    background: #1a2744;
    border: 1px solid #2d4a8a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
}
.success-box {
    background: #0d2d1a;
    border: 1px solid #065f46;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    color: #34d399;
}
.warning-box {
    background: #2d1f00;
    border: 1px solid #78350f;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    color: #fbbf24;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #161b22;
    border-radius: 14px;
    padding: 8px 10px;
    gap: 10px !important;
    border: 1px solid #21262d;
    flex-wrap: wrap !important;
    margin-bottom: 1.5rem;
}
[data-testid="stTabs"] [role="tab"] {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
    border-radius: 10px !important;
    font-weight: 600;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.1rem !important;
    margin: 3px 4px !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    border-color: #3b82f6 !important;
    color: #60a5fa !important;
    background: #192338 !important;
    transform: translateY(-1px);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a5f, #2563eb) !important;
    color: #ffffff !important;
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35) !important;
}

/* ── Divider & Scrollbar ── */
hr { border-color: #21262d !important; margin: 1.5rem 0 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* ── Streamlit Selectbox / MultiSelect Overrides ── */
[data-testid="stMarkdownContainer"] p { color: #e6edf3; }
.stAlert { border-radius: 10px; }
[data-testid="stSelectbox"] > div > div {
    background: #0d1117 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
    cursor: pointer !important;
}
[data-testid="stSelectbox"] * { cursor: pointer !important; }
[data-testid="stSelectbox"] input { caret-color: transparent !important; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

[data-testid="stMultiSelect"] span[data-baseweb="tag"],
[data-baseweb="tag"] {
    background: #1e3a5f !important;
    border: 1px solid #2d4a8a !important;
    border-radius: 6px !important;
    color: #60a5fa !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #60a5fa !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] [data-baseweb="icon"],
[data-baseweb="tag"] svg {
    fill: #93c5fd !important;
    color: #93c5fd !important;
}
[data-testid="stMultiSelect"] > div > div {
    border-color: #30363d !important;
    background: #0d1117 !important;
}
[data-testid="stMultiSelect"] > div > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
"""

THEME_PEARL_WHITE = """
/* ── Pearl White (Clean Light Theme) ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc !important;
    color: #0f172a !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #1e293b !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1200px; }

/* ── Streamlit Chrome Overrides ── */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    z-index: 999999 !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    color: #2563eb !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar User Card ── */
.sidebar-user-card {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.sidebar-user-card .user-card-name {
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-top: 0.3rem;
    font-size: 0.95rem;
}
.sidebar-user-card .user-card-loc {
    color: #475569 !important;
    font-size: 0.8rem;
}
.sidebar-user-card .user-card-role {
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: #2563eb !important;
    font-weight: 700;
}

/* ── Main Header ── */
.main-header {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #3b82f6 100%) !important;
    border: 1px solid #60a5fa !important;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(37,99,235,0.18) !important;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -10%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(255,255,255,0.2) 0%, transparent 70%);
    pointer-events: none;
}
.header-content {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    position: relative;
    z-index: 1;
}
.header-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px rgba(255,255,255,0.6));
}
.main-header h1 {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
    line-height: 1.2;
    background: linear-gradient(90deg, #ffffff 60%, #dbeafe) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.main-header p {
    color: #e0e7ff !important;
    font-size: 0.9rem;
    margin: 0.25rem 0 0;
}

/* ── Buttons ── */
[data-testid="stButton"] > button,
[data-testid="stFormSubmitButton"] > button {
    background: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    width: 100%;
}
[data-testid="stButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: #f1f5f9 !important;
    border-color: #2563eb !important;
    color: #2563eb !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37,99,235,0.15) !important;
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    border: 1px solid #1d4ed8 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stButton"] > button {
    white-space: nowrap !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 0.5rem !important;
    text-overflow: ellipsis !important;
    overflow: hidden !important;
}

/* ── Hero Section ── */
.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid #bfdbfe !important;
    box-shadow: 0 4px 20px rgba(37,99,235,0.08) !important;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 400px;
    background: radial-gradient(ellipse, rgba(37,99,235,0.08) 0%, transparent 70%);
}
.hero-section h2 {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.75rem !important;
    position: relative;
    background: linear-gradient(90deg, #1e40af, #6366f1, #d946ef) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.hero-section p {
    font-size: 1.1rem;
    color: #475569 !important;
    max-width: 600px;
    margin: 0 auto !important;
    position: relative;
}

/* ── Stat Cards ── */
.stat-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    cursor: default;
}
.stat-card:hover {
    border-color: #2563eb !important;
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(37,99,235,0.15) !important;
    background: #f8fafc !important;
}
.stat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #2563eb !important;
}
.stat-label { font-size: 0.8rem; color: #475569 !important; margin-top: 0.2rem; }

/* ── Feature Cards ── */
.feature-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.feature-card:hover {
    border-color: #2563eb !important;
    transform: translateX(4px);
    box-shadow: -4px 0 20px rgba(37,99,235,0.12) !important;
    background: #f8fafc !important;
}
.feature-card h3 {
    color: #0f172a !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}
.feature-card p { color: #475569 !important; font-size: 0.88rem; margin: 0; }

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e2e8f0 !important;
}
.section-header-icon {
    font-size: 1.6rem;
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #dbeafe, #eff6ff) !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
}
.section-header h2 {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin: 0 !important;
}
.section-header p { color: #475569 !important; font-size: 0.85rem; margin: 0; }

/* ── Job Cards ── */
.job-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.job-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #2563eb, #8b5cf6) !important;
    border-radius: 3px 0 0 3px;
}
.job-card:hover {
    border-color: #93c5fd !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(37,99,235,0.12) !important;
    background: #f8fafc !important;
}
.job-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-bottom: 0.3rem;
}
.job-company { color: #2563eb !important; font-size: 0.9rem; font-weight: 600; }
.job-desc { color: #475569 !important; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.6rem; }
.job-why-match {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-left: 3px solid #2563eb !important;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 0.6rem 0;
    font-size: 0.82rem;
    color: #1e3a8a !important;
}
.why-match-skills {
    color: #059669 !important;
    font-weight: 700 !important;
}
.job-meta {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin: 0.75rem 0;
}
.badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
}
.badge-blue { background: #dbeafe !important; color: #1d4ed8 !important; border: 1px solid #bfdbfe !important; }
.badge-green { background: #dcfce7 !important; color: #15803d !important; border: 1px solid #bbf7d0 !important; }
.badge-purple { background: #f3e8ff !important; color: #7e22ce !important; border: 1px solid #e9d5ff !important; }
.badge-orange { background: #ffedd5 !important; color: #c2410c !important; border: 1px solid #fed7aa !important; }
.badge-red { background: #fee2e2 !important; color: #b91c1c !important; border: 1px solid #fecaca !important; }
.match-score {
    position: absolute; top: 1rem; right: 1rem;
    background: linear-gradient(135deg, #eff6ff, #f3e8ff) !important;
    border: 1px solid #93c5fd !important;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: #1d4ed8 !important;
}
.match-bar-container {
    background: #e2e8f0 !important;
    border-radius: 4px;
    height: 6px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.match-bar {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #2563eb, #8b5cf6) !important;
    transition: width 0.6s ease;
}

/* ── Scheme Cards ── */
.scheme-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.scheme-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #10b981, #059669) !important;
    border-radius: 3px 0 0 3px;
}
.scheme-card:hover {
    border-color: #a7f3d0 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(16,185,129,0.12) !important;
    background: #f0fdf4 !important;
}
.scheme-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #0f172a !important;
}
.scheme-benefit {
    background: #dcfce7 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    color: #15803d !important;
}

/* ── Emergency Cards ── */
.emergency-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.emergency-card.critical {
    border-color: #fca5a5 !important;
}
.emergency-card.critical::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #ef4444, #dc2626) !important;
}
.emergency-card:not(.critical)::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #f59e0b, #d97706) !important;
}
.emergency-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(239,68,68,0.12) !important;
}
.phone-badge {
    display: inline-block;
    background: #dbeafe !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: #1d4ed8 !important;
    margin: 0.3rem 0;
}

/* ── Streamlit Expander in Light Mode ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    margin-bottom: 1rem !important;
}
[data-testid="stExpander"] summary {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    border-bottom: 1px solid #e2e8f0 !important;
    padding: 0.6rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
    background: #e2e8f0 !important;
    color: #2563eb !important;
}
[data-testid="stExpander"] summary svg,
[data-testid="stExpander"] summary [data-testid="stIconMaterial"] {
    fill: #2563eb !important;
    color: #2563eb !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #0f172a !important;
    font-weight: 700 !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #ffffff !important;
    color: #0f172a !important;
    padding: 1.2rem !important;
}

/* ── Forms ── */
.form-container {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px;
    padding: 2rem;
    max-width: 600px;
    margin: 0 auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
}
.form-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a !important;
    margin-bottom: 1.5rem;
    text-align: center;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}
label, [data-testid="stMarkdownContainer"] label, [data-testid="stWidgetLabel"] label {
    color: #1e293b !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

/* ── Admin Dashboard & Metrics ── */
.metric-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.metric-card:hover { border-color: #2563eb !important; transform: translateY(-3px); }
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.metric-label { color: #475569 !important; font-size: 0.85rem; margin-top: 0.3rem; }
.metric-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }

/* ── Info/Success/Warning boxes ── */
.info-box {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin: 0.75rem 0;
    color: #1e40af !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.06) !important;
}
.info-box * {
    color: #1e293b !important;
}
.info-box [style*="color:#e6edf3"], .info-box [style*="color: #e6edf3"],
.info-box [style*="color:#ffffff"], .info-box [style*="color: #ffffff"] {
    color: #0f172a !important;
    font-weight: 700 !important;
}
.info-box [style*="color:#8b949e"], .info-box [style*="color: #8b949e"],
.info-box [style*="color:#94a3b8"], .info-box [style*="color: #94a3b8"],
.info-box [style*="color:#cbd5e1"], .info-box [style*="color: #cbd5e1"] {
    color: #475569 !important;
}
.info-box [style*="color:#60a5fa"], .info-box [style*="color: #60a5fa"] {
    color: #2563eb !important;
    font-weight: 700 !important;
}

.success-box {
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    color: #15803d !important;
}
.warning-box {
    background: #fffbeb !important;
    border: 1px solid #fde68a !important;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    color: #b45309 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #f1f5f9 !important;
    border-radius: 14px;
    padding: 8px 10px;
    gap: 10px !important;
    border: 1px solid #e2e8f0 !important;
    flex-wrap: wrap !important;
    margin-bottom: 1.5rem;
}
[data-testid="stTabs"] [role="tab"] {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #475569 !important;
    border-radius: 10px !important;
    font-weight: 600;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.1rem !important;
    margin: 3px 4px !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
    background: #eff6ff !important;
    transform: translateY(-1px);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #ffffff !important;
    border: 1px solid #1d4ed8 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
}

/* ── Divider & Scrollbar ── */
hr { border-color: #e2e8f0 !important; margin: 1.5rem 0 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f8fafc; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── Streamlit Selectbox / MultiSelect Overrides ── */
[data-testid="stMarkdownContainer"] p { color: #1e293b !important; }
.stAlert { border-radius: 10px; }
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    color: #0f172a !important;
}
[data-testid="stSelectbox"] * {
    color: #0f172a !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"],
[data-baseweb="tag"] {
    background: #dbeafe !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 6px !important;
    color: #1d4ed8 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #1d4ed8 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] [data-baseweb="icon"],
[data-baseweb="tag"] svg {
    fill: #2563eb !important;
    color: #2563eb !important;
}
[data-testid="stMultiSelect"] > div > div {
    border-color: #cbd5e1 !important;
    background: #ffffff !important;
}
[data-testid="stMultiSelect"] > div > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}

/* ── Checkboxes and Radios ── */
[data-testid="stCheckbox"] label span,
[data-testid="stRadio"] label span {
    color: #0f172a !important;
    font-weight: 500 !important;
}

/* ── Universal Contrast Overrides for Light Mode ── */
[style*="background:#161b22"], [style*="background: #161b22"],
[style*="background:#1a2332"], [style*="background: #1a2332"],
[style*="background:#0d1117"], [style*="background: #0d1117"] {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    color: #0f172a !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
[style*="background:#1a2744"], [style*="background: #1a2744"],
[style*="background:#1e3a5f"], [style*="background: #1e3a5f"] {
    background: #eff6ff !important;
    border-color: #bfdbfe !important;
    color: #1e40af !important;
}
[style*="background:#0d2d1a"], [style*="background: #0d2d1a"] {
    background: #f0fdf4 !important;
    border-color: #bbf7d0 !important;
    color: #15803d !important;
}
[style*="background:#2d1f00"], [style*="background: #2d1f00"],
[style*="background:#3d1f00"], [style*="background: #3d1f00"] {
    background: #fffbeb !important;
    border-color: #fde68a !important;
    color: #b45309 !important;
}

/* Text overrides */
[data-testid="stMarkdownContainer"] [style*="color:#e6edf3"],
[data-testid="stMarkdownContainer"] [style*="color: #e6edf3"] {
    color: #0f172a !important;
}
[data-testid="stMarkdownContainer"] [style*="color:#8b949e"],
[data-testid="stMarkdownContainer"] [style*="color: #8b949e"],
[data-testid="stMarkdownContainer"] [style*="color:#94a3b8"],
[data-testid="stMarkdownContainer"] [style*="color: #94a3b8"],
[data-testid="stMarkdownContainer"] [style*="color:#cbd5e1"],
[data-testid="stMarkdownContainer"] [style*="color: #cbd5e1"] {
    color: #475569 !important;
}
[data-testid="stMarkdownContainer"] [style*="color:#60a5fa"],
[data-testid="stMarkdownContainer"] [style*="color: #60a5fa"] {
    color: #2563eb !important;
}

/* Ensure Header and Primary button colors stay bright white */
.main-header, .main-header *, 
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button[kind="primary"] *,
[data-testid="stFormSubmitButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"] * {
    color: #ffffff !important;
}
.main-header p {
    color: #e0e7ff !important;
}
"""

THEME_EMERALD_GREEN = """
/* ── Emerald Mint (Fresh Green Theme) ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #051410 !important;
    color: #ecfdf5 !important;
}
[data-testid="stSidebar"] {
    background: #0a221b !important;
    border-right: 1px solid #134e4a !important;
}
[data-testid="stSidebar"] * { color: #ecfdf5 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1200px; }

/* ── Streamlit Chrome Overrides ── */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    z-index: 999999 !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    color: #34d399 !important;
    background: #0a221b !important;
    border: 1px solid #134e4a !important;
    border-radius: 8px !important;
}
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar User Card ── */
.sidebar-user-card {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.sidebar-user-card .user-card-name {
    font-weight: 600;
    color: #ecfdf5 !important;
    margin-top: 0.3rem;
    font-size: 0.95rem;
}
.sidebar-user-card .user-card-loc {
    color: #a7f3d0 !important;
    font-size: 0.8rem;
}
.sidebar-user-card .user-card-role {
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: #34d399 !important;
    font-weight: 600;
}

/* ── Main Header ── */
.main-header {
    background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #022c22 100%) !important;
    border: 1px solid #059669 !important;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 32px rgba(16,185,129,0.2) !important;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -10%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(52,211,153,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.header-content {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    position: relative;
    z-index: 1;
}
.header-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px rgba(52,211,153,0.6));
}
.main-header h1 {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
    line-height: 1.2;
    background: linear-gradient(90deg, #ffffff 60%, #34d399) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.main-header p {
    color: #a7f3d0 !important;
    font-size: 0.9rem;
    margin: 0.25rem 0 0;
}

/* ── Buttons ── */
[data-testid="stButton"] > button,
[data-testid="stFormSubmitButton"] > button {
    background: #0b251e !important;
    color: #ecfdf5 !important;
    border: 1px solid #134e4a !important;
    border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
    transition: all 0.2s ease;
    width: 100%;
}
[data-testid="stButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: #134e4a !important;
    border-color: #10b981 !important;
    color: #34d399 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(16,185,129,0.25) !important;
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #059669, #047857) !important;
    border: 1px solid #10b981 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1.5rem !important;
    box-shadow: 0 4px 18px rgba(16,185,129,0.3) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    box-shadow: 0 6px 24px rgba(16,185,129,0.45) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stButton"] > button {
    white-space: nowrap !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 0.5rem !important;
    text-overflow: ellipsis !important;
    overflow: hidden !important;
}

/* ── Hero Section ── */
.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(180deg, #051410 0%, #064e3b 100%) !important;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid #047857 !important;
    box-shadow: 0 4px 24px rgba(16,185,129,0.15) !important;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 400px;
    background: radial-gradient(ellipse, rgba(52,211,153,0.15) 0%, transparent 70%);
}
.hero-section h2 {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 0.75rem !important;
    position: relative;
    background: linear-gradient(90deg, #34d399, #6ee7b7, #fef08a) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.hero-section p {
    font-size: 1.1rem;
    color: #a7f3d0 !important;
    max-width: 600px;
    margin: 0 auto !important;
    position: relative;
}

/* ── Stat Cards ── */
.stat-card {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.25s ease;
    cursor: default;
}
.stat-card:hover {
    border-color: #10b981 !important;
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(16,185,129,0.2) !important;
    background: #0f3329 !important;
}
.stat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #34d399 !important;
}
.stat-label { font-size: 0.8rem; color: #a7f3d0 !important; margin-top: 0.2rem; }

/* ── Feature Cards ── */
.feature-card {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.feature-card:hover {
    border-color: #10b981 !important;
    transform: translateX(4px);
    box-shadow: -4px 0 20px rgba(16,185,129,0.2) !important;
    background: #0f3329 !important;
}
.feature-card h3 {
    color: #ecfdf5 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}
.feature-card p { color: #a7f3d0 !important; font-size: 0.88rem; margin: 0; }

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #134e4a !important;
}
.section-header-icon {
    font-size: 1.6rem;
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #064e3b, #042f2e) !important;
    border: 1px solid #059669 !important;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
}
.section-header h2 {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #ecfdf5 !important;
    margin: 0 !important;
}
.section-header p { color: #a7f3d0 !important; font-size: 0.85rem; margin: 0; }

/* ── Job Cards ── */
.job-card {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.job-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #10b981, #059669) !important;
    border-radius: 3px 0 0 3px;
}
.job-card:hover {
    border-color: #059669 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(16,185,129,0.2) !important;
    background: #0f3329 !important;
}
.job-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #ecfdf5 !important;
    margin-bottom: 0.3rem;
}
.job-company { color: #34d399 !important; font-size: 0.9rem; font-weight: 600; }
.job-desc { color: #ecfdf5 !important; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.6rem; }
.job-why-match {
    background: #051410 !important;
    border: 1px solid #134e4a !important;
    border-left: 3px solid #10b981 !important;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 0.6rem 0;
    font-size: 0.82rem;
    color: #a7f3d0 !important;
}
.why-match-skills {
    color: #34d399 !important;
    font-weight: 600 !important;
}
.job-meta {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin: 0.75rem 0;
}
.badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
}
.badge-blue { background: #064e3b !important; color: #34d399 !important; border: 1px solid #059669 !important; }
.badge-green { background: #042f2e !important; color: #6ee7b7 !important; border: 1px solid #10b981 !important; }
.badge-purple { background: #1f1d36 !important; color: #c084fc !important; border: 1px solid #581c87 !important; }
.badge-orange { background: #3d1f00 !important; color: #fb923c !important; border: 1px solid #7c2d12 !important; }
.badge-red { background: #2d1515 !important; color: #f87171 !important; border: 1px solid #7f1d1d !important; }
.match-score {
    position: absolute; top: 1rem; right: 1rem;
    background: linear-gradient(135deg, #064e3b, #042f2e) !important;
    border: 1px solid #10b981 !important;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: #34d399 !important;
}
.match-bar-container {
    background: #134e4a !important;
    border-radius: 4px;
    height: 6px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.match-bar {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #10b981, #34d399) !important;
    transition: width 0.6s ease;
}

/* ── Streamlit Expander in Emerald Mode ── */
[data-testid="stExpander"] {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    background: #0b251e !important;
    color: #ecfdf5 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary:hover {
    background: #0f3329 !important;
    color: #34d399 !important;
}
[data-testid="stExpander"] summary svg {
    fill: #34d399 !important;
    color: #34d399 !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #ecfdf5 !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #0b251e !important;
    color: #ecfdf5 !important;
}

/* ── Forms ── */
.form-container {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 16px;
    padding: 2rem;
    max-width: 600px;
    margin: 0 auto;
}
.form-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ecfdf5 !important;
    margin-bottom: 1.5rem;
    text-align: center;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextArea"] textarea {
    background: #051410 !important;
    border: 1px solid #134e4a !important;
    border-radius: 8px !important;
    color: #ecfdf5 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.2) !important;
}
label, [data-testid="stMarkdownContainer"] label {
    color: #a7f3d0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Admin Dashboard & Metrics ── */
.metric-card {
    background: #0b251e !important;
    border: 1px solid #134e4a !important;
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
    transition: all 0.2s;
}
.metric-card:hover { border-color: #10b981 !important; transform: translateY(-3px); }
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #34d399, #6ee7b7) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.metric-label { color: #a7f3d0 !important; font-size: 0.85rem; margin-top: 0.3rem; }
.metric-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #0b251e !important;
    border-radius: 14px;
    padding: 8px 10px;
    gap: 10px !important;
    border: 1px solid #134e4a !important;
    flex-wrap: wrap !important;
    margin-bottom: 1.5rem;
}
[data-testid="stTabs"] [role="tab"] {
    background: #051410 !important;
    border: 1px solid #134e4a !important;
    color: #a7f3d0 !important;
    border-radius: 10px !important;
    font-weight: 600;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.1rem !important;
    margin: 3px 4px !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    border-color: #10b981 !important;
    color: #34d399 !important;
    background: #0f3329 !important;
    transform: translateY(-1px);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #064e3b, #059669) !important;
    color: #ffffff !important;
    border: 1px solid #10b981 !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.35) !important;
}

/* ── Overrides for Selectbox / MultiSelect ── */
[data-testid="stMarkdownContainer"] p { color: #ecfdf5 !important; }
[data-testid="stSelectbox"] > div > div {
    background: #051410 !important;
    border-color: #134e4a !important;
    color: #ecfdf5 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"],
[data-baseweb="tag"] {
    background: #064e3b !important;
    border: 1px solid #059669 !important;
    border-radius: 6px !important;
    color: #34d399 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #34d399 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] [data-baseweb="icon"],
[data-baseweb="tag"] svg {
    fill: #6ee7b7 !important;
    color: #6ee7b7 !important;
}
[data-testid="stMultiSelect"] > div > div {
    border-color: #134e4a !important;
    background: #051410 !important;
}
[data-testid="stMultiSelect"] > div > div:focus-within {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.2) !important;
}
hr { border-color: #134e4a !important; margin: 1.5rem 0 !important; }
::-webkit-scrollbar-track { background: #051410; }
::-webkit-scrollbar-thumb { background: #134e4a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #059669; }
"""

def get_theme_css(theme="midnight"):
    if theme == "pearl_white":
        return THEME_PEARL_WHITE
    elif theme == "emerald_green":
        return THEME_EMERALD_GREEN
    return THEME_MIDNIGHT

def load_styles(theme="midnight"):
    theme_css = get_theme_css(theme)
    full_css = "<style>\n" + BASE_CSS + "\n" + theme_css + "\n</style>"
    st.markdown(full_css, unsafe_allow_html=True)
