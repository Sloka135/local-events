"""
styles.py
=========
Custom CSS styles for the Hyperlocal Events Streamlit app.
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

/* --- Cards ------------------------------ */
.event-card {
    background: #13131F;
    border: 1px solid #1E1E30;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.event-card:hover {
    border-color: #6C63FF;
    box-shadow: 0 4px 24px rgba(108, 99, 255, 0.15);
    transform: translateY(-2px);
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

/* --- Hide Streamlit default elements ---- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

</style>
"""