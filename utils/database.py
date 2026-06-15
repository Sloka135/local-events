"""
Database utility module for Radius.
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

    # Create registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            UNIQUE(event_id, email)
        )
    """)

    # Create reminders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            remind_days_before INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            UNIQUE(event_id, email)
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
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM events ORDER BY date ASC", conn)
    conn.close()
    return df


def get_event_by_id(event_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_event(title, category, location, latitude, longitude, date, description) -> int:
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


# ─── Favorites CRUD ──────────────────────────────────────────────────────────

def get_favorites() -> pd.DataFrame:
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()


def is_favorite(event_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM favorites WHERE event_id = ?", (event_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ─── Registrations CRUD ──────────────────────────────────────────────────────

def register_for_event(event_id: int, name: str, email: str, phone: str = "") -> bool:
    """Register a user for an event. Returns True on success, False if already registered."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO registrations (event_id, name, email, phone)
            VALUES (?, ?, ?, ?)
        """, (event_id, name, email, phone))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def is_registered(event_id: int, email: str) -> bool:
    """Check if an email is already registered for an event."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM registrations WHERE event_id = ? AND email = ?",
        (event_id, email)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_registration_count(event_id: int) -> int:
    """Get number of registrations for an event."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM registrations WHERE event_id = ?",
        (event_id,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ─── Reminders CRUD ──────────────────────────────────────────────────────────

def set_reminder(event_id: int, name: str, email: str, days_before: int = 1) -> bool:
    """Set a reminder for an event. Returns True on success, False if already set."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reminders (event_id, name, email, remind_days_before)
            VALUES (?, ?, ?, ?)
        """, (event_id, name, email, days_before))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def has_reminder(event_id: int, email: str) -> bool:
    """Check if a reminder is already set for this event and email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM reminders WHERE event_id = ? AND email = ?",
        (event_id, email)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def remove_reminder(event_id: int, email: str):
    """Remove a reminder."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM reminders WHERE event_id = ? AND email = ?",
        (event_id, email)
    )
    conn.commit()
    conn.close()


# ─── Analytics helpers ────────────────────────────────────────────────────────

def get_stats() -> dict:
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

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total_registrations = cursor.fetchone()[0]

    conn.close()
    return {
        "total_events":        total_events,
        "total_favorites":     total_favorites,
        "upcoming_events":     upcoming,
        "categories":          categories,
        "total_registrations": total_registrations,
    }


def get_events_by_category() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT category, COUNT(*) as count
        FROM events GROUP BY category ORDER BY count DESC
    """, conn)
    conn.close()
    return df


def get_upcoming_events(limit: int = 5) -> pd.DataFrame:
    today = datetime.now().date().isoformat()
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM events WHERE date >= ? ORDER BY date ASC LIMIT ?
    """, conn, params=(today, limit))
    conn.close()
    return df