import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from app.data.db import connect_database
from app.data.tickets import get_all_tickets

from models.it_ticket import ITTicket

TICKETS_TABLE = "it_tickets"  # matches your DB


st.set_page_config(
    page_title="IT Operations",
    page_icon="🛠",
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
st.title("🛠 IT Operations Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")



# ---- Load tickets from DB using your existing function ----
try:
    conn = connect_database()
    tickets_df = get_all_tickets(conn)

    if not isinstance(tickets_df, pd.DataFrame):
        tickets_df = pd.DataFrame(tickets_df)

except Exception as e:
    st.error(f"Failed to load ticket table: {e}")
    st.stop()

if tickets_df.empty:
    st.info("No ticket data found.")
    st.stop()

# ---- Sidebar filters ----
st.sidebar.header("Filters")

filtered = tickets_df.copy()

# Priority filter
if "priority" in filtered.columns:
    prio_opts = sorted(filtered["priority"].dropna().unique().tolist())
    selected_prio = st.sidebar.multiselect("Priority", prio_opts, default=prio_opts)
    filtered = filtered[filtered["priority"].isin(selected_prio)]

# Status filter
if "status" in filtered.columns:
    status_opts = sorted(filtered["status"].dropna().unique().tolist())
    selected_status = st.sidebar.multiselect("Status", status_opts, default=status_opts)
    filtered = filtered[filtered["status"].isin(selected_status)]

# Date range filter (created_date if available)
date_col = "created_date" if "created_date" in filtered.columns else ("date" if "date" in filtered.columns else None)
if date_col:
    filtered[date_col] = pd.to_datetime(filtered[date_col], errors="coerce")
    min_d = filtered[date_col].min()
    max_d = filtered[date_col].max()
    if pd.notna(min_d) and pd.notna(max_d):
        date_range = st.sidebar.date_input("Date range", value=(min_d.date(), max_d.date()))
        if date_range and len(date_range) == 2:
            start = pd.to_datetime(date_range[0])
            end = pd.to_datetime(date_range[1])
            filtered = filtered[(filtered[date_col] >= start) & (filtered[date_col] <= end)]

# Search by title
search = st.sidebar.text_input("Search ticket title", "").strip().lower()
if search and "title" in filtered.columns:
    filtered = filtered[filtered["title"].astype(str).str.lower().str.contains(search)]

# ---- OOP conversion (Week 11 requirement) ----
ticket_objects = []

if not filtered.empty:
    for _, r in filtered.iterrows():
        ticket_objects.append(
            ITTicket(
                ticket_id=int(r.get("id", 0) or 0),
                title=str(r.get("title", "Untitled Ticket")),
                priority=str(r.get("priority", "Low")),
                status=str(r.get("status", "open")),
                created_date=str(r.get(date_col, "")) if date_col else "",
            )
        )

# ---- Metrics using object methods ----
st.subheader("Ticket Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Tickets (filtered)", len(ticket_objects))

with c2:
    st.metric("High priority", sum(1 for t in ticket_objects if t.is_high_priority()))

with c3:
    st.metric("Active (open / in-progress)", sum(1 for t in ticket_objects if t.is_active()))

st.divider()
st.subheader("Ticket Actions")

with st.expander("➕ Add / 🗑 Delete Ticket", expanded=False):

    def table_columns(table_name: str) -> list[str]:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in cur.fetchall()]

    cols_in_table = table_columns(TICKETS_TABLE)

    tab_add, tab_delete = st.tabs(["➕ Add ticket", "🗑 Delete ticket"])

    # -------------------------
    # ADD TICKET
    # -------------------------
    with tab_add:
        priority_options = ["Low", "Medium", "High"]
        status_options = ["open", "in-progress", "closed"]

        with st.form("add_ticket_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="e.g., Wi-Fi not working in Lab 2")
            priority = st.selectbox("Priority", priority_options, index=1)
            status = st.selectbox("Status", status_options, index=0)
            created_date = st.date_input("Created date")

            submitted = st.form_submit_button("Create ticket")

        if submitted:
            new_row = {}

            if "title" in cols_in_table:
                new_row["title"] = title.strip()
            if "priority" in cols_in_table:
                new_row["priority"] = priority
            if "status" in cols_in_table:
                new_row["status"] = status
            if "created_date" in cols_in_table:
                new_row["created_date"] = str(created_date)
            elif "date" in cols_in_table:
                new_row["date"] = str(created_date)

            if "title" in new_row and not new_row["title"]:
                st.error("Title is required.")
            else:
                try:
                    columns = ", ".join(new_row.keys())
                    placeholders = ", ".join(["?"] * len(new_row))
                    values = tuple(new_row.values())

                    sql = f"INSERT INTO {TICKETS_TABLE} ({columns}) VALUES ({placeholders})"
                    cur = conn.cursor()
                    cur.execute(sql, values)
                    conn.commit()

                    st.success("Ticket created successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to create ticket: {e}")

    # -------------------------
    # DELETE TICKET
    # -------------------------
    with tab_delete:
        if tickets_df.empty or "id" not in tickets_df.columns:
            st.info("No tickets available to delete (or missing 'id' column).")
        else:
            ticket_ids = sorted(set(tickets_df["id"].dropna().astype(int).tolist()))
            chosen_id = st.selectbox("Ticket ID", ticket_ids)

            if "title" in tickets_df.columns:
                title_preview = tickets_df.loc[tickets_df["id"] == chosen_id, "title"]
                if not title_preview.empty:
                    st.write("Selected:", title_preview.iloc[0])

            confirm = st.checkbox("I understand this will permanently delete the ticket.")
            if st.button("Delete ticket", disabled=not confirm):
                try:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM {TICKETS_TABLE} WHERE id = ?", (chosen_id,))
                    conn.commit()

                    st.success(f"Ticket {chosen_id} deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete ticket: {e}")


# ---- Graphs (different from other pages) ----
g1, g2, g3 = st.columns(3)

with g1:
    st.subheader("Tickets by Status (Area)")
    if "status" in filtered.columns and not filtered.empty:
        counts = filtered["status"].value_counts()
        st.area_chart(counts)
    else:
        st.info("No status data to chart.")

with g2:
    st.subheader("Priority Distribution (Pie)")
    if "priority" in filtered.columns and not filtered.empty:
        counts = filtered["priority"].value_counts()
        fig = plt.figure()
        plt.pie(counts.values, labels=counts.index, autopct="%1.0f%%")
        st.pyplot(fig)
    else:
        st.info("No priority data to chart.")

with g3:
    st.subheader("Tickets by Priority (Bar)")
    if "priority" in filtered.columns and not filtered.empty:
        st.bar_chart(filtered["priority"].value_counts())
    else:
        st.info("No priority data to chart.")

st.divider()

# ---- Table (from objects -> dict) ----
st.subheader("Tickets Table (Filtered)")

if not ticket_objects:
    st.info("No tickets match your filters.")
else:
    st.dataframe(pd.DataFrame([t.to_dict() for t in ticket_objects]), use_container_width=True)

# ---- Logout ----
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "user"
    st.switch_page("home.py")  # change to Home.py if needed
