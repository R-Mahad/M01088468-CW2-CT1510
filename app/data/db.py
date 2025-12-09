# app/data/db.py
from pathlib import Path
import sqlite3


# Default DB path used everywhere
DB_PATH = Path("DATA") / "intelligence_platform.db"


def connect_database(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    """
    Connect to the SQLite database (and create it if it does not exist).
    Sets row_factory so you can access columns by name.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)  # make sure DATA/ exists

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
