def insert_ticket(conn, title, priority, status="open", created_date=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
    """, (title, priority, status, created_date))
    conn.commit()


def get_all_tickets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets")
    return cursor.fetchall()


def update_ticket_status(conn, ticket_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets
        SET status = ?
        WHERE id = ?
    """, (new_status, ticket_id))
    conn.commit()


def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
