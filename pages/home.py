"""
Home page for Hyperlocal Event Discovery Platform.
Displays hero section, platform stats, and quick navigation cards.
"""
import streamlit as st
from utils.database import get_stats, get_upcoming_events
from utils.styles import CATEGORY_EMOJIS


def render():
    """Render the Home page."""

    # ── Hero Section ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Discover Events<br><span>Near You</span></div>
        <div class="hero-subtitle">
            Find tech meetups, music festivals, food fairs, and more happening
            right in your neighbourhood. Create, explore, and never miss out.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Platform Statistics ───────────────────────────────────────────────────
    stats = get_stats()
    col1, col2, col3, col4 = st.columns(4)
    stat_items = [
        (col1, stats["total_events"],    "Total Events",     "📅"),
        (col2, stats["upcoming_events"], "Upcoming Events",  "🔜"),
        (col3, stats["categories"],      "Categories",       "🏷️"),
        (col4, stats["total_favorites"], "Saved Favourites", "❤️"),
    ]
    for col, number, label, icon in stat_items:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:1.6rem;margin-bottom:4px;">{icon}</div>
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Navigation Cards ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Explore the Platform</div>', unsafe_allow_html=True)

    nav_cards = [
        ("🔍", "Discover Events",     "Search and filter events near you",        "Discover Events"),
        ("➕", "Create Event",         "Share your event with the community",       "Create Event"),
        ("❤️",  "My Favourites",        "View and manage your saved events",         "Favorites"),
        ("📊", "Analytics Dashboard", "Visualise trends and event statistics",     "Analytics Dashboard"),
    ]

    cols = st.columns(4)
    for col, (icon, title, desc, page) in zip(cols, nav_cards):
        with col:
            st.markdown(f"""
            <div class="nav-card">
                <div class="nav-card-icon">{icon}</div>
                <div class="nav-card-title">{title}</div>
                <div class="nav-card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go →", key=f"home_{page}", use_container_width=True):
                st.session_state["page"] = page
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Upcoming Events Preview ───────────────────────────────────────────────
    st.markdown('<div class="section-header">Upcoming Events</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Next 5 events on the calendar</div>', unsafe_allow_html=True)

    upcoming = get_upcoming_events(5)
    if upcoming.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <div class="empty-state-text">No upcoming events. Be the first to create one!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, row in upcoming.iterrows():
            emoji = CATEGORY_EMOJIS.get(row["category"], "📌")
            desc = str(row.get("description", ""))
            short_desc = desc[:140] + ("..." if len(desc) > 140 else "")
            st.markdown(f"""
            <div class="event-card">
                <div class="category-badge">{emoji} {row['category']}</div>
                <div class="event-card-title">{row['title']}</div>
                <div class="event-meta">
                    <span>📅 {row['date']}</span>
                    <span>📍 {row['location']}</span>
                </div>
                <div class="event-description">{short_desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Category Chips ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Browse by Category</div>', unsafe_allow_html=True)

    chips_html = "".join(
        f'<span style="display:inline-block;background:#16162A;border:1px solid #2A2A40;'
        f'border-radius:20px;padding:6px 16px;margin:4px;font-size:0.85rem;color:#C4C4D4;'
        f'font-weight:500;">{emoji} {cat}</span>'
        for cat, emoji in CATEGORY_EMOJIS.items()
    )
    st.markdown(f'<div style="line-height:2.4;">{chips_html}</div>', unsafe_allow_html=True)