from app.data.db import connect_database
from app.data.schema import create_tables
from app.data.users import migrate_users_from_file, get_all_users
from app.data.load_data import (
    load_cyber_incidents_csv,
    load_datasets_csv,
    load_it_tickets_csv,
)


def main():
    # 1. connect to database
    conn = connect_database()
    if conn is None:
        return

    # 2. create tables
    create_tables(conn)

    # 3. migrate users from users.txt
    migrate_users_from_file(conn, "DATA/users.txt")

    # 4. load CSV data into the other tables
    load_cyber_incidents_csv(conn)
    load_datasets_csv(conn)
    load_it_tickets_csv(conn)

    # 5. quick check – print users and row counts
    print("\nUsers in database:")
    for row in get_all_users(conn):
        print(row)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
    print("cyber_incidents rows:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
    print("datasets_metadata rows:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM it_tickets")
    print("it_tickets rows:", cursor.fetchone()[0])

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()

