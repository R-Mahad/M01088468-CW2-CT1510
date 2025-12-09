# app/services/user_service.py
import bcrypt
from pathlib import Path
from app.data.users import get_user_by_username, insert_user

def register_user(username, password, role="user"):
    """Register new user with password hashing."""
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    insert_user(username, password_hash, role)


def migrate_users_from_file():
    """
    Read DATA/users.txt and add users to the database.

    Expected line formats:
        username,password,role
        username,password        (role defaults to 'user')
    Any empty or broken lines are skipped safely.
    """
    file_path = Path("DATA/users.txt")

    if not file_path.exists():
        print("[WARN] DATA/users.txt not found, skipping migration")
        return

    with file_path.open("r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            # skip empty lines
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]

            # not enough values → skip with message, but DON'T crash
            if len(parts) < 2:
                print(f"[WARN] Skipping line {line_no}: not enough values -> {raw_line!r}")
                continue

            username = parts[0]
            password = parts[1]
            role = parts[2] if len(parts) >= 3 else "user"

            # avoid duplicates
            if get_user_by_username(username):
                continue

            register_user(username, password, role)
