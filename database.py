from pathlib import Path

from app.data.db import connect_database
from app.data.users import verify_password, insert_user


class DatabaseManager:
    """
    Helper class for the Streamlit app.
    Reuses the Week 8 database functions.
    """

    def __init__(self, db_path: str = "DATA/intelligence_platform.db"):
        self.db_path = Path(db_path)
        self.conn = connect_database(str(self.db_path))

    def verify_user(self, username: str, plain_password: str):
        """
        Check username and password against the users table.
        Returns (True, role) if correct, otherwise (False, None).
        """
        cur = self.conn.cursor()
        cur.execute(
            "SELECT password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()
        if row is None:
            return False, None

        password_hash, role = row

        if verify_password(plain_password, password_hash):
            return True, role

        return False, None

    def register_user(self, username: str, plain_password: str, role: str = "user"):
        """
        Register a new user in the database.
        Returns True if created, False if the username already exists.
        """
        return insert_user(self.conn, username, plain_password, role)

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
