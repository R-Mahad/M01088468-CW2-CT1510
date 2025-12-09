import pandas as pd

def load_cyber_incidents_csv(conn, csv_path="DATA/cyber_incidents.csv"):
    df = pd.read_csv(csv_path)
    df.to_sql("cyber_incidents", conn, if_exists="append", index=False)


def load_datasets_csv(conn, csv_path="DATA/datasets_metadata.csv"):
    df = pd.read_csv(csv_path)
    df.to_sql("datasets_metadata", conn, if_exists="append", index=False)


def load_it_tickets_csv(conn, csv_path="DATA/it_tickets.csv"):
    df = pd.read_csv(csv_path)
    df.to_sql("it_tickets", conn, if_exists="append", index=False)
