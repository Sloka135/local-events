"""
styles.py
=========
Custom CSS styles and constants for the Radius Streamlit app.
"""

CUSTOM_CSS = """
<style>
/* Google Font ----------------------*/
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* --- Global reset ----------------------- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #F2EDE4;
}

/* --- Page background -------------------- */
.stApp {
    background: #2A1A10;
}

/* --- Sidebar ---------------------------- */
[data-testid="stSidebar"] {
    background: #3B2F26 !important;
    border-right: 1px solid #4A3828;
}

[data-testid="stSidebar"] * {
    color: #F2EDE4 !important;
}

/* --- Hide Streamlit default page nav --- */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* --- Buttons ---------------------------- */
.stButton > button {
    background: linear-gradient(135deg, #B06B4A, #8B4F32);
    color: #F2EDE4;
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
    box-shadow: 0 4px 20px rgba(176, 107, 74, 0.4);
}

/* --- Input fields ----------------------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #3B2F26 !important;
    border: 1px solid #4A3828 !important;
    border-radius: 8px !important;
    color: #F2EDE4 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #B06B4A !important;
    box-shadow: 0 0 0 2px rgba(176, 107, 74, 0.2) !important;
}

/* --- Metric boxes ----------------------- */
[data-testid="stMetric"] {
    background: #3B2F26;
    border: 1px solid #4A3828;
    border-radius: 10px;
    padding: 1rem;
}

[data-testid="stMetricValue"] {
    color: #B06B4A !important;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* --- Tabs ------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    background: #3B2F26;
    border-radius: 10px;
    padding: 0.3rem;
    gap: 0.3rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #8A7A6A;
    font-weight: 500;
    padding: 0.4rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: #B06B4A !important;
    color: #F2EDE4 !important;
}

/* --- Dividers --------------------------- */
hr {
    border-color: #4A3828;
    margin: 1rem 0;
}

/* --- Scrollbar -------------------------- */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #2A1A10;
}

::-webkit-scrollbar-thumb {
    background: #4A3828;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #B06B4A;
}

/* --- Headers ---------------------------- */
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    color: #F2EDE4;
}

/* --- Badges / tags ---------------------- */
.tag {
    display: inline-block;
    background: rgba(176, 107, 74, 0.15);
    color: #B06B4A;
    border: 1px solid rgba(176, 107, 74, 0.3);
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.1rem;
}

/* --- Success / error messages ----------- */
.stSuccess {
    background: rgba(176, 107, 74, 0.1) !important;
    border-color: #B06B4A !important;
    color: #B06B4A !important;
}

.stError {
    background: rgba(180, 60, 40, 0.1) !important;
    border-color: #B43C28 !important;
}

/* --- Dataframe / table ------------------ */
.stDataFrame {
    border: 1px solid #4A3828;
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
    color: #F2EDE4;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(135deg, #B06B4A, #D4956A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1rem;
    color: #A89880;
    max-width: 560px;
    line-height: 1.6;
}

/* --- Stat cards ------------------------- */
.stat-card {
    background: #3B2F26;
    border: 1px solid #4A3828;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #B06B4A;
}

.stat-label {
    font-size: 0.8rem;
    color: #8A7A6A;
    margin-top: 0.2rem;
}

/* --- Nav cards -------------------------- */
.nav-card {
    background: #3B2F26;
    border: 1px solid #4A3828;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.nav-card:hover {
    border-color: #B06B4A;
}

.nav-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
}

.nav-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #F2EDE4;
    margin-bottom: 0.3rem;
}

.nav-card-desc {
    font-size: 0.78rem;
    color: #8A7A6A;
}

/* --- Event Cards ----------------------- */
.event-card {
    background: #3B2F26;
    border: 1px solid #4A3828;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.event-card:hover {
    border-color: #B06B4A;
    box-shadow: 0 4px 24px rgba(176, 107, 74, 0.15);
}

.event-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #F2EDE4;
    margin: 0.5rem 0 0.4rem 0;
}

.event-meta {
    display: flex;
    gap: 1.2rem;
    font-size: 0.82rem;
    color: #8A7A6A;
    margin-bottom: 0.5rem;
}

.event-description {
    font-size: 0.88rem;
    color: #A89880;
    line-height: 1.5;
}

/* --- Category & score badges ------------ */
.category-badge {
    display: inline-block;
    background: rgba(176, 107, 74, 0.12);
    color: #D4956A;
    border: 1px solid rgba(176, 107, 74, 0.25);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.4rem;
}

.distance-badge {
    display: inline-block;
    background: rgba(176, 140, 74, 0.12);
    color: #C4A45A;
    border: 1px solid rgba(176, 140, 74, 0.25);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.4rem;
    margin-bottom: 0.4rem;
}

.score-badge {
    display: inline-block;
    background: rgba(180, 130, 60, 0.12);
    color: #C8A050;
    border: 1px solid rgba(180, 130, 60, 0.25);
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
    color: #F2EDE4;
    margin-bottom: 0.2rem;
}

.section-sub {
    font-size: 0.88rem;
    color: #8A7A6A;
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
    color: #8A7A6A;
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
    "Travel":        "✈️",
    "Networking":    "🔗",
    "Comedy":        "😂",
    "Film":          "🎬",
    "Science":       "🔬",
    "Other":         "📌",
}

CATEGORIES = list(CATEGORY_EMOJIS.keys())