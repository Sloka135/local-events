"""
Favorites page for Hyperlocal Event Discovery Platform.
Displays saved events and allows removal from favorites.
"""

import streamlit as st
from streamlit_folium import st_folium
from utils.database import get_favorites, remove_favorite
from utils.maps import build_events_map
from utils.styles import CATEGORY_EMOJIS


def render():
    """Render the Favorites page."""
    st.markdown('<div class="section-header">❤️ My Favourites</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Events you\'ve saved for quick access</div>', unsafe_allow_html=True)

    favs = get_favorites()

    if favs.empty:
        st.markdown("""
        <div class="empty-state" style="padding:4rem 1rem;">
            <div class="empty-state-icon">💔</div>
            <div style="font-size:1.1rem;font-weight:700;color:#E0E0FF;margin-bottom:0.4rem;">No saved events yet</div>
            <div class="empty-state-text">
                Head over to <b>Discover Events</b> and hit the save button on any event you like.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Discover Events", type="primary"):
            st.session_state["page"] = "Discover Events"
            st.rerun()
        return

    # Summary strip
    st.markdown(f"""
    <div style="background:#16162A;border:1px solid #2A2A40;border-radius:12px;
                padding:0.9rem 1.4rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.8rem;">
        <span style="font-size:1.4rem;">❤️</span>
        <span style="color:#E0E0FF;font-weight:600;">{len(favs)} saved event{'s' if len(favs)!=1 else ''}</span>
    </div>
    """, unsafe_allow_html=True)

    # Tabs: Cards | Map
    tab1, tab2 = st.tabs(["📋 Saved Events", "🗺️ Map View"])

    with tab1:
        for _, row in favs.iterrows():
            emoji = CATEGORY_EMOJIS.get(row["category"], "📌")
            added = str(row.get("added_at", ""))[:10]

            st.markdown(f"""
            <div class="event-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.4rem;">
                    <div class="category-badge">{emoji} {row['category']}</div>
                    <div style="font-size:0.75rem;color:#4A4A7A;">Saved on {added}</div>
                </div>
                <div class="event-card-title">{row['title']}</div>
                <div class="event-meta">
                    <span>📅 {row['date']}</span>
                    <span>📍 {row['location']}</span>
                </div>
                <div class="event-description">{str(row.get('description',''))[:220]}{"…" if len(str(row.get('description',''))) > 220 else ""}</div>
            </div>
            """, unsafe_allow_html=True)

            rcol, _ = st.columns([1, 5])
            with rcol:
                if st.button("🗑️ Remove", key=f"rm_{row['id']}", use_container_width=True):
                    remove_favorite(int(row["id"]))
                    st.success("Removed from favourites.")
                    st.rerun()

    with tab2:
        if not favs.empty:
            fmap = build_events_map(
                favs,
                center_lat=favs["latitude"].mean(),
                center_lon=favs["longitude"].mean(),
                zoom=12,
            )
            st_folium(fmap, use_container_width=True, height=500)
        else:
            st.info("No saved events to display on the map.")
