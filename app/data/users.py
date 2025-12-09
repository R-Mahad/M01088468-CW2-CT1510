import hashlib

def hash_password(password: str) -> str:
    """
    Hash the password using SHA-256.
    (In the workshop they use bcrypt, but this works without extra installs.)
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def migrate_users_from_file(conn, file_path="DATA/users.txt"):
    """
    Read users from a text file and insert into the users table.
    Each line in users.txt should look like:
        username,password,role
    """
    cursor = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            username, password, role = line.split(",")

            password_hash = hash_password(password.strip())

            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username.strip(), password_hash, role.strip())
            )

    conn.commit()
    print("Users migrated from file into database.")


def get_all_users(conn):
    """
    Return a list of (id, username, role) for all users.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    return cursor.fetchall()
