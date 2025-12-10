import streamlit as st
from database import DatabaseManager

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# ---------- Initialise session state ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"


@st.cache_resource
def get_db():
    return DatabaseManager("DATA/intelligence_platform.db")


db = get_db()

st.title("🔐 Welcome")

# If already logged in, go straight to dashboard (optional)
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()


# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        if not login_username or not login_password:
            st.warning("Please enter both username and password.")
        else:
            ok, role = db.verify_user(login_username, login_password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.session_state.role = role or "user"
                st.success(f"Welcome back, {login_username}!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password.")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            created = db.register_user(new_username, new_password, role="user")
            if created:
                st.success("Account created! You can now log in from the Login tab.")
            else:
                st.error("Username already exists. Choose another one.")
