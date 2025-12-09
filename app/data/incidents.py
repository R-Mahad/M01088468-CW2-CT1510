# app/data/incidents.py
import sqlite3
from typing import List, Dict, Optional


def insert_incident(
    conn: sqlite3.Connection,
    title: str,
    severity: str,
    status: str = "open",
    date: str | None = None,
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents (title, severity, status, date)
        VALUES (?, ?, ?, ?)
        """,
        (title, severity, status, date),
    )
    conn.commit()
    return cursor.lastrowid


def get_all_incidents(conn: sqlite3.Connection) -> List[Dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_incident_by_id(
    conn: sqlite3.Connection, incident_id: int
) -> Optional[Dict]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        (incident_id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def update_incident_status(
    conn: sqlite3.Connection, incident_id: int, new_status: str
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
        """,
        (new_status, incident_id),
    )
    conn.commit()
    return cursor.rowcount


def delete_incident(conn: sqlite3.Connection, incident_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,),
    )
    conn.commit()
    return cursor.rowcount
