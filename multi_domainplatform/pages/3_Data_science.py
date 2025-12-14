import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from app.data.db import connect_database
from app.data.datasets import get_all_datasets  # <-- if your function name differs, change this line only

from models.dataset import Dataset

DATASETS_TABLE = "datasets_metadata"  


st.set_page_config(
    page_title="Data Science",
    page_icon="📦",
    layout="wide"
)

# ---- Session defaults ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"

# ---- Guard ----
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("home.py")  # change to Home.py if needed
    st.stop()

# ---- Header ----
st.title("📦 Data Science Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# ---- Load datasets from DB using your existing function ----
try:
    conn = connect_database()
    datasets_df = get_all_datasets(conn)

    if not isinstance(datasets_df, pd.DataFrame):
        datasets_df = pd.DataFrame(datasets_df)

except Exception as e:
    st.error(f"Failed to load dataset table: {e}")
    st.stop()

if datasets_df.empty:
    st.info("No dataset data found.")
    st.stop()

# ---- Sidebar filters ----
st.sidebar.header("Filters")

filtered = datasets_df.copy()

# Category filter
if "category" in filtered.columns:
    cat_opts = sorted(filtered["category"].dropna().unique().tolist())
    selected_cat = st.sidebar.multiselect("Category", cat_opts, default=cat_opts)
    filtered = filtered[filtered["category"].isin(selected_cat)]

# Source filter
if "source" in filtered.columns:
    src_opts = sorted(filtered["source"].dropna().unique().tolist())
    selected_src = st.sidebar.multiselect("Source", src_opts, default=src_opts)
    filtered = filtered[filtered["source"].isin(selected_src)]

# Search by name
search = st.sidebar.text_input("Search dataset name", "").strip().lower()
if search and "name" in filtered.columns:
    filtered = filtered[filtered["name"].astype(str).str.lower().str.contains(search)]

# Size range (if size exists)
if "size" in filtered.columns and not filtered.empty:
    min_size = int(filtered["size"].min())
    max_size = int(filtered["size"].max())
    size_range = st.sidebar.slider("Size range", min_size, max_size, (min_size, max_size))
    filtered = filtered[(filtered["size"] >= size_range[0]) & (filtered["size"] <= size_range[1])]

# ---- OOP conversion (Week 11 requirement) ----
dataset_objects = []

if not filtered.empty:
    for _, r in filtered.iterrows():
        dataset_objects.append(
            Dataset(
                int(r.get("id", 0) or 0),
                str(r.get("name", "Unnamed Dataset")),
                str(r.get("source", "Unknown")),
                str(r.get("category", "Other")),
                int(r.get("size", 0) or 0),
            )
        )

# ---- Metrics using object methods ----
st.subheader("Dataset Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Datasets (filtered)", len(dataset_objects))

with c2:
    avg_size = int(filtered["size"].mean()) if ("size" in filtered.columns and not filtered.empty) else 0
    st.metric("Average size", avg_size)

with c3:
    big_count = sum(1 for d in dataset_objects if d.size_mb() > 1)
    st.metric("Datasets > 1MB", big_count)

st.divider()

st.subheader("Dataset Actions")

with st.expander("➕ Add / 🗑 Delete Dataset", expanded=False):

    def table_columns(table_name: str) -> list[str]:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in cur.fetchall()]

    cols_in_table = table_columns(DATASETS_TABLE)

    tab_add, tab_delete = st.tabs(["➕ Add dataset", "🗑 Delete dataset"])

    # -------------------------
    # ADD DATASET
    # -------------------------
    with tab_add:
        with st.form("add_dataset_form", clear_on_submit=True):
            name = st.text_input("Name", placeholder="e.g., Customer Churn Dataset")
            source = st.text_input("Source", placeholder="e.g., Kaggle / Internal / API")
            category = st.text_input("Category", placeholder="e.g., Finance / Health / Cyber")
            size = st.number_input("Size (bytes)", min_value=0, value=0, step=1000)

            submitted = st.form_submit_button("Create dataset")

        if submitted:
            new_row = {}

            if "name" in cols_in_table:
                new_row["name"] = name.strip()
            if "source" in cols_in_table:
                new_row["source"] = source.strip()
            if "category" in cols_in_table:
                new_row["category"] = category.strip()
            if "size" in cols_in_table:
                new_row["size"] = int(size)

            if "name" in new_row and not new_row["name"]:
                st.error("Name is required.")
            else:
                try:
                    columns = ", ".join(new_row.keys())
                    placeholders = ", ".join(["?"] * len(new_row))
                    values = tuple(new_row.values())

                    sql = f"INSERT INTO {DATASETS_TABLE} ({columns}) VALUES ({placeholders})"
                    cur = conn.cursor()
                    cur.execute(sql, values)
                    conn.commit()

                    st.success("Dataset created successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to create dataset: {e}")

    # -------------------------
    # DELETE DATASET
    # -------------------------
    with tab_delete:
        if datasets_df.empty or "id" not in datasets_df.columns:
            st.info("No datasets available to delete (or missing 'id' column).")
        else:
            dataset_ids = sorted(set(datasets_df["id"].dropna().astype(int).tolist()))
            chosen_id = st.selectbox("Dataset ID", dataset_ids)

            if "name" in datasets_df.columns:
                name_preview = datasets_df.loc[datasets_df["id"] == chosen_id, "name"]
                if not name_preview.empty:
                    st.write("Selected:", name_preview.iloc[0])

            confirm = st.checkbox("I understand this will permanently delete the dataset.")
            if st.button("Delete dataset", disabled=not confirm):
                try:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM {DATASETS_TABLE} WHERE id = ?", (chosen_id,))
                    conn.commit()

                    st.success(f"Dataset {chosen_id} deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete dataset: {e}")


# ---- Graphs (different from Cybersecurity) ----
g1, g2, g3 = st.columns(3)

with g1:
    st.subheader("Datasets by Category")
    if "category" in filtered.columns and not filtered.empty:
        st.bar_chart(filtered["category"].value_counts())
    else:
        st.info("No category data to chart.")

with g2:
    st.subheader("Datasets by Source")
    if "source" in filtered.columns and not filtered.empty:
        st.bar_chart(filtered["source"].value_counts())
    else:
        st.info("No source data to chart.")

with g3:
    st.subheader("Size Scatter (ID vs Size)")
    if "size" in filtered.columns and not filtered.empty:
        fig = plt.figure()
        x = filtered["id"] if "id" in filtered.columns else range(len(filtered))
        plt.scatter(x, filtered["size"])
        plt.xlabel("Dataset ID")
        plt.ylabel("Size")
        st.pyplot(fig)
    else:
        st.info("No size data to chart.")

st.divider()

# ---- Table (from objects -> dict) ----
st.subheader("Datasets Table (Filtered)")

if not dataset_objects:
    st.info("No datasets match your filters.")
else:
    st.dataframe(pd.DataFrame([d.to_dict() for d in dataset_objects]), use_container_width=True)

# ---- Logout ----
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "user"
    st.switch_page("home.py")  # change to Home.py if needed
