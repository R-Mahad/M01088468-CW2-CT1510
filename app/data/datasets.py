# app/data/datasets.py
import pandas as pd


def get_all_datasets(conn):
    """
    Get all dataset metadata rows.
    """
    query = "SELECT * FROM datasets_metadata ORDER BY id ASC"
    df = pd.read_sql_query(query, conn)
    return df


def insert_dataset(conn, name, source, category, size=None):
    """
    Insert one dataset metadata row.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
        """,
        (name, source, category, size),
    )
    conn.commit()
