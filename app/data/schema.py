# app/data/schema.py
import sqlite3
from .db import connect_database, DB_PATH


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create all required tables if they do not already exist.
    """
    cursor = conn.cursor()

    # users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
        """
    )

    # cyber_incidents
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            date TEXT
        )
        """
    )

    # datasets_metadata
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT,
            category TEXT,
            size INTEGER
        )
        """
    )

    # it_tickets
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT
        )
        """
    )

    conn.commit()


# Small helper so you can also run this file directly if needed:
if __name__ == "__main__":
    conn = connect_database(DB_PATH)
    create_tables(conn)
    conn.close()
