"""
Map utility module for Hyperlocal Event Discovery Platform.
Builds interactive Folium maps for event visualization.
"""

import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Category-to-color mapping for map markers
CATEGORY_COLORS = {
    "Technology":      "#6366F1",  # indigo
    "Music":           "#EC4899",  # pink
    "Food & Drink":    "#F59E0B",  # amber
    "Arts":            "#8B5CF6",  # violet
    "Health & Wellness": "#10B981", # emerald
    "Entertainment":   "#EF4444",  # red
    "Sports":          "#3B82F6",  # blue
    "Education":       "#14B8A6",  # teal
    "Other":           "#6B7280",  # gray
}

CATEGORY_ICONS = {
    "Technology":      "laptop",
    "Music":           "music",
    "Food & Drink":    "cutlery",
    "Arts":            "picture-o",
    "Health & Wellness": "heart",
    "Entertainment":   "star",
    "Sports":          "trophy",
    "Education":       "graduation-cap",
    "Other":           "map-marker",
}


def _get_color(category: str) -> str:
    """Return a Folium-compatible color name for a category."""
    color_map = {
        "Technology":        "purple",
        "Music":             "pink",
        "Food & Drink":      "orange",
        "Arts":              "darkpurple",
        "Health & Wellness": "green",
        "Entertainment":     "red",
        "Sports":            "blue",
        "Education":         "cadetblue",
        "Other":             "gray",
    }
    return color_map.get(category, "gray")


def build_events_map(
    events_df: pd.DataFrame,
    center_lat: float = 17.4065,
    center_lon: float = 78.4772,
    zoom: int = 12,
    cluster: bool = True,
) -> folium.Map:
    """
    Build a Folium map with event markers.

    Args:
        events_df: DataFrame containing event data.
        center_lat/center_lon: Map center coordinates.
        zoom: Initial zoom level.
        cluster: Whether to cluster nearby markers.

    Returns:
        Configured folium.Map object.
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="CartoDB positron",
        control_scale=True,
    )

    if events_df.empty:
        return m

    # Optional marker clustering
    marker_group = MarkerCluster(name="Events") if cluster else folium.FeatureGroup(name="Events")

    for _, row in events_df.iterrows():
        try:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
        except (ValueError, KeyError):
            continue

        category = row.get("category", "Other")
        color = _get_color(category)
        icon_name = CATEGORY_ICONS.get(category, "map-marker")

        # Rich popup HTML
        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; min-width: 200px; max-width: 260px;">
            <div style="background: {CATEGORY_COLORS.get(category, '#6B7280')};
                        color: white; padding: 8px 12px; border-radius: 8px 8px 0 0;
                        font-weight: 700; font-size: 13px;">
                {row.get('title', 'Event')}
            </div>
            <div style="padding: 10px 12px; background: #ffffff; border-radius: 0 0 8px 8px;
                        border: 1px solid #e5e7eb; border-top: none;">
                <p style="margin: 4px 0; font-size: 12px; color: #6B7280;">
                    <b>📅</b> {row.get('date', 'TBD')}
                </p>
                <p style="margin: 4px 0; font-size: 12px; color: #6B7280;">
                    <b>📍</b> {row.get('location', 'TBD')}
                </p>
                <p style="margin: 4px 0; font-size: 12px; color: #6B7280;">
                    <b>🏷️</b> {category}
                </p>
                <p style="margin: 8px 0 4px 0; font-size: 11px; color: #374151;
                          line-height: 1.4;">
                    {str(row.get('description', ''))[:120]}{'...' if len(str(row.get('description', ''))) > 120 else ''}
                </p>
            </div>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{row.get('title', '')} — {category}",
            icon=folium.Icon(color=color, icon=icon_name, prefix="fa"),
        ).add_to(marker_group)

    marker_group.add_to(m)

    # Legend
    legend_items = "".join(
        f'<div style="display:flex;align-items:center;gap:6px;margin:3px 0;">'
        f'<span style="width:12px;height:12px;border-radius:50%;background:{hex_color};display:inline-block;"></span>'
        f'<span style="font-size:11px;color:#374151;">{cat}</span></div>'
        for cat, hex_color in CATEGORY_COLORS.items()
    )
    legend_html = f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                background:white;padding:12px 16px;border-radius:12px;
                box-shadow:0 4px 20px rgba(0,0,0,0.15);font-family:sans-serif;">
        <div style="font-weight:700;font-size:13px;margin-bottom:8px;color:#1F2937;">Event Categories</div>
        {legend_items}
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m
