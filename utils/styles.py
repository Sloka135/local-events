"""
styles.py
=========
Custom CSS styles and constants for the Radius Streamlit app.
"""

CUSTOM_CSS = """
<style>
/* Google Font ----------------------*/
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* --- CSS Variables ---------------------- */
:root {
    --sand:        #F2EDE4;
    --sand2:       #EAE3D8;
    --sand3:       #DDD4C5;
    --terracotta:  #B06B4A;
    --terracotta2: #8F5438;
    --bark:        #3B2F26;
    --bark2:       #2A1A10;
    --stone:       #7A6E65;
    --stone2:      #A8A099;
    --white:       #FDFAF6;
}

/* --- Global reset ----------------------- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--bark2);
}

/* --- Page background -------------------- */
.stApp {
    background: var(--white);
}

/* --- Sidebar ---------------------------- */
[data-testid="stSidebar"] {
    background: var(--sand) !important;
    border-right: 1px solid var(--sand3);
}

[data-testid="stSidebar"] * {
    color: var(--bark) !important;
}

/* --- Hide Streamlit default page nav --- */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* --- Buttons ---------------------------- */
.stButton > button {
    background: linear-gradient(135deg, var(--terracotta), var(--terracotta2));
    color: var(--white);
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(176, 107, 74, 0.35);
}

/* --- Input fields ----------------------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--white) !important;
    border: 1px solid var(--sand3) !important;
    border-radius: 8px !important;
    color: var(--bark2) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--terracotta) !important;
    box-shadow: 0 0 0 2px rgba(176, 107, 74, 0.15) !important;
}

/* --- Metric boxes ----------------------- */
[data-testid="stMetric"] {
    background: var(--sand);
    border: 1px solid var(--sand3);
    border-radius: 10px;
    padding: 1rem;
}

[data-testid="stMetricValue"] {
    color: var(--terracotta) !important;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* --- Tabs ------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    background: var(--sand2);
    border-radius: 10px;
    padding: 0.3rem;
    gap: 0.3rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: var(--stone);
    font-weight: 500;
    padding: 0.4rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: var(--terracotta) !important;
    color: var(--white) !important;
}

/* --- Dividers --------------------------- */
hr {
    border-color: var(--sand3);
    margin: 1rem 0;
}

/* --- Scrollbar -------------------------- */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: var(--sand2);
}

::-webkit-scrollbar-thumb {
    background: var(--sand3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--terracotta);
}

/* --- Headers ---------------------------- */
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    color: var(--bark2);
}

/* --- Badges / tags ---------------------- */
.tag {
    display: inline-block;
    background: rgba(176, 107, 74, 0.1);
    color: var(--terracotta);
    border: 1px solid rgba(176, 107, 74, 0.25);
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.1rem;
}

/* --- Success / error messages ----------- */
.stSuccess {
    background: rgba(176, 107, 74, 0.08) !important;
    border-color: var(--terracotta) !important;
    color: var(--terracotta2) !important;
}

.stError {
    background: rgba(180, 60, 40, 0.08) !important;
    border-color: #B43C28 !important;
}

/* --- Dataframe / table ------------------ */
.stDataFrame {
    border: 1px solid var(--sand3);
    border-radius: 10px;
    overflow: hidden;
}

/* --- Hero section ----------------------- */
.hero-section {
    padding: 2.5rem 0 1.5rem 0;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--bark2);
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(135deg, var(--terracotta), var(--terracotta2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1rem;
    color: var(--stone);
    max-width: 560px;
    line-height: 1.6;
}

/* --- Stat cards ------------------------- */
.stat-card {
    background: var(--sand);
    border: 1px solid var(--sand3);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--terracotta);
}

.stat-label {
    font-size: 0.8rem;
    color: var(--stone);
    margin-top: 0.2rem;
}

/* --- Nav cards -------------------------- */
.nav-card {
    background: var(--sand);
    border: 1px solid var(--sand3);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.nav-card:hover {
    border-color: var(--terracotta);
    box-shadow: 0 4px 20px rgba(176, 107, 74, 0.12);
}

.nav-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
}

.nav-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--bark);
    margin-bottom: 0.3rem;
}

.nav-card-desc {
    font-size: 0.78rem;
    color: var(--stone);
}

/* --- Event Cards ----------------------- */
.event-card {
    background: var(--sand);
    border: 1px solid var(--sand3);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.event-card:hover {
    border-color: var(--terracotta);
    box-shadow: 0 4px 24px rgba(176, 107, 74, 0.12);
}

.event-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--bark2);
    margin: 0.5rem 0 0.4rem 0;
}

.event-meta {
    display: flex;
    gap: 1.2rem;
    font-size: 0.82rem;
    color: var(--stone);
    margin-bottom: 0.5rem;
}

.event-description {
    font-size: 0.88rem;
    color: var(--stone2);
    line-height: 1.5;
}

/* --- Category & score badges ------------ */
.category-badge {
    display: inline-block;
    background: rgba(176, 107, 74, 0.1);
    color: var(--terracotta2);
    border: 1px solid rgba(176, 107, 74, 0.2);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.4rem;
}

.distance-badge {
    display: inline-block;
    background: rgba(122, 110, 101, 0.1);
    color: var(--stone);
    border: 1px solid rgba(122, 110, 101, 0.2);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.4rem;
    margin-bottom: 0.4rem;
}

.score-badge {
    display: inline-block;
    background: rgba(176, 107, 74, 0.1);
    color: var(--terracotta2);
    border: 1px solid rgba(176, 107, 74, 0.2);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.4rem;
    margin-bottom: 0.4rem;
}

/* --- Section headers ------------------- */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--bark2);
    margin-bottom: 0.2rem;
}

.section-sub {
    font-size: 0.88rem;
    color: var(--stone);
    margin-bottom: 1.2rem;
}

/* --- Empty state ------------------------ */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.empty-state-text {
    font-size: 1rem;
    color: var(--stone);
}

/* --- Hide Streamlit default elements ---- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

</style>
"""

CATEGORY_EMOJIS = {
    "Music":         "🎵",
    "Sports":        "⚽",
    "Food":          "🍕",
    "Art":           "🎨",
    "Technology":    "💻",
    "Education":     "📚",
    "Health":        "🏃",
    "Business":      "💼",
    "Community":     "🤝",
    "Entertainment": "🎭",
    "Outdoor":       "🌿",
    "Fitness":       "💪",
    "Gaming":        "🎮",
    "Fashion":       "👗",
    --Travel":        "✈️",
    "Networking":    "🔗",
    "Comedy":        "😂",
    "Film":          "🎬",
    "Science":       "🔬",
    "Other":         "📌",
}

CATEGORIES = list(CATEGORY_EMOJIS.keys())