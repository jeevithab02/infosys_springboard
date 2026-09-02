# pyrefly: ignore [missing-import]
import streamlit as st

from auth import login, signup
from components.sidebar import render_sidebar
from api import get_api
from style import load_css
from charts import area_line_chart, donut_chart


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
        <div class="card-icon alert-icon"><span class="dot dot-danger"></span></div>
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
        <div class="card-icon maintenance-icon"><span class="dot dot-info"></span></div>
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
# Charts
# =============================

st.markdown("### Live Monitoring")

chart_col1, chart_col2 = st.columns([2, 1])

telemetry = get_api("/telemetry/all") or []

with chart_col1:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <h4>Telemetry Trend</h4>
                    <p>Recent temperature readings from the monitoring system</p>
                </div>
                <span class="chip chip-green">Live Data</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    if telemetry:

        recent = telemetry[-30:]

        readings = list(range(1, len(recent) + 1))
        temperatures = [record.get("temperature", 0) for record in recent]

        fig = area_line_chart(
            readings,
            temperatures,
            name="Temperature (°C)",
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    else:

        st.info("No telemetry records available yet.")

    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <h4>Alert Distribution</h4>
                    <p>Resolved vs unresolved alerts</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    total_alerts = summary.get("total_alerts", 0)
    unresolved_alerts = summary.get("unresolved_alerts", 0)
    resolved_alerts = max(total_alerts - unresolved_alerts, 0)

    if total_alerts:

        fig = donut_chart(
            ["Resolved", "Unresolved"],
            [resolved_alerts, unresolved_alerts],
            colors=["#20c563", "#e5484d"],
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    else:

        st.info("No alerts recorded yet.")

    st.markdown("</div>", unsafe_allow_html=True)


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
