"""
Recommendation and geolocation utilities for Hyperlocal Event Discovery Platform.
Uses Scikit-Learn TF-IDF for content-based recommendations and Geopy for distance.
"""

import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─── Distance / Nearby filter ────────────────────────────────────────────────

def filter_nearby_events(
    events_df: pd.DataFrame,
    user_lat: float,
    user_lon: float,
    radius_km: float = 10.0,
) -> pd.DataFrame:
    """
    Filter events within a given radius (km) from the user's location.

    Args:
        events_df: DataFrame of events (must have 'latitude', 'longitude' columns).
        user_lat: User's latitude.
        user_lon: User's longitude.
        radius_km: Search radius in kilometres.

    Returns:
        Filtered DataFrame with a 'distance_km' column added, sorted by distance.
    """
    if events_df.empty:
        return events_df

    user_coords = (user_lat, user_lon)

    def _dist(row):
        try:
            return round(geodesic(user_coords, (row["latitude"], row["longitude"])).km, 2)
        except Exception:
            return float("inf")

    df = events_df.copy()
    df["distance_km"] = df.apply(_dist, axis=1)
    nearby = df[df["distance_km"] <= radius_km].sort_values("distance_km")
    return nearby.reset_index(drop=True)


# ─── Content-based Recommendations ──────────────────────────────────────────

def recommend_events(
    events_df: pd.DataFrame,
    interest_category: str,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Recommend events based on a chosen interest category using TF-IDF cosine similarity.

    Builds a corpus from each event's title + category + description, then ranks
    events by similarity to the user-supplied interest string.

    Args:
        events_df: DataFrame of all events.
        interest_category: Category/keyword string representing user interest.
        top_n: Number of recommendations to return.

    Returns:
        Top-N recommended events DataFrame with a 'score' column.
    """
    if events_df.empty:
        return events_df

    df = events_df.copy()

    # Build a text corpus for each event
    df["corpus"] = (
        df["title"].fillna("") + " "
        + df["category"].fillna("") + " "
        + df["description"].fillna("")
    )

    # Append the user interest as a query document
    query = interest_category
    corpus = list(df["corpus"].values) + [query]

    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        # Fallback: category-based filter if TF-IDF fails
        return df[df["category"] == interest_category].head(top_n)

    # Cosine similarity between each event and the query (last row)
    query_vec = tfidf_matrix[-1]
    event_vecs = tfidf_matrix[:-1]
    scores = cosine_similarity(event_vecs, query_vec).flatten()

    df["score"] = np.round(scores, 4)
    recommended = (
        df[df["score"] > 0]
        .sort_values("score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # If no TF-IDF matches, fall back to same-category events
    if recommended.empty:
        recommended = df[df["category"] == interest_category].head(top_n).copy()
        recommended["score"] = 0.0

    return recommended


# ─── Search helper ────────────────────────────────────────────────────────────

def search_events(
    events_df: pd.DataFrame,
    query: str = "",
    category: str = "All",
    date_from: str = "",
    date_to: str = "",
) -> pd.DataFrame:
    """
    Filter events by text query, category, and date range.

    Args:
        events_df: Full events DataFrame.
        query: Free-text search string (matches title, location, description).
        category: Category to filter by ('All' means no filter).
        date_from / date_to: ISO date strings for the date range.

    Returns:
        Filtered DataFrame.
    """
    df = events_df.copy()

    if query:
        q = query.lower()
        mask = (
            df["title"].str.lower().str.contains(q, na=False)
            | df["location"].str.lower().str.contains(q, na=False)
            | df["description"].str.lower().str.contains(q, na=False)
        )
        df = df[mask]

    if category and category != "All":
        df = df[df["category"] == category]

    if date_from:
        df = df[df["date"] >= date_from]

    if date_to:
        df = df[df["date"] <= date_to]

    return df.reset_index(drop=True)
