# app/data/tickets.py
import pandas as pd


def get_all_tickets(conn):
    """
    Get all IT tickets.
    """
    query = "SELECT * FROM it_tickets ORDER BY id ASC"
    df = pd.read_sql_query(query, conn)
    return df


def insert_ticket(conn, title, priority, status="open", created_date=None):
    """
    Insert one IT ticket row.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
        """,
        (title, priority, status, created_date),
    )
    conn.commit()
