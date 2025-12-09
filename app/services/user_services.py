import bcrypt

def migrate_users_from_file(conn, file_path="C:\\Users\\rayaa\\OneDrive\\Desktop\\M01088468-CW2-CT1510\\M01088468-CW2-CT1510\\users.txt"):
    """
    Read users from a text file and insert them into the users table
    with hashed passwords.
    """
    cursor = conn.cursor()

    with open(file_path, "r") as f:
        for line in f:
            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            username, password, role = line.split(",")

            # Hash the password
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Insert using parameterized query (SECURE)
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username.strip(), hashed.decode("utf-8"), role.strip()))

    conn.commit()