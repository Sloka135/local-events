"""
Analytics Dashboard page for Hyperlocal Event Discovery Platform.
Displays platform-wide statistics and interactive Plotly charts.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from utils.database import (
    get_all_events,
    get_events_by_category,
    get_stats,
    get_upcoming_events,
)

# Dark theme tokens consistent with the app palette
PLOTLY_TEMPLATE = "plotly_dark"
CHART_BG        = "rgba(22,22,42,0)"   # transparent
PAPER_BG        = "rgba(22,22,42,0)"
GRID_COLOR      = "#2A2A40"
ACCENT_COLORS   = [
    "#6366F1", "#EC4899", "#F59E0B", "#10B981",
    "#3B82F6", "#EF4444", "#8B5CF6", "#14B8A6",
    "#6B7280",
]


def _common_layout(fig, title: str = ""):
    """Apply consistent dark styling to any Plotly figure."""
    fig.update_layout(
        title=title,
        title_font=dict(size=15, color="#E0E0FF"),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="Inter", color="#9898B8"),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(font=dict(color="#9898B8")),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig


def render():
    """Render the Analytics Dashboard page."""
    st.markdown('<div class="section-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Platform-wide insights and event statistics</div>', unsafe_allow_html=True)

    all_events = get_all_events()
    stats      = get_stats()

    if all_events.empty:
        st.info("No events in the database yet. Create some events to see analytics!")
        return

    # ── KPI Metrics ───────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Events",      stats["total_events"])
    m2.metric("Upcoming Events",   stats["upcoming_events"])
    m3.metric("Categories",        stats["categories"])
    m4.metric("Saved Favourites",  stats["total_favorites"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Category donut + Monthly bar ──────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        cat_df = get_events_by_category()
        fig_donut = px.pie(
            cat_df,
            values="count",
            names="category",
            hole=0.55,
            color_discrete_sequence=ACCENT_COLORS,
            template=PLOTLY_TEMPLATE,
        )
        fig_donut.update_traces(textinfo="percent+label", textfont_size=11)
        _common_layout(fig_donut, "Events by Category")
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        # Monthly distribution
        events_copy = all_events.copy()
        events_copy["month"] = pd.to_datetime(events_copy["date"], errors="coerce").dt.strftime("%b %Y")
        monthly = events_copy.groupby("month").size().reset_index(name="count")

        fig_bar = px.bar(
            monthly,
            x="month",
            y="count",
            color="count",
            color_continuous_scale=["#6366F1", "#EC4899"],
            template=PLOTLY_TEMPLATE,
            text="count",
        )
        fig_bar.update_traces(textposition="outside", marker_line_width=0)
        fig_bar.update_coloraxes(showscale=False)
        _common_layout(fig_bar, "Events per Month")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Row 2: Category horizontal bar + Geographic scatter ──────────────────
    c3, c4 = st.columns(2)

    with c3:
        cat_df_sorted = cat_df.sort_values("count")
        fig_hbar = px.bar(
            cat_df_sorted,
            y="category",
            x="count",
            orientation="h",
            color="category",
            color_discrete_sequence=ACCENT_COLORS,
            template=PLOTLY_TEMPLATE,
            text="count",
        )
        fig_hbar.update_traces(textposition="outside")
        fig_hbar.update_layout(showlegend=False, yaxis_title="", xaxis_title="Number of events")
        _common_layout(fig_hbar, "Category Breakdown")
        st.plotly_chart(fig_hbar, use_container_width=True)

    with c4:
        # Geographic scatter
        fig_scatter = px.scatter_mapbox(
            all_events,
            lat="latitude",
            lon="longitude",
            color="category",
            hover_name="title",
            hover_data={"date": True, "location": True, "latitude": False, "longitude": False},
            color_discrete_sequence=ACCENT_COLORS,
            zoom=10,
            mapbox_style="carto-darkmatter",
        )
        fig_scatter.update_layout(
            paper_bgcolor=PAPER_BG,
            margin=dict(l=0, r=0, t=30, b=0),
            title="Event Locations",
            title_font=dict(size=15, color="#E0E0FF"),
            legend=dict(font=dict(color="#9898B8")),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ── Row 3: Upcoming events table ─────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="font-size:1.2rem;">📅 Next 10 Upcoming Events</div>',
                unsafe_allow_html=True)

    upcoming = get_upcoming_events(10)
    if not upcoming.empty:
        display_df = upcoming[["title", "category", "date", "location"]].copy()
        display_df.columns = ["Title", "Category", "Date", "Location"]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No upcoming events found.")

    # ── Row 4: Timeline scatter ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    events_timeline = all_events.copy()
    events_timeline["date_parsed"] = pd.to_datetime(events_timeline["date"], errors="coerce")
    events_timeline = events_timeline.dropna(subset=["date_parsed"])

    if not events_timeline.empty:
        # Count by category + date for bubble size
        fig_timeline = px.scatter(
            events_timeline,
            x="date_parsed",
            y="category",
            color="category",
            hover_name="title",
            hover_data={"date_parsed": False, "location": True},
            color_discrete_sequence=ACCENT_COLORS,
            template=PLOTLY_TEMPLATE,
            size_max=14,
        )
        fig_timeline.update_traces(marker=dict(size=12, opacity=0.8))
        fig_timeline.update_layout(
            showlegend=False,
            xaxis_title="Date",
            yaxis_title="",
        )
        _common_layout(fig_timeline, "Event Timeline")
        st.plotly_chart(fig_timeline, use_container_width=True)
