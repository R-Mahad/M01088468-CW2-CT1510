import sqlite3


def create_users_table(conn):
    """
    Create the users table if it does not exist.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table if it does not exist.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        date TEXT,
        reported_by TEXT,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table if it does not exist.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        source TEXT,
        category TEXT,
        size INTEGER
    )
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def create_it_tickets_table(conn):
    """
    Create the it_tickets table if it does not exist.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        created_date TEXT
    )
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def create_all_tables(conn):
    """
    Create all project tables.
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

