# pyrefly: ignore [missing-import]
import streamlit as st

from auth import login, signup
from components.sidebar import render_sidebar
from api import get_api
from style import load_css


st.set_page_config(
    page_title="EV Charging Health Monitor",
    layout="wide",
)

load_css()

# -----------------------------
# Session State
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# Hide Streamlit's automatic sidebar on login/signup
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }

        button[data-testid="stBaseButton-headerNoPadding"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

user = st.session_state.user

# =============================
# Dashboard Header
# =============================

st.markdown(
    f"""
    <div class="hero-header">
        <div class="hero-content">
            <div>
                <div class="hero-label">EV INFRASTRUCTURE MONITORING</div>
                <h1>Charging Station Health Monitor</h1>
                <p>Welcome back, {user.get('name', 'User')} · Real-time system overview</p>
            </div>
        </div>
        <div class="system-status">
            <span class="status-dot"></span>
            <div>
                <strong>System Operational</strong>
                <small>All services running</small>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# =============================
# Get Dashboard Data
# =============================

summary = get_api("/dashboard/summary")

if summary is None:

    st.error(
        "Unable to load dashboard data. " "Make sure the FastAPI backend is running."
    )

    st.stop()


# =============================
# Primary Metrics
# =============================

st.markdown("### System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Charging Stations",
        summary.get("total_stations", 0),
    )

with col2:
    st.metric(
        "Active Alerts",
        summary.get("unresolved_alerts", 0),
    )

with col3:
    st.metric(
        "Failure Records",
        summary.get("total_failures", 0),
    )

with col4:
    st.metric(
        "Maintenance",
        summary.get("total_maintenance", 0),
    )


st.write("")


# =============================
# Activity Metrics
# =============================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Charging Sessions",
        summary.get("total_charging_sessions", 0),
    )

with col2:
    st.metric(
        "Operators",
        summary.get("total_operators", 0),
    )

with col3:
    st.metric(
        "AI Predictions",
        summary.get("total_predictions", 0),
    )


st.divider()


# =============================
# Monitoring Summary
# =============================

st.markdown("### Monitoring Summary")

col1, col2 = st.columns(2)

with col1:

    unresolved_alerts = summary.get("unresolved_alerts", 0)

    total_alerts = summary.get("total_alerts", 0)

    st.markdown(
        f"""
    <div class="dashboard-card">
        <div class="card-icon alert-icon">🚨</div>
        <div>
            <h3>Alert Monitoring</h3>
            <p><strong>{unresolved_alerts}</strong> unresolved alerts out of <strong>{total_alerts}</strong> total alerts.</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


with col2:

    pending = summary.get("pending_maintenance", 0)

    total_maintenance = summary.get("total_maintenance", 0)

    st.markdown(
        f"""
    <div class="dashboard-card">
        <div class="card-icon maintenance-icon">🔧</div>
        <div>
            <h3>Maintenance</h3>
            <p><strong>{pending}</strong> pending tasks out of <strong>{total_maintenance}</strong> maintenance records.</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


st.write("")


# =============================
# Quick Access
# =============================

st.markdown("### Quick Access")

q1, q2, q3 = st.columns(3)

with q1:

    if st.button(
        "View Charging Stations",
        use_container_width=True,
    ):
        st.switch_page("pages/stations.py")


with q2:

    if st.button(
        "View Alerts",
        use_container_width=True,
    ):
        st.switch_page("pages/alerts.py")


with q3:

    if st.button(
        "View Maintenance",
        use_container_width=True,
    ):
        st.switch_page("pages/maintenance.py")
