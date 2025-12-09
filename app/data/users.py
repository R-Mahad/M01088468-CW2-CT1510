import hashlib

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def migrate_users_from_file(conn, file_path):
    """
    Read users from a text file and insert them into the users table.
    Each valid line must be: username,password,role
    """
    cursor = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                # skip empty lines
                continue

            # skip header if present
            if line.lower().startswith("username"):
                continue

            parts = [p.strip() for p in line.split(",")]

            if len(parts) != 3:
                # bad line format – don't crash, just skip
                print(f"Skipping invalid line in users file: {line!r}")
                continue

            username, password, role = parts
            password_hash = hash_password(password)

            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, role)
            )

    conn.commit()
    print("Users migrated from file into database.")


def get_all_users(conn):
    """
    Return all users as (id, username, role) rows.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    return cursor.fetchall()
