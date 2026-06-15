"""
Discover Events page for Radius.
Provides search, category/date filters, nearby filter, event cards,
add-to-favorites, registration, reminders, map view, and recommendations.
"""

import streamlit as st
from streamlit_folium import st_folium
from utils.database import (
    get_all_events, add_favorite, is_favorite,
    register_for_event, is_registered, get_registration_count,
    set_reminder, has_reminder,
)
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
                event_id  = int(row["id"])
                emoji     = CATEGORY_EMOJIS.get(row["category"], "📌")
                fav       = is_favorite(event_id)
                reg_count = get_registration_count(event_id)

                with st.container(border=True):

                    # ── Badge row ─────────────────────────────────────────────
                    badge_col, count_col = st.columns([4, 1])
                    with badge_col:
                        tags = f"`{emoji} {row['category']}`"
                        if "distance_km" in row:
                            tags += f"  `📍 {row['distance_km']} km away`"
                        st.markdown(tags)
                    with count_col:
                        st.caption(f"👥 {reg_count} going")

                    # ── Title & meta ──────────────────────────────────────────
                    st.markdown(f"### {row['title']}")
                    mcol1, mcol2 = st.columns(2)
                    with mcol1:
                        st.markdown(f"📅 **{row['date']}**")
                    with mcol2:
                        st.markdown(f"📍 **{row['location']}**")

                    # ── Description ───────────────────────────────────────────
                    desc = str(row.get("description", ""))
                    st.caption(desc[:200] + ("…" if len(desc) > 200 else ""))

                    st.divider()

                    # ── Action buttons ────────────────────────────────────────
                    btn1, btn2, btn3, _ = st.columns([1, 1, 1, 2])
                    with btn1:
                        fav_label = "❤️ Saved" if fav else "🤍 Save"
                        if st.button(fav_label, key=f"fav_{event_id}", disabled=fav, use_container_width=True):
                            if add_favorite(event_id):
                                st.toast("Added to favourites! ❤️")
                                st.rerun()

                    with btn2:
                        if st.button("📝 Register", key=f"reg_btn_{event_id}", use_container_width=True):
                            st.session_state[f"show_reg_{event_id}"] = not st.session_state.get(f"show_reg_{event_id}", False)
                            st.session_state[f"show_rem_{event_id}"] = False

                    with btn3:
                        if st.button("🔔 Reminder", key=f"rem_btn_{event_id}", use_container_width=True):
                            st.session_state[f"show_rem_{event_id}"] = not st.session_state.get(f"show_rem_{event_id}", False)
                            st.session_state[f"show_reg_{event_id}"] = False

                    # ── Registration form ─────────────────────────────────────
                    if st.session_state.get(f"show_reg_{event_id}"):
                        with st.form(key=f"reg_form_{event_id}"):
                            st.markdown("#### 📝 Register for this Event")
                            reg_name  = st.text_input("Your Name")
                            reg_email = st.text_input("Your Email")
                            reg_phone = st.text_input("Phone (optional)")

                            scol1, scol2 = st.columns(2)
                            with scol1:
                                submitted = st.form_submit_button("✅ Confirm", use_container_width=True)
                            with scol2:
                                cancelled = st.form_submit_button("✖ Cancel", use_container_width=True)

                            if submitted:
                                if not reg_name or not reg_email:
                                    st.warning("Please fill in your name and email.")
                                elif is_registered(event_id, reg_email):
                                    st.info("You're already registered for this event!")
                                else:
                                    if register_for_event(event_id, reg_name, reg_email, reg_phone):
                                        st.session_state[f"show_reg_{event_id}"] = False
                                        st.toast(f"Registered for {row['title']}! 🎉")
                                        st.rerun()
                                    else:
                                        st.error("Registration failed. Please try again.")
                            if cancelled:
                                st.session_state[f"show_reg_{event_id}"] = False
                                st.rerun()

                    # ── Reminder form ─────────────────────────────────────────
                    if st.session_state.get(f"show_rem_{event_id}"):
                        with st.form(key=f"rem_form_{event_id}"):
                            st.markdown("#### 🔔 Set a Reminder")
                            rem_name  = st.text_input("Your Name")
                            rem_email = st.text_input("Your Email")
                            rem_days  = st.selectbox(
                                "Remind me",
                                [1, 2, 3, 7],
                                format_func=lambda d: f"{d} day{'s' if d > 1 else ''} before",
                            )

                            rcol1, rcol2 = st.columns(2)
                            with rcol1:
                                rem_submitted = st.form_submit_button("🔔 Set Reminder", use_container_width=True)
                            with rcol2:
                                rem_cancelled = st.form_submit_button("✖ Cancel", use_container_width=True)

                            if rem_submitted:
                                if not rem_name or not rem_email:
                                    st.warning("Please fill in your name and email.")
                                elif has_reminder(event_id, rem_email):
                                    st.info("You already have a reminder set for this event!")
                                else:
                                    if set_reminder(event_id, rem_name, rem_email, rem_days):
                                        st.session_state[f"show_rem_{event_id}"] = False
                                        st.toast(f"Reminder set {rem_days} day{'s' if rem_days > 1 else ''} before {row['title']}! 🔔")
                                        st.rerun()
                                    else:
                                        st.error("Could not set reminder. Please try again.")
                            if rem_cancelled:
                                st.session_state[f"show_rem_{event_id}"] = False
                                st.rerun()

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