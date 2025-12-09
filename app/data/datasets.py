def insert_dataset(conn, name, source, category, size):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))
    conn.commit()


def get_all_datasets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata")
    return cursor.fetchall()


def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
