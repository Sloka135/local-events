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
    color: #E0E0FF;
}

/* --- Page background -------------------- */
.stApp {
    background: #0F0F1A;
}

/* --- Sidebar ---------------------------- */
[data-testid="stSidebar"] {
    background: #13131F !important;
    border-right: 1px solid #1E1E30;
}

[data-testid="stSidebar"] * {
    color: #E0E0FF !important;
}

/* --- Hide Streamlit default page nav --- */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* --- Buttons ---------------------------- */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #4ECDC4);
    color: white;
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
    box-shadow: 0 4px 20px rgba(108, 99, 255, 0.4);
}

/* --- Input fields ----------------------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1A1A2E !important;
    border: 1px solid #2A2A40 !important;
    border-radius: 8px !important;
    color: #E0E0FF !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
}

/* --- Metric boxes ----------------------- */
[data-testid="stMetric"] {
    background: #13131F;
    border: 1px solid #1E1E30;
    border-radius: 10px;
    padding: 1rem;
}

[data-testid="stMetricValue"] {
    color: #6C63FF !important;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* --- Tabs ------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    background: #13131F;
    border-radius: 10px;
    padding: 0.3rem;
    gap: 0.3rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #4A4A7A;
    font-weight: 500;
    padding: 0.4rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: #6C63FF !important;
    color: white !important;
}

/* --- Dividers --------------------------- */
hr {
    border-color: #2A2A40;
    margin: 1rem 0;
}

/* --- Scrollbar -------------------------- */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #0F0F1A;
}

::-webkit-scrollbar-thumb {
    background: #2A2A40;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6C63FF;
}

/* --- Headers ---------------------------- */
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    color: #E0E0FF;
}

/* --- Badges / tags ---------------------- */
.tag {
    display: inline-block;
    background: rgba(108, 99, 255, 0.15);
    color: #6C63FF;
    border: 1px solid rgba(108, 99, 255, 0.3);
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.1rem;
}

/* --- Success / error messages ----------- */
.stSuccess {
    background: rgba(78, 205, 196, 0.1) !important;
    border-color: #4ECDC4 !important;
    color: #4ECDC4 !important;
}

.stError {
    background: rgba(255, 99, 99, 0.1) !important;
    border-color: #FF6363 !important;
}

/* --- Dataframe / table ------------------ */
.stDataFrame {
    border: 1px solid #1E1E30;
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
    color: #E0E0FF;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(135deg, #6C63FF, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1rem;
    color: #7070A0;
    max-width: 560px;
    line-height: 1.6;
}

/* --- Stat cards ------------------------- */
.stat-card {
    background: #13131F;
    border: 1px solid #1E1E30;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #6C63FF;
}

.stat-label {
    font-size: 0.8rem;
    color: #6A6A9A;
    margin-top: 0.2rem;
}

/* --- Nav cards -------------------------- */
.nav-card {
    background: #13131F;
    border: 1px solid #1E1E30;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.nav-card:hover {
    border-color: #6C63FF;
}

.nav-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
}

.nav-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #E0E0FF;
    margin-bottom: 0.3rem;
}

.nav-card-desc {
    font-size: 0.78rem;
    color: #6A6A9A;
}

/* --- Event Cards ----------------------- */
.event-card {
    background: #13131F;
    border: 1px solid #1E1E30;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.event-card:hover {
    border-color: #6C63FF;
    box-shadow: 0 4px 24px rgba(108, 99, 255, 0.15);
}

.event-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #E0E0FF;
    margin: 0.5rem 0 0.4rem 0;
}

.event-meta {
    display: flex;
    gap: 1.2rem;
    font-size: 0.82rem;
    color: #6A6A9A;
    margin-bottom: 0.5rem;
}

.event-description {
    font-size: 0.88rem;
    color: #9090B0;
    line-height: 1.5;
}

/* --- Category & score badges ------------ */
.category-badge {
    display: inline-block;
    background: rgba(108, 99, 255, 0.12);
    color: #A5A0FF;
    border: 1px solid rgba(108, 99, 255, 0.25);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.4rem;
}

.distance-badge {
    display: inline-block;
    background: rgba(78, 205, 196, 0.12);
    color: #4ECDC4;
    border: 1px solid rgba(78, 205, 196, 0.25);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.4rem;
    margin-bottom: 0.4rem;
}

.score-badge {
    display: inline-block;
    background: rgba(255, 193, 7, 0.12);
    color: #FFC107;
    border: 1px solid rgba(255, 193, 7, 0.25);
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
    color: #E0E0FF;
    margin-bottom: 0.2rem;
}

.section-sub {
    font-size: 0.88rem;
    color: #6A6A9A;
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
    color: #6A6A9A;
}

/* --- Hide Streamlit default elements ---- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header {
    visibility: visible;
}

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