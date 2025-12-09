import sqlite3
import os

def connect_database(db_path="DATA/intelligence_platform.db"):
    """
    Create a connection to the SQLite database.
    If the folder does not exist, it will be created.
    """
    # make sure the DATA folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None

