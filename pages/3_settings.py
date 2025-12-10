import streamlit as st
from database import DatabaseManager


@st.cache_resource
def get_database():
    return DatabaseManager("DATA/intelligence_platform.db")


# DEBUG
st.write("⚙️ Settings page loaded")


# ---------- AUTH GUARD ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must log in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

db = get_database()

st.title("⚙️ Settings & Session Info")

st.subheader("Current session state")
st.json(
    {
        "logged_in": st.session_state.logged_in,
        "username": st.session_state.username,
        "role": st.session_state.role,
    }
)

st.subheader("Actions")

if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.success("Logged out.")
    st.switch_page("Home.py")
