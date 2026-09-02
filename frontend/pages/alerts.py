# pyrefly: ignore [missing-import]
import streamlit as st

from api import get_api
from style import load_css
from auth import require_login
from components.sidebar import render_sidebar
from auth import require_login
from charts import donut_chart

st.set_page_config(
    page_title="Alerts",
    layout="wide",
)

load_css()

require_login()

if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")
render_sidebar()

# =============================
# Header
# =============================

st.title("Alerts")
st.caption("Monitor and review charging station alerts.")


# =============================
# Load Data
# =============================

alerts = get_api("/alerts/all")
stations = get_api("/charging-stations/all")


if alerts is None:
    st.error("Unable to load alerts. " "Make sure the FastAPI backend is running.")
    st.stop()


# =============================
# Summary
# =============================

total_alerts = len(alerts)

unresolved_alerts = [alert for alert in alerts if not alert.get("is_resolved", False)]

resolved_alerts = [alert for alert in alerts if alert.get("is_resolved", False)]


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Alerts", total_alerts)

with col2:
    st.metric("Unresolved", len(unresolved_alerts))

with col3:
    st.metric("Resolved", len(resolved_alerts))


st.divider()


# =============================
# Alert Distribution
# =============================

if total_alerts:

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

    fig = donut_chart(
        ["Resolved", "Unresolved"],
        [len(resolved_alerts), len(unresolved_alerts)],
        colors=["#20c563", "#e5484d"],
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")


# =============================
# Filters
# =============================

st.subheader("Alert Monitoring")

alert_types = sorted(
    set(alert.get("alert_type") for alert in alerts if alert.get("alert_type"))
)

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_type = st.selectbox("Alert Type", ["All"] + alert_types)

with filter_col2:

    selected_status = st.selectbox("Status", ["All", "Unresolved", "Resolved"])


# =============================
# Apply Filters
# =============================

filtered_alerts = alerts


if selected_type != "All":

    filtered_alerts = [
        alert for alert in filtered_alerts if alert.get("alert_type") == selected_type
    ]


if selected_status == "Unresolved":

    filtered_alerts = [
        alert for alert in filtered_alerts if not alert.get("is_resolved", False)
    ]

elif selected_status == "Resolved":

    filtered_alerts = [
        alert for alert in filtered_alerts if alert.get("is_resolved", False)
    ]


st.write(f"Showing **{len(filtered_alerts)}** alerts")


# =============================
# Station Lookup
# =============================

station_names = {}

if stations:

    station_names = {
        station.get("id"): station.get("station_name") for station in stations
    }


# =============================
# Alert List
# =============================

for alert in filtered_alerts:

    station_id = alert.get("charging_station_id")

    station_name = station_names.get(station_id, f"Station {station_id}")

    is_resolved = alert.get("is_resolved", False)

    if is_resolved:

        status_text = "<span class='dot dot-success'></span>Resolved"

    else:

        status_text = "<span class='dot dot-danger'></span>Unresolved"

    with st.container(border=True):

        alert_col1, alert_col2 = st.columns([4, 1])

        with alert_col1:

            st.markdown(f"### {alert.get('alert_type', 'Alert')}")

            st.write(alert.get("description", "No description available."))

            st.caption(f"{station_name} · " f"Station ID: {station_id}")

        with alert_col2:

            st.markdown(
                f"<strong>{status_text}</strong>",
                unsafe_allow_html=True,
            )

            timestamp = alert.get("timestamp", "")

            if timestamp:

                st.caption(timestamp[:19])
