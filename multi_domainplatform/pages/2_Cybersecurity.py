import streamlit as st
import pandas as pd

from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets

from models.security_incident import SecurityIncident
from models.it_ticket import ITTicket


st.set_page_config(
    page_title="Cybersecurity",
    page_icon="🛡",
    layout="wide"
)



INCIDENTS_TABLE = "cyber_incidents"


# --------------------------
# Session checks (only set if missing)
# --------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"

# --------------------------
# Guard: if not logged in, send user back
# --------------------------
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("home.py") 

# --------------------------
# Page header
# --------------------------
st.title("🛡 Cybersecurity Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# --------------------------
# Load data from DB using your existing functions
# --------------------------
try:
    conn = connect_database()

    incidents_df = get_all_incidents(conn)
    tickets_df = get_all_tickets(conn)

    # If your functions already return DataFrames, this keeps them as-is.
    # If they return lists, this safely turns them into DataFrames.
    if not isinstance(incidents_df, pd.DataFrame):
        incidents_df = pd.DataFrame(incidents_df)

    if not isinstance(tickets_df, pd.DataFrame):
        tickets_df = pd.DataFrame(tickets_df)

except Exception as e:
    st.error(f"Failed to load tables: {e}")
    st.stop()


# --------------------------
# Sidebar filters (real dashboard-style filters)
# --------------------------
st.sidebar.header("Filters")

filtered_incidents = incidents_df.copy()

# Severity filter
if not filtered_incidents.empty and "severity" in filtered_incidents.columns:
    severity_options = sorted(filtered_incidents["severity"].dropna().unique().tolist())
    selected_severity = st.sidebar.multiselect("Severity", severity_options, default=severity_options)
    filtered_incidents = filtered_incidents[filtered_incidents["severity"].isin(selected_severity)]

# Status filter
if not filtered_incidents.empty and "status" in filtered_incidents.columns:
    status_options = sorted(filtered_incidents["status"].dropna().unique().tolist())
    selected_status = st.sidebar.multiselect("Status", status_options, default=status_options)
    filtered_incidents = filtered_incidents[filtered_incidents["status"].isin(selected_status)]

# Date range filter (only if "date" exists)
if not filtered_incidents.empty and "date" in filtered_incidents.columns:
    filtered_incidents["date"] = pd.to_datetime(filtered_incidents["date"], errors="coerce")
    min_d = filtered_incidents["date"].min()
    max_d = filtered_incidents["date"].max()

    if pd.notna(min_d) and pd.notna(max_d):
        date_range = st.sidebar.date_input("Date range", value=(min_d.date(), max_d.date()))
        if date_range and len(date_range) == 2:
            start = pd.to_datetime(date_range[0])
            end = pd.to_datetime(date_range[1])
            filtered_incidents = filtered_incidents[
                (filtered_incidents["date"] >= start) & (filtered_incidents["date"] <= end)
            ]

# Search filter
search_text = st.sidebar.text_input("Search (title/description/reported_by)", "").strip().lower()

if search_text and not filtered_incidents.empty:
    search_fields = [c for c in ["title", "description", "reported_by"] if c in filtered_incidents.columns]
    if search_fields:
        mask = False
        for f in search_fields:
            mask = mask | filtered_incidents[f].astype(str).str.lower().str.contains(search_text)
        filtered_incidents = filtered_incidents[mask]



# Convert filtered incidents into SecurityIncident objects
# --------------------------
incident_objects = []

if not filtered_incidents.empty:
    for _, r in filtered_incidents.iterrows():
        incident_objects.append(
            SecurityIncident(
                incident_id=int(r.get("id", 0) or 0),
                title=str(r.get("title", "Untitled")),
                incident_type=str(r.get("incident_type", r.get("type", "Unknown"))),
                severity=str(r.get("severity", "Low")),
                status=str(r.get("status", "open")),
                date=str(r.get("date", "")),
                description=str(r.get("description", "")),
                reported_by=r.get("reported_by", None),
            )
        )

# Convert tickets into ITTicket objects
ticket_objects = []

if not tickets_df.empty:
    for _, r in tickets_df.iterrows():
        ticket_objects.append(
            ITTicket(
                ticket_id=int(r.get("id", 0) or 0),
                title=str(r.get("title", "Untitled Ticket")),
                priority=str(r.get("priority", "Low")),
                status=str(r.get("status", "open")),
                created_date=str(r.get("created_date", r.get("date", ""))),
            )
        )


# --------------------------
# Metrics 
st.subheader("Security Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total incidents (filtered)", len(incident_objects))

with col2:
    st.metric("High/Critical", sum(1 for i in incident_objects if i.is_high_risk()))

with col3:
    st.metric("Open/In progress", sum(1 for i in incident_objects if i.is_open_or_in_progress()))

st.divider()

st.subheader("Incident Actions")

with st.expander("➕ Add / 🗑 Delete Incident", expanded=False):
    # We reuse your existing DB connection
    # conn already exists from connect_database()

    # --- Read columns from the actual table (so we don't guess) ---
    def table_columns(table_name: str) -> list[str]:
        try:
            cur = conn.cursor()
            cur.execute(f"PRAGMA table_info({table_name})")
            return [row[1] for row in cur.fetchall()]  # row[1] = column name
        except Exception:
            return []

    cols_in_table = table_columns(INCIDENTS_TABLE)

    if not cols_in_table:
        st.warning(
            f"Could not read table columns for '{INCIDENTS_TABLE}'. "
            "Check the table name."
        )
    else:
        tab_add, tab_delete = st.tabs(["➕ Add incident", "🗑 Delete incident"])

        # -------------------------
        # ADD INCIDENT
        # -------------------------
        with tab_add:
            st.caption("Fill in the form and click **Create incident**.")

            # Use dropdown options if columns exist in dataframe
            severity_options = ["Low", "Medium", "High", "Critical"]
            status_options = ["open", "in-progress", "closed"]

            # Build form
            with st.form("add_incident_form", clear_on_submit=True):
                title = st.text_input("Title", placeholder="e.g., Phishing email reported")

                # These fields may or may not exist in your table; we handle that below.
                incident_type = st.text_input("Incident type", placeholder="e.g., phishing / malware / access")
                severity = st.selectbox("Severity", severity_options, index=2)
                status = st.selectbox("Status", status_options, index=0)
                date_val = st.date_input("Date")
                description = st.text_area("Description", placeholder="Short description (optional)")
                reported_by = st.text_input("Reported by", placeholder="e.g., alice")

                submitted = st.form_submit_button("Create incident")

            if submitted:
                # Build row dict only with columns that actually exist in your DB table
                new_row = {}

                # Common columns (only add if they exist in the table)
                if "title" in cols_in_table:
                    new_row["title"] = title.strip()

                if "incident_type" in cols_in_table:
                    new_row["incident_type"] = incident_type.strip()

                if "severity" in cols_in_table:
                    new_row["severity"] = severity

                if "status" in cols_in_table:
                    new_row["status"] = status

                # Store date as ISO string (YYYY-MM-DD) if date column exists
                if "date" in cols_in_table:
                    new_row["date"] = str(date_val)

                if "description" in cols_in_table:
                    new_row["description"] = description.strip()

                if "reported_by" in cols_in_table:
                    new_row["reported_by"] = reported_by.strip() if reported_by.strip() else None

                # Basic validation: title usually required
                if "title" in new_row and not new_row["title"]:
                    st.error("Title is required.")
                else:
                    try:
                        columns = ", ".join(new_row.keys())
                        placeholders = ", ".join(["?"] * len(new_row))
                        values = tuple(new_row.values())

                        sql = f"INSERT INTO {INCIDENTS_TABLE} ({columns}) VALUES ({placeholders})"
                        cur = conn.cursor()
                        cur.execute(sql, values)
                        conn.commit()

                        st.success("Incident created successfully.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Failed to create incident: {e}")

        # -------------------------
        # DELETE INCIDENT
        # -------------------------
        with tab_delete:
            st.caption("Select an incident ID and confirm deletion.")

            if incidents_df.empty or "id" not in incidents_df.columns:
                st.info("No incidents available to delete (or missing 'id' column).")
            else:
                incident_ids = incidents_df["id"].dropna().astype(int).tolist()
                incident_ids = sorted(set(incident_ids))

                chosen_id = st.selectbox("Incident ID", incident_ids)

                # Simple preview (optional)
                if "title" in incidents_df.columns:  # show title if available
                    title_preview = incidents_df.loc[incidents_df["id"] == chosen_id, "title"]
                    if not title_preview.empty:
                        st.write("Selected:", title_preview.iloc[0])

                confirm = st.checkbox("I understand this will permanently delete the incident.")

                if st.button("Delete incident", disabled=not confirm):
                    try:
                        cur = conn.cursor()
                        cur.execute(f"DELETE FROM {INCIDENTS_TABLE} WHERE id = ?", (chosen_id,))
                        conn.commit()

                        st.success(f"Incident {chosen_id} deleted.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Failed to delete incident: {e}")


# --------------------------
# Graphs (incidents + tickets)
# --------------------------
g1, g2, g3 = st.columns(3)

with g1:
    st.subheader("Incidents by Severity")
    if not filtered_incidents.empty and "severity" in filtered_incidents.columns:
        st.bar_chart(filtered_incidents["severity"].value_counts())
    else:
        st.info("No severity data available.")

with g2:
    st.subheader("Incidents Over Time")
    if not filtered_incidents.empty and "date" in filtered_incidents.columns and filtered_incidents["date"].notna().any():
        by_day = filtered_incidents.dropna(subset=["date"]).groupby(filtered_incidents["date"].dt.date).size()
        st.line_chart(by_day)
    else:
        st.info("No date data available.")

with g3:
    st.subheader("Ticket Priority (Pie)")
    if not tickets_df.empty and "priority" in tickets_df.columns:
        counts = tickets_df["priority"].value_counts()
        # streamlit doesn't have a built-in pie chart, so use matplotlib quickly
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.pie(counts.values, labels=counts.index, autopct="%1.0f%%")
        st.pyplot(fig)
    else:
        st.info("No ticket priority data available.")

st.divider()


# --------------------------
# Tables (shown from objects -> dict)
# --------------------------
st.subheader("Database Tables")

colA, colB = st.columns(2)

with colA:
    st.markdown("### 🛡 Cyber Incidents (Filtered)")
    if not incident_objects:
        st.info("No incidents found with current filters.")
    else:
        st.dataframe(pd.DataFrame([i.to_dict() for i in incident_objects]), use_container_width=True)

with colB:
    st.markdown("### 🛠 IT Tickets")
    if not ticket_objects:
        st.info("No tickets found in the database.")
    else:
        st.dataframe(pd.DataFrame([t.to_dict() for t in ticket_objects]), use_container_width=True)


# --------------------------
# Logout
# --------------------------
st.divider()

if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "user"
    st.info("You have been logged out.")
    st.switch_page("home.py")  # change to Home.py if needed
