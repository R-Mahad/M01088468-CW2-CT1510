# app/data/incidents.py
import pandas as pd


def get_all_incidents(conn):
    """
    Get all cyber incidents (newest first).
    """
    query = "SELECT * FROM cyber_incidents ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    return df


def get_incidents_by_severity(conn, severity):
    """
    Get incidents with a given severity.
    """
    query = """
    SELECT *
    FROM cyber_incidents
    WHERE severity = ?
    ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn, params=(severity,))
    return df


def get_incidents_by_status(conn, status):
    """
    Get incidents with a given status.
    """
    query = """
    SELECT *
    FROM cyber_incidents
    WHERE status = ?
    ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn, params=(status,))
    return df

def insert_incident(conn, title, severity, status="open", date=None, reported_by=None):
    """
    Insert one incident row.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cyber_incidents (title, severity, status, date, reported_by)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, severity, status, date, reported_by),
    )
    conn.commit()
