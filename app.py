"""
Hyperlocal Event Discovery Platform
=====================================
Main entry point for the Streamlit multi-page application.

Run with:
    streamlit run app.py
"""

import sys
import os

# Ensure the project root is in sys.path so relative imports work
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Hyperlocal Events",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports ──────────────────────────────────────────────────────────
from utils.database import init_database
from utils.styles import CUSTOM_CSS
from pages import home, discover, create_event, favorites, analytics

# ── Bootstrap DB ──────────────────────────────────────────────────────────────
init_database()

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# ── Sidebar navigation ────────────────────────────────────────────────────────
PAGES = {
    "Home":                ("🏠", home),
    "Discover Events":     ("🔍", discover),
    "Create Event":        ("➕", create_event),
    "Favorites":           ("❤️",  favorites),
    "Analytics Dashboard": ("📊", analytics),
}

with st.sidebar:
    # Logo / brand
    st.markdown("""
<div style="padding:1.2rem 0 1.6rem 0;text-align:center;">
    <div style="font-size:2rem;margin-bottom:0.3rem;">📍</div>
    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#E0E0FF;letter-spacing:-0.01em;line-height:1.2;">
        Hyperlocal<br>Events
    </div>
    <div style="font-size:0.72rem;color:#4A4A7A;margin-top:0.3rem;">
        Discover · Create · Connect
    </div>
</div>
<hr style="border-color:#2A2A40;margin:0 0 1rem 0;">
""", unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.7rem;color:#4A4A7A;text-transform:uppercase;'
        'letter-spacing:0.1em;margin-bottom:0.5rem;padding-left:0.2rem;">Navigation</div>',
        unsafe_allow_html=True,
    )

    for page_name, (icon, _module) in PAGES.items():
        is_active = st.session_state["page"] == page_name
        if st.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
        ):
            st.session_state["page"] = page_name
            st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:0.72rem;color:#3A3A6A;text-align:center;line-height:1.6;">
    Built with Streamlit · SQLite<br>Folium · Plotly · Scikit-Learn
</div>
""", unsafe_allow_html=True)

# ── Route to active page ──────────────────────────────────────────────────────
current_page = st.session_state.get("page", "Home")
_, module = PAGES.get(current_page, ("🏠", home))

try:
    module.render()
except Exception as e:
    st.error(f"Something went wrong rendering **{current_page}**: `{e}`")
    import traceback
    with st.expander("Stack trace"):
        st.code(traceback.format_exc())