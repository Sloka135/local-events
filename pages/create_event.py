"""
Create Event page for Hyperlocal Event Discovery Platform.
Allows users to submit new events that are stored in SQLite.
"""

import streamlit as st
from datetime import date, timedelta
from utils.database import create_event
from utils.styles import CATEGORIES, CATEGORY_EMOJIS


# Default coordinates (Hyderabad city centre)
DEFAULT_LAT = 17.4065
DEFAULT_LON = 78.4772


def render():
    """Render the Create Event page."""
    st.markdown('<div class="section-header">➕ Create a New Event</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Share your event with the community — it appears on the map immediately.</div>',
                unsafe_allow_html=True)

    # Two-column layout: form | tips
    form_col, tip_col = st.columns([3, 1])

    with form_col:
        with st.form("create_event_form", clear_on_submit=True):
            st.markdown("##### Event Details")

            title = st.text_input(
                "Event Title *",
                placeholder="e.g. Hyderabad Design Week Opening Night",
                max_chars=120,
            )

            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox(
                    "Category *",
                    CATEGORIES,
                    format_func=lambda c: f"{CATEGORY_EMOJIS.get(c, '📌')} {c}",
                )
            with col2:
                event_date = st.date_input(
                    "Event Date *",
                    value=date.today() + timedelta(days=7),
                    min_value=date.today(),
                )

            location = st.text_input(
                "Location / Venue *",
                placeholder="e.g. Novotel Hotel, HITECH City, Hyderabad",
            )

            st.markdown("##### Map Coordinates")
            st.caption("Tip: Find coordinates on Google Maps → right-click on the venue → Copy coordinates.")

            lat_col, lon_col = st.columns(2)
            with lat_col:
                latitude = st.number_input(
                    "Latitude *",
                    value=DEFAULT_LAT,
                    format="%.4f",
                    min_value=-90.0,
                    max_value=90.0,
                )
            with lon_col:
                longitude = st.number_input(
                    "Longitude *",
                    value=DEFAULT_LON,
                    format="%.4f",
                    min_value=-180.0,
                    max_value=180.0,
                )

            description = st.text_area(
                "Description",
                placeholder="Tell people what to expect, who it's for, and how to join…",
                height=140,
                max_chars=1000,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Publish Event", type="primary", use_container_width=True)

        # Form validation & submission
        if submitted:
            errors = []
            if not title.strip():
                errors.append("Event title is required.")
            if not location.strip():
                errors.append("Location is required.")
            if latitude == 0.0 and longitude == 0.0:
                errors.append("Please enter valid coordinates (0,0 is the Gulf of Guinea!).")

            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")
            else:
                try:
                    event_id = create_event(
                        title=title.strip(),
                        category=category,
                        location=location.strip(),
                        latitude=latitude,
                        longitude=longitude,
                        date=event_date.isoformat(),
                        description=description.strip(),
                    )
                    st.success(f"✅ Event **{title}** published successfully! (ID: #{event_id})")
                    st.balloons()
                except Exception as e:
                    st.error(f"Failed to save event: {e}")

    # ── Tips panel ────────────────────────────────────────────────────────────
    with tip_col:
        st.markdown("""
        <div style="background:#16162A;border:1px solid #2A2A40;border-radius:14px;padding:1.2rem;">
            <div style="font-weight:700;color:#E0E0FF;margin-bottom:0.8rem;">💡 Tips</div>
            <div style="font-size:0.82rem;color:#7878A8;line-height:1.7;">
                <p>🏷️ Choose the most accurate category so people can find your event easily.</p>
                <p>📍 Precise coordinates help the map pin land on the right spot.</p>
                <p>📝 A good description boosts your event's recommendation score.</p>
                <p>📅 Events are shown in date order — plan ahead for more visibility.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#16162A;border:1px solid #2A2A40;border-radius:14px;padding:1.2rem;">
            <div style="font-weight:700;color:#E0E0FF;margin-bottom:0.8rem;">🗺️ Find Coordinates</div>
            <div style="font-size:0.82rem;color:#7878A8;line-height:1.7;">
                <ol style="padding-left:1.1rem;margin:0;">
                    <li>Open Google Maps</li>
                    <li>Find your venue</li>
                    <li>Right-click → "What's here?"</li>
                    <li>Copy the lat/lon shown</li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)
