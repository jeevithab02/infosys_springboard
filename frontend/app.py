import streamlit as st

from auth import login, signup
from components.sidebar import render_sidebar
from api import get_api


st.set_page_config(
    page_title="EV Charging Health Monitor",
    page_icon="⚡",
    layout="wide",
)


# -----------------------------
# Session State
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


# -----------------------------
# Authentication
# -----------------------------

if not st.session_state.logged_in:

    if st.session_state.auth_page == "signup":
        signup()
    else:
        login()

    st.stop()


# -----------------------------
# Logged-in Application
# -----------------------------

render_sidebar()

st.title("⚡ EV Charging Station Health Monitor")

user = st.session_state.user

st.caption(f"Welcome back, {user.get('name', 'User')} • System Overview")

summary = get_api("/dashboard/summary")

if summary is None:
    st.error(
        "Unable to load dashboard data. " "Make sure the FastAPI backend is running."
    )
    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Charging Stations", summary.get("total_stations", 0))

with col2:
    st.metric("Active Alerts", summary.get("unresolved_alerts", 0))

with col3:
    st.metric("Failure Records", summary.get("total_failures", 0))

with col4:
    st.metric("Maintenance", summary.get("total_maintenance", 0))


st.divider()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Charging Sessions", summary.get("total_charging_sessions", 0))

with col2:
    st.metric("Operators", summary.get("total_operators", 0))

with col3:
    st.metric("Predictions", summary.get("total_predictions", 0))
