import streamlit as st
import pandas as pd

from database import DatabaseManager
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets


@st.cache_resource
def get_database():
    return DatabaseManager("DATA/intelligence_platform.db")


# DEBUG: prove this file is running
st.write("✅ Dashboard page loaded")


# ---------- AUTH GUARD ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must log in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

db = get_database()

st.title("📊 Dashboard")

st.write(f"Logged in as **{st.session_state.username}** (role: {st.session_state.role})")

# ---------- LOAD DATA ----------
incidents_df = get_all_incidents(db.conn)
tickets_df = get_all_tickets(db.conn)

# ---------- SIMPLE METRICS ----------
st.subheader("Quick stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total incidents", len(incidents_df))

with col2:
    high_count = (incidents_df["severity"] == "High").sum() if not incidents_df.empty else 0
    st.metric("High severity incidents", int(high_count))

with col3:
    open_tickets = (tickets_df["status"] == "in-progress").sum() if not tickets_df.empty else 0
    st.metric("IT tickets in progress", int(open_tickets))

st.divider()

# ---------- CHART EXAMPLE ----------
st.subheader("Incidents by severity")

if not incidents_df.empty:
    severity_counts = incidents_df["severity"].value_counts()
    chart_data = pd.DataFrame(
        {"severity": severity_counts.index, "count": severity_counts.values}
    ).set_index("severity")
    st.bar_chart(chart_data)
else:
    st.info("No incidents found in the database.")

st.divider()

# ---------- SIMPLE CRUD DEMO USING SESSION_STATE ----------
st.subheader("Demo: local records (session only)")

if "demo_records" not in st.session_state:
    st.session_state.demo_records = []

# CREATE
with st.form("create_record"):
    new_title = st.text_input("Record title")
    new_notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add record")
    if submitted:
        if new_title:
            st.session_state.demo_records.append(
                {"title": new_title, "notes": new_notes}
            )
            st.success("Record added.")
        else:
            st.warning("Title is required.")

# READ
if st.session_state.demo_records:
    st.write("Current records:")
    st.dataframe(st.session_state.demo_records)
else:
    st.info("No demo records yet. Add one using the form above.")

# UPDATE / DELETE
st.subheader("Update or delete a record")

if st.session_state.demo_records:
    index = st.number_input(
        "Select record index",
        min_value=0,
        max_value=len(st.session_state.demo_records) - 1,
        step=1,
        format="%d",
    )

    selected = st.session_state.demo_records[index]
    updated_title = st.text_input("Edit title", value=selected["title"], key="edit_title")
    updated_notes = st.text_area(
        "Edit notes", value=selected["notes"], key="edit_notes"
    )

    col_u, col_d = st.columns(2)
    with col_u:
        if st.button("Save changes"):
            st.session_state.demo_records[index] = {
                "title": updated_title,
                "notes": updated_notes,
            }
            st.success("Record updated.")
            st.experimental_rerun()

    with col_d:
        if st.button("Delete record"):
            st.session_state.demo_records.pop(index)
            st.success("Record deleted.")
            st.experimental_rerun()
else:
    st.caption("Nothing to update or delete yet.")

st.divider()

# ---------- LOG OUT ----------
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.success("You have been logged out.")
    st.switch_page("Home.py")
