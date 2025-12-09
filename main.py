# main.py
from app.data.db import connect_database
from app.data.schema import create_tables
from app.data.users import (
    create_user,
    get_all_users,
    update_user_role,
    delete_user,
)
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
)
from app.data.datasets import (
    insert_dataset,
    get_all_datasets,
)
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
)
from app.services.user_service import migrate_users_from_file


def main() -> None:
    conn = connect_database()
    create_tables(conn)

    # 1. Migrate users from Week 7 file
    migrate_users_from_file(conn)

    # 2. Test User CRUD
    print("\n=== USERS ===")
    create_user(conn, "test_user", "dummy_hash", "tester")
    print("All users:", get_all_users(conn))
    update_user_role(conn, "test_user", "admin")
    print("After role update:", get_all_users(conn))
    delete_user(conn, "test_user")
    print("After delete:", get_all_users(conn))

    # 3. Test Incidents CRUD
    print("\n=== INCIDENTS ===")
    incident_id = insert_incident(conn, "Phishing email", "High")
    print("All incidents:", get_all_incidents(conn))
    update_incident_status(conn, incident_id, "closed")
    print("After status update:", get_all_incidents(conn))

    # 4. Test Datasets CRUD
    print("\n=== DATASETS ===")
    insert_dataset(conn, "Threat Intel Feed", "External", "Threat", 5000)
    print("All datasets:", get_all_datasets(conn))

    # 5. Test Tickets CRUD
    print("\n=== TICKETS ===")
    ticket_id = insert_ticket(conn, "Reset VPN password", "Medium")
    print("All tickets:", get_all_tickets(conn))

    conn.close()


if __name__ == "__main__":
    main()
