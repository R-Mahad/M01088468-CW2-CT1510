import streamlit as st
import pandas as pd

from database import DatabaseManager
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets


@st.cache_resource
def get_database():
    return DatabaseManager("DATA/intelligence_platform.db")


# DEBUG
st.write("📈 Analytics page loaded")


# ---------- AUTH GUARD ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must log in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

db = get_database()

st.title("📈 Domain Analytics")

domain = st.selectbox(
    "Select domain",
    ["Cybersecurity (Incidents)", "IT Operations (Tickets)"],
)

if domain.startswith("Cyber"):
    st.subheader("Cybersecurity incident analytics")

    incidents_df = get_all_incidents(db.conn)

    if incidents_df.empty:
        st.info("No incident data available.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total incidents", len(incidents_df))
        with col2:
            critical_count = (incidents_df["severity"] == "Critical").sum()
            st.metric("Critical incidents", int(critical_count))

        status_counts = incidents_df["status"].value_counts()
        status_chart = pd.DataFrame(
            {"status": status_counts.index, "count": status_counts.values}
        ).set_index("status")

        st.subheader("Incidents by status")
        st.bar_chart(status_chart)

else:
    st.subheader("IT Operations analytics")

    tickets_df = get_all_tickets(db.conn)

    if tickets_df.empty:
        st.info("No ticket data available.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total tickets", len(tickets_df))
        with col2:
            high_priority = (tickets_df["priority"] == "High").sum()
            st.metric("High priority tickets", int(high_priority))

        status_counts = tickets_df["status"].value_counts()
        status_chart = pd.DataFrame(
            {"status": status_counts.index, "count": status_counts.values}
        ).set_index("status")

        st.subheader("Tickets by status")
        st.area_chart(status_chart)
