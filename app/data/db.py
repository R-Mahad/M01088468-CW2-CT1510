# app/data/db.py
import sqlite3
import os

DB_PATH = "DATA/intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database file.
    Creates the folder/file if they don't exist.
    """
    # Make sure DATA folder exists
    folder = os.path.dirname(db_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn
