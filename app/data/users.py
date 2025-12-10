# app/data/users.py
import sqlite3
import bcrypt


def hash_password(plain_text_password):
    """
    Hash a password using bcrypt.
    """
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_text_password, hashed_password):
    """
    Check a plaintext password against a stored hash.
    """
    password_bytes = plain_text_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def insert_user(conn, username, plain_password, role="user"):
    """
    Insert a new user row.

    Returns True if inserted, False if username already exists.
    """
    cur = conn.cursor()
    password_hash = hash_password(plain_password)

    try:
        cur.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Username already taken (UNIQUE)
        return False


def get_user_by_username(conn, username):
    """
    Return a single user row by username, or None.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,),
    )
    return cur.fetchone()


def get_all_users(conn):
    """
    Return all users (id, username, role).
    """
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    return cur.fetchall()


def update_user_role(conn, username, new_role):
    """
    Update the role of a user. Returns number of rows updated.
    """
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (new_role, username),
    )
    conn.commit()
    return cur.rowcount


def delete_user(conn, username):
    """
    Delete a user by username. Returns number of rows deleted.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    return cur.rowcount
