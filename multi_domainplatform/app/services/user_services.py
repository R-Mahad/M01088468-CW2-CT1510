# app/services/user_service.py
import sqlite3
import os

from app.data.users import hash_password


def migrate_users_from_file(conn, filepath="DATA/users.txt"):
    """
    Read users from users.txt and insert them into the users table.

    Supports lines like:
    username,plain_password
    or
    username,password_hash,role
    """
    if not os.path.exists(filepath):
        print("users.txt not found at {}. No users migrated.".format(filepath))
        return 0

    migrated = 0
    cur = conn.cursor()

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # If the file has a header row, you can skip it here by checking content.
    # For safety, we just skip completely empty lines.
    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")

        # At least username and a second value
        if len(parts) < 2:
            continue

        username = parts[0].strip()
        second = parts[1].strip()
        role = "user"

        if len(parts) >= 3:
            role = parts[2].strip() or "user"

        # If second part looks like a bcrypt hash (starts with $2),
        # use it directly, otherwise treat as plain password.
        if second.startswith("$2"):
            password_hash = second
        else:
            password_hash = hash_password(second)

        try:
            cur.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, role),
            )
            migrated += 1
        except sqlite3.IntegrityError:
            # Username already exists, skip
            continue

    conn.commit()
    return migrated
