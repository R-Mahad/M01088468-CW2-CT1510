# app/data/datasets.py
import sqlite3
from typing import List, Dict, Optional


def insert_dataset(
    conn: sqlite3.Connection,
    name: str,
    source: str | None = None,
    category: str | None = None,
    size: int | None = None,
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
        """,
        (name, source, category, size),
    )
    conn.commit()
    return cursor.lastrowid


def get_all_datasets(conn: sqlite3.Connection) -> List[Dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_dataset_by_id(
    conn: sqlite3.Connection, dataset_id: int
) -> Optional[Dict]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE id = ?",
        (dataset_id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def update_dataset_category(
    conn: sqlite3.Connection, dataset_id: int, new_category: str
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE datasets_metadata
        SET category = ?
        WHERE id = ?
        """,
        (new_category, dataset_id),
    )
    conn.commit()
    return cursor.rowcount


def delete_dataset(conn: sqlite3.Connection, dataset_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,),
    )
    conn.commit()
    return cursor.rowcount
