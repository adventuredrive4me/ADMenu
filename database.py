# ==========================================================
# ADMENU APP ENGINE PRO
# Database Engine
#
# Creates the SQLite database and all required tables.
# ==========================================================

import sqlite3
import os

from config import DATABASE_NAME


def get_connection():
    """Connect to SQLite database."""

    folder = os.path.dirname(DATABASE_NAME)

    if folder:
        os.makedirs(folder, exist_ok=True)

    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """Create database tables if they don't exist."""

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # Trips
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        trip_name TEXT,

        start_date TEXT,

        end_date TEXT,

        total_days INTEGER,

        total_nights INTEGER,

        currency TEXT,

        exchange_rate REAL

    )
    """)

    # ------------------------------------------------------
    # Stops
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stops(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        trip_id INTEGER,

        stop_day TEXT,

        stop_type TEXT,

        restaurant_name TEXT,

        phone TEXT,

        email TEXT,

        address TEXT,

        arrival_datetime TEXT,

        status TEXT

    )
    """)

    # ------------------------------------------------------
    # Guests
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guests(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        guest_name TEXT,

        car_number TEXT,

        room_number TEXT

    )
    """)

    # ------------------------------------------------------
    # Menu
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        stop_id INTEGER,

        item_name TEXT,

        course TEXT,

        unit TEXT,

        ratio REAL,

        price REAL,

        menu_type TEXT,

        display INTEGER

    )
    """)

    # ------------------------------------------------------
    # Orders
    # ------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        guest_id INTEGER,

        stop_id INTEGER,

        menu_id INTEGER,

        quantity INTEGER

    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")
