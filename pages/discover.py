"""
Discover Events page for Radius.
Provides search, category/date filters, nearby filter, event cards,
add-to-favorites, map view, and content-based recommendations.
"""

import streamlit as st
from streamlit_folium import st_folium
from utils.database import get_all_events, add_favorite, is_favorite
from utils.recommender import search_events, filter_nearby_events, recommend_events
from utils.maps import build_events_map
from utils.styles import CATEGORIES, CATEGORY_EMOJIS


def render():
    """Render the Discover Events page."""
    st.title("🔍 Discover Events")
    st.caption("Find events happening around you")

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
        user_lat, user_lon, radius = 17.4065, 78.4772, 10
        if use_nearby:
            ncol1, ncol2, ncol3 = st.columns(3)
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
            st.info("🔭 No events match your filters. Try broadening your search.")
        else:
            for _, row in filtered.iterrows():
                emoji = CATEGORY_EMOJIS.get(row["category"], "📌")
                fav   = is_favorite(int(row["id"]))

                with st.container(border=True):
                    # Category + distance badges
                    badge_col, spacer = st.columns([3, 1])
                    with badge_col:
                        tags = f"`{emoji} {row['category']}`"
                        if "distance_km" in row:
                            tags += f"  `📍 {row['distance_km']} km away`"
                        st.markdown(tags)

                    # Title
                    st.markdown(f"### {row['title']}")

                    # Meta info
                    mcol1, mcol2 = st.columns(2)
                    with mcol1:
                        st.markdown(f"📅 **{row['date']}**")
                    with mcol2:
                        st.markdown(f"📍 **{row['location']}**")

                    # Description
                    desc = str(row.get("description", ""))
                    st.caption(desc[:200] + ("…" if len(desc) > 200 else ""))

                    # Save button
                    btn_label = "❤️ Saved" if fav else "🤍 Save"
                    bcol1, _ = st.columns([1, 5])
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
            format_func=lambda c: f"{CATEGORY_EMOJIS.get(c, '📌')} {c}",
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

                    with st.container(border=True):
                        st.markdown(f"`{emoji} {row['category']}`  `✨ Match: {score_pct}%`")
                        st.markdown(f"### {row['title']}")
                        mcol1, mcol2 = st.columns(2)
                        with mcol1:
                            st.markdown(f"📅 **{row['date']}**")
                        with mcol2:
                            st.markdown(f"📍 **{row['location']}**")
                        st.caption(desc)