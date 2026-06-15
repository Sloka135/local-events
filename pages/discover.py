"""
Discover Events page for Hyperlocal Event Discovery Platform.
Provides search, category/date filters, nearby filter, event cards,
add-to-favorites, map view, and content-based recommendations.
"""

import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
from utils.database import get_all_events, add_favorite, is_favorite, get_stats
from utils.recommender import search_events, filter_nearby_events, recommend_events
from utils.maps import build_events_map
from utils.styles import CATEGORIES, CATEGORY_EMOJIS


def event_card_html(emoji, category, dist_badge, title, date, location, description):
    css = """
    <style>
    .event-card {
        background: #13131F;
        border: 1px solid #1E1E30;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    .category-badge {
        display: inline-block;
        background: rgba(108,99,255,0.12);
        color: #A5A0FF;
        border: 1px solid rgba(108,99,255,0.25);
        border-radius: 20px;
        padding: 0.15rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    .distance-badge {
        display: inline-block;
        background: rgba(78,205,196,0.12);
        color: #4ECDC4;
        border: 1px solid rgba(78,205,196,0.25);
        border-radius: 20px;
        padding: 0.15rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .score-badge {
        display: inline-block;
        background: rgba(255,193,7,0.12);
        color: #FFC107;
        border: 1px solid rgba(255,193,7,0.25);
        border-radius: 20px;
        padding: 0.15rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .event-card-title {
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
    </style>
    """
    html = (
        '<div class="event-card">'
        '<div class="category-badge">' + emoji + " " + category + "</div>"
        + dist_badge
        + '<div class="event-card-title">' + title + "</div>"
        + '<div class="event-meta">'
        + "<span>📅 " + date + "</span>"
        + "<span>📍 " + location + "</span>"
        + "</div>"
        + '<div class="event-description">' + description + "</div>"
        + "</div>"
    )
    return css + html


def render():
    """Render the Discover Events page."""
    st.markdown('<div class="section-header">🔍 Discover Events</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Find events happening around you</div>', unsafe_allow_html=True)

    all_events = get_all_events()

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🎛️ Filters & Search", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            query = st.text_input("Search events", placeholder="Tech, music, food…", label_visibility="collapsed")
        with col2:
            category = st.selectbox("Category", ["All"] + CATEGORIES, label_visibility="collapsed")

        col3, col4 = st.columns(2)
        with col3:
            date_from = st.date_input("From date", value=None, key="date_from")
        with col4:
            date_to = st.date_input("To date", value=None, key="date_to")

        st.markdown("**📍 Nearby Filter**")
        use_nearby = st.toggle("Show only nearby events")
        if use_nearby:
            ncol1, ncol2, ncol3 = st.columns([1, 1, 1])
            with ncol1:
                user_lat = st.number_input("Your Latitude", value=17.4065, format="%.4f")
            with ncol2:
                user_lon = st.number_input("Your Longitude", value=78.4772, format="%.4f")
            with ncol3:
                radius = st.slider("Radius (km)", 1, 50, 10)

    # Apply filters
    date_from_str = date_from.isoformat() if date_from else ""
    date_to_str   = date_to.isoformat()   if date_to   else ""

    filtered = search_events(all_events, query, category, date_from_str, date_to_str)

    if use_nearby:
        filtered = filter_nearby_events(filtered, user_lat, user_lon, radius)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋 Event Cards", "🗺️ Map View", "✨ Recommendations"])

    # ── Tab 1: Event Cards ────────────────────────────────────────────────────
    with tab1:
        st.markdown(f"**{len(filtered)} event(s) found**")

        if filtered.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔭</div>
                <div class="empty-state-text">No events match your filters. Try broadening your search.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for _, row in filtered.iterrows():
                emoji      = CATEGORY_EMOJIS.get(row["category"], "📌")
                fav        = is_favorite(int(row["id"]))
                dist_badge = (
                    '<span class="distance-badge">📍 ' + str(row["distance_km"]) + " km away</span>"
                    if "distance_km" in row else ""
                )
                desc       = str(row.get("description", ""))
                short_desc = desc[:200] + ("…" if len(desc) > 200 else "")

                components.html(
                    event_card_html(
                        emoji,
                        str(row["category"]),
                        dist_badge,
                        str(row["title"]),
                        str(row["date"]),
                        str(row["location"]),
                        short_desc,
                    ),
                    height=180,
                )

                btn_label = "❤️ Saved" if fav else "🤍 Save"
                bcol1, bcol2 = st.columns([1, 5])
                with bcol1:
                    if st.button(btn_label, key=f"fav_{row['id']}", disabled=fav, use_container_width=True):
                        success = add_favorite(int(row["id"]))
                        if success:
                            st.toast("Added to favourites! ❤️")
                            st.rerun()
                        else:
                            st.info("Already in favourites.")

    # ── Tab 2: Map View ───────────────────────────────────────────────────────
    with tab2:
        if filtered.empty:
            st.info("No events to show on the map. Adjust your filters.")
        else:
            center_lat = filtered["latitude"].mean()
            center_lon = filtered["longitude"].mean()
            fmap = build_events_map(filtered, center_lat=center_lat, center_lon=center_lon)
            st_folium(fmap, use_container_width=True, height=520)

    # ── Tab 3: Recommendations ────────────────────────────────────────────────
    with tab3:
        st.markdown("##### Choose an interest to get personalised event recommendations")
        interest = st.selectbox(
            "Your interest",
            CATEGORIES,
            format_func=lambda c: f"{CATEGORY_EMOJIS.get(c,'📌')} {c}",
            key="rec_interest",
        )
        top_n = st.slider("Number of recommendations", 3, 10, 5, key="rec_topn")

        if st.button("✨ Get Recommendations", type="primary"):
            recs = recommend_events(all_events, interest, top_n=top_n)
            if recs.empty:
                st.info("No recommendations found. Try a different category.")
            else:
                st.markdown(f"**Top {len(recs)} events matching your interest in {interest}:**")
                for _, row in recs.iterrows():
                    emoji     = CATEGORY_EMOJIS.get(row["category"], "📌")
                    score_pct = int(row.get("score", 0) * 100)
                    desc      = str(row.get("description", ""))[:160] + "…"
                    score_badge = '<span class="score-badge">Match: ' + str(score_pct) + "%</span>"

                    components.html(
                        event_card_html(
                            emoji,
                            str(row["category"]),
                            score_badge,
                            str(row["title"]),
                            str(row["date"]),
                            str(row["location"]),
                            desc,
                        ),
                        height=180,
                    )