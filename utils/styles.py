Shared CSS styles and UI constants for the platform.
"""

CATEGORIES = [
    "Technology",
    "Music",
    "Food & Drink",
    "Arts",
    "Health & Wellness",
    "Entertainment",
    "Sports",
    "Education",
    "Other",
]

CATEGORY_EMOJIS = {
    "Technology":        "💻",
    "Music":             "🎵",
    "Food & Drink":      "🍽️",
    "Arts":              "🎨",
    "Health & Wellness": "🧘",
    "Entertainment":     "🎭",
    "Sports":            "🏆",
    "Education":         "📚",
    "Other":             "📌",
}

CUSTOM_CSS = """
<style>
/*  Google Font ────────*/
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

/* ── Global reset ────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Page background ─────────────────────────────────── */
.stApp {
    background: #0F0F1A;
}

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #13131F !important;
    border-right: 1px solid #1E1E30;
}
[data-testid="stSidebar"] .stRadio label {
    color: #C4C4D4 !important;
    font-size: 14px;
    font-weight: 500;
}

/* ── Main content area ───────────────────────────────── */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* ── Hero section ────────────────────────────────────── */
.hero-section {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid #2a2a4a;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0 0 1rem 0;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(90deg, #6366F1, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #9898B8;
    margin: 0 0 2rem 0;
    line-height: 1.6;
    max-width: 600px;
}

/* ── Stat cards ──────────────────────────────────────── */
.stat-card {
    background: #16162A;
    border: 1px solid #2A2A40;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover {
    border-color: #6366F1;
    transform: translateY(-2px);
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-label {
    font-size: 0.8rem;
    color: #6B6B8A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

/* ── Section header ──────────────────────────────────── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 1.2rem 0;
    letter-spacing: -0.01em;
}
.section-sub {
    font-size: 0.9rem;
    color: #7070A0;
    margin-top: -0.8rem;
    margin-bottom: 1.4rem;
}

/* ── Event cards ─────────────────────────────────────── */
.event-card {
    background: #16162A;
    border: 1px solid #2A2A40;
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    position: relative;
}
.event-card:hover {
    border-color: #6366F1;
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.15);
}
.event-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #E0E0FF;
    margin: 0 0 0.5rem 0;
}
.event-meta {
    font-size: 0.82rem;
    color: #6868A0;
    display: flex;
    gap: 1rem;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
}
.event-description {
    font-size: 0.85rem;
    color: #9898B8;
    line-height: 1.5;
    margin: 0.6rem 0 0 0;
}
.category-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    background: #1E1E38;
    color: #9898C8;
    border: 1px solid #2E2E50;
    margin-bottom: 0.6rem;
}

/* ── Nav cards ───────────────────────────────────────── */
.nav-card {
    background: #16162A;
    border: 1px solid #2A2A40;
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    height: 100%;
}
.nav-card:hover {
    border-color: #6366F1;
    background: #1E1E38;
    transform: translateY(-3px);
}
.nav-card-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
}
.nav-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #E0E0FF;
    margin-bottom: 0.3rem;
}
.nav-card-desc {
    font-size: 0.8rem;
    color: #6868A0;
}

/* ── Form styles ─────────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stDateInput input {
    background: #16162A !important;
    border: 1px solid #2A2A40 !important;
    border-radius: 10px !important;
    color: #E0E0FF !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ── Primary button ──────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.88 !important;
}

/* ── Secondary button ────────────────────────────────── */
.stButton > button {
    background: #1E1E38 !important;
    color: #C4C4D4 !important;
    border: 1px solid #2A2A40 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: border-color 0.2s !important;
}
.stButton > button:hover {
    border-color: #6366F1 !important;
    color: #E0E0FF !important;
}

/* ── Success / info alerts ───────────────────────────── */
.stSuccess, .stInfo, .stWarning {
    border-radius: 10px !important;
}

/* ── Divider ─────────────────────────────────────────── */
hr {
    border-color: #2A2A40 !important;
    margin: 1.5rem 0 !important;
}

/* ── Distance badge ──────────────────────────────────── */
.distance-badge {
    display: inline-block;
    background: rgba(16,185,129,0.12);
    color: #10B981;
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* ── Score badge ─────────────────────────────────────── */
.score-badge {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    color: #818CF8;
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* ── Empty state ─────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #5050808;
}
.empty-state-icon { font-size: 3rem; margin-bottom: 0.8rem; }
.empty-state-text { color: #6868A0; font-size: 0.9rem; }

/* ── Metric overrides ────────────────────────────────── */
[data-testid="stMetric"] {
    background: #16162A;
    border: 1px solid #2A2A40;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricValue"] {
    color: #E0E0FF !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    color: #6868A0 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
</style>