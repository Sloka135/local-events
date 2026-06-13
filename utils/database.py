"""
Database utility module for Hyperlocal Event Discovery Platform.
Handles SQLite database creation, connections, and CRUD operations.
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "events.db")


def get_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables if they don't exist, and seed with sample data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create favorites table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            UNIQUE(event_id)
        )
    """)

    conn.commit()

    # Seed with sample data if empty
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    if count == 0:
        _seed_sample_data(cursor)
        conn.commit()

    conn.close()


def _seed_sample_data(cursor):
    """Insert sample events into the database."""
    sample_events = [
        ("Tech Startup Meetup", "Technology", "HITEC City, Hyderabad", 17.4435, 78.3772,
         "2025-07-15", "Monthly networking meetup for startup founders and developers. Pitches, demos, and open discussion."),
        ("Classical Music Evening", "Music", "Ravindra Bharathi, Hyderabad", 17.4062, 78.4691,
         "2025-07-18", "An evening of classical Carnatic music by renowned artists. Open to all music lovers."),
        ("Food Festival Hyderabad", "Food & Drink", "Necklace Road, Hyderabad", 17.4146, 78.4738,
         "2025-07-20", "Celebrate Hyderabad's rich culinary culture with over 50 food stalls, live cooking demos, and competitions."),
        ("Photography Walk", "Arts", "Charminar, Hyderabad", 17.3616, 78.4747,
         "2025-07-22", "Guided photography walk through the historic old city. All skill levels welcome. Bring your camera!"),
        ("Yoga & Wellness Camp", "Health & Wellness", "KBR National Park, Hyderabad", 17.4239, 78.4244,
         "2025-07-24", "A rejuvenating morning yoga session followed by wellness workshops and healthy food stalls."),
        ("Open Mic Night", "Entertainment", "Jubilee Hills, Hyderabad", 17.4314, 78.4079,
         "2025-07-25", "Open mic event for stand-up comedians, poets, and musicians. Sign up at the venue."),
        ("Python Workshop", "Technology", "T-Hub, Hyderabad", 17.4270, 78.3440,
         "2025-07-28", "Hands-on Python workshop for beginners. Topics: data analysis, automation, and web scraping."),
        ("Indie Art Exhibition", "Arts", "Lamakaan, Hyderabad", 17.4207, 78.4340,
         "2025-07-30", "Showcasing work from 20 independent Hyderabadi artists. Painting, sculpture, and digital art."),
        ("Marathon 2025", "Sports", "LB Stadium, Hyderabad", 17.3950, 78.4744,
         "2025-08-02", "Annual city marathon with 5K, 10K, and 21K categories. Register online to participate."),
        ("Book Club Meetup", "Education", "Crossword Bookstore, Hyderabad", 17.4484, 78.3873,
         "2025-08-05", "Monthly book club meetup. This month's book: 'The Alchemist'. Discussion and refreshments."),
        ("Street Dance Battle", "Entertainment", "Inorbit Mall, Hyderabad", 17.4333, 78.3817,
         "2025-08-07", "Inter-city street dance competition featuring hip-hop, breaking, and locking styles. Cash prizes!"),
        ("Startup Funding Summit", "Technology", "Novotel Hotel, Hyderabad", 17.4523, 78.3748,
         "2025-08-10", "Connect with VCs, angel investors, and fellow entrepreneurs. Panel discussions and 1:1 meetings."),
        ("Farmers Market", "Food & Drink", "Madhapur, Hyderabad", 17.4485, 78.3908,
         "2025-08-12", "Fresh organic produce, homemade goods, and artisanal foods directly from local farmers."),
        ("Cycling Event", "Sports", "Hussain Sagar, Hyderabad", 17.4239, 78.4738,
         "2025-08-14", "Morning cycling event around Hussain Sagar lake. All skill levels. Cycles available for rent."),
        ("AI & ML Conference", "Technology", "ISB Hyderabad", 17.5353, 78.3463,
         "2025-08-16", "Full-day conference on the latest in Artificial Intelligence and Machine Learning. 20+ speakers."),
    ]

    cursor.executemany("""
        INSERT INTO events (title, category, location, latitude, longitude, date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_events)


# ─── Events CRUD ─────────────────────────────────────────────────────────────

def get_all_events() -> pd.DataFrame:
    """Retrieve all events as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM events ORDER BY date ASC", conn)
    conn.close()
    return df


def get_event_by_id(event_id: int) -> dict | None:
    """Retrieve a single event by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_event(title, category, location, latitude, longitude, date, description) -> int:
    """Insert a new event and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (title, category, location, latitude, longitude, date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, category, location, float(latitude), float(longitude), date, description))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


def delete_event(event_id: int):
    """Delete an event by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


# ─── Favorites CRUD ──────────────────────────────────────────────────────────

def get_favorites() -> pd.DataFrame:
    """Retrieve all favorited events as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT e.*, f.id as fav_id, f.added_at
        FROM favorites f
        JOIN events e ON f.event_id = e.id
        ORDER BY f.added_at DESC
    """, conn)
    conn.close()
    return df


def add_favorite(event_id: int) -> bool:
    """Add an event to favorites. Returns True on success, False if already exists."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO favorites (event_id) VALUES (?)", (event_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def remove_favorite(event_id: int):
    """Remove an event from favorites."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()


def is_favorite(event_id: int) -> bool:
    """Check if an event is in favorites."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM favorites WHERE event_id = ?", (event_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ─── Analytics helpers ────────────────────────────────────────────────────────

def get_stats() -> dict:
    """Return platform-level statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM favorites")
    total_favorites = cursor.fetchone()[0]

    today = datetime.now().date().isoformat()
    cursor.execute("SELECT COUNT(*) FROM events WHERE date >= ?", (today,))
    upcoming = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT category) FROM events")
    categories = cursor.fetchone()[0]

    conn.close()
    return {
        "total_events": total_events,
        "total_favorites": total_favorites,
        "upcoming_events": upcoming,
        "categories": categories,
    }


def get_events_by_category() -> pd.DataFrame:
    """Return event counts grouped by category."""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT category, COUNT(*) as count
        FROM events GROUP BY category ORDER BY count DESC
    """, conn)
    conn.close()
    return df


def get_upcoming_events(limit: int = 5) -> pd.DataFrame:
    """Return the next N upcoming events."""
    today = datetime.now().date().isoformat()
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM events WHERE date >= ? ORDER BY date ASC LIMIT ?
    """, conn, params=(today, limit))
    conn.close()
    return df
