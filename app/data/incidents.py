def insert_incident(conn, title, severity, status="open", date=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (title, severity, status, date)
        VALUES (?, ?, ?, ?)
    """, (title, severity, status, date))
    conn.commit()


def get_all_incidents(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    return cursor.fetchall()


def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """, (new_status, incident_id))
    conn.commit()


def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
