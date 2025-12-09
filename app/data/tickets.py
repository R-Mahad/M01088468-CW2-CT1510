# app/data/tickets.py
import sqlite3
from typing import List, Dict, Optional


def insert_ticket(
    conn: sqlite3.Connection,
    title: str,
    priority: str,
    status: str = "open",
    created_date: str | None = None,
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
        """,
        (title, priority, status, created_date),
    )
    conn.commit()
    return cursor.lastrowid


def get_all_tickets(conn: sqlite3.Connection) -> List[Dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_ticket_by_id(
    conn: sqlite3.Connection, ticket_id: int
) -> Optional[Dict]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE id = ?",
        (ticket_id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def update_ticket_status(
    conn: sqlite3.Connection, ticket_id: int, new_status: str
) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE it_tickets
        SET status = ?
        WHERE id = ?
        """,
        (new_status, ticket_id),
    )
    conn.commit()
    return cursor.rowcount


def delete_ticket(conn: sqlite3.Connection, ticket_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE id = ?",
        (ticket_id,),
    )
    conn.commit()
    return cursor.rowcount

