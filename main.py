import pandas as pd  # used by some helper functions


from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import migrate_users_from_file
from app.data.users import insert_user, get_all_users
from app.data.incidents import (
    get_all_incidents,
    get_incidents_by_severity,
    get_incidents_by_status,
)
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets


def main():
    # Connect and set up tables
    conn = connect_database()
    create_all_tables(conn)

    # Migrate users from Week 7 file (if it exists)
    migrated = migrate_users_from_file(conn)
    if migrated > 0:
        print("Migrated {} user(s) from users.txt".format(migrated))

        # 4. Load CSV data into the database
    try:
        pd.read_csv("DATA/cyber_incidents.csv").to_sql(
            "cyber_incidents", conn, if_exists="append", index=False
        )
        pd.read_csv("DATA/datasets_metadata.csv").to_sql(
            "datasets_metadata", conn, if_exists="append", index=False
        )
        pd.read_csv("DATA/it_tickets.csv").to_sql(
            "it_tickets", conn, if_exists="append", index=False
        )
        print("Loaded CSV data into tables")
    except FileNotFoundError as e:
        print("CSV file not found:", e)


    # Optional: create a demo user for testing
    inserted = insert_user(conn, "alice", "SecurePass123", role="admin")
    if inserted:
        print("Created demo user 'alice'.")

    print("\n=== Users ===")
    for row in get_all_users(conn):
        print(row)

    print("\n=== All incidents ===")
    print(get_all_incidents(conn))

    print("\n=== High severity incidents ===")
    print(get_incidents_by_severity(conn, "High"))

    print("\n=== Open incidents ===")
    print(get_incidents_by_status(conn, "open"))

    print("\n=== Datasets ===")
    print(get_all_datasets(conn))

    print("\n=== IT Tickets ===")
    print(get_all_tickets(conn))

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()

