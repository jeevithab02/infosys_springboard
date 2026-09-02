# pyrefly: ignore [missing-import]
from auth import require_login

# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
from api import get_api
from style import load_css
from components.sidebar import render_sidebar
from charts import multi_line_chart


st.set_page_config(
    page_title="Analytics",
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

st.title("Station Analytics")
st.caption("View performance and operational analytics for charging stations.")


# =============================
# Load Stations
# =============================

stations = get_api("charging-stations/all")

if stations is None:
    st.error(
        "Unable to load charging stations. " "Make sure the FastAPI backend is running."
    )
    st.stop()

if not stations:
    st.info("No charging stations available.")
    st.stop()


# =============================
# Station Selection
# =============================

station_options = {
    station.get("station_name"): station.get("id")
    for station in stations
    if station.get("station_name") is not None
}

selected_name = st.selectbox(
    "Select Charging Station",
    list(station_options.keys()),
)

selected_id = station_options[selected_name]


# =============================
# Load Analytics
# =============================

analytics = get_api(f"charging-stations/{selected_id}/analytics")

if analytics is None:
    st.error("Unable to load analytics for this station.")
    st.stop()


st.divider()


# =============================
# Station Overview
# =============================

st.subheader(selected_name)

overview_col1, overview_col2, overview_col3 = st.columns(3)

with overview_col1:
    st.metric(
        "Average Temperature",
        (
            f"{analytics.get('average_temperature', 0):.2f} °C"
            if analytics.get("average_temperature") is not None
            else "N/A"
        ),
    )

with overview_col2:
    st.metric(
        "Average Humidity",
        (
            f"{analytics.get('average_humidity', 0):.2f} %"
            if analytics.get("average_humidity") is not None
            else "N/A"
        ),
    )

with overview_col3:
    st.metric(
        "Average Power",
        f"{analytics.get('average_power_consumption', 0):.2f}",
    )


# =============================
# Telemetry & Battery Health Trend
# =============================

telemetry = get_api("/telemetry/all") or []

station_telemetry = [
    record
    for record in telemetry
    if record.get("charging_station_id") == selected_id
]

if station_telemetry:

    st.write("")

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <h4>Telemetry & Battery Health</h4>
                    <p>Temperature, humidity and power consumption over recorded readings</p>
                </div>
                <span class="chip chip-blue">Monitored</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    reading_numbers = list(range(1, len(station_telemetry) + 1))

    series = {
        "Temperature (°C)": [
            record.get("temperature", 0) for record in station_telemetry
        ],
        "Humidity (%)": [record.get("humidity", 0) for record in station_telemetry],
        "Power Consumption": [
            record.get("power_consumption", 0) for record in station_telemetry
        ],
    }

    fig = multi_line_chart(reading_numbers, series)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("</div>", unsafe_allow_html=True)


# =============================
# Charging Statistics
# =============================

st.divider()

st.subheader("Charging Performance")

charge_col1, charge_col2, charge_col3 = st.columns(3)

with charge_col1:
    st.metric(
        "Charging Sessions",
        analytics.get("total_charging_sessions", 0),
    )

with charge_col2:
    st.metric(
        "Energy Consumed",
        f"{analytics.get('total_energy_consumed', 0):.2f}",
    )

with charge_col3:
    st.metric(
        "Total Charging Cost",
        f"₹{analytics.get('total_charging_cost', 0):,.2f}",
    )


# =============================
# Health & Maintenance
# =============================

st.divider()

st.subheader("Health & Maintenance")

health_col1, health_col2, health_col3, health_col4 = st.columns(4)

with health_col1:
    st.metric(
        "Total Alerts",
        analytics.get("total_alerts", 0),
    )

with health_col2:
    st.metric(
        "Unresolved Alerts",
        analytics.get("unresolved_alerts", 0),
    )

with health_col3:
    st.metric(
        "Total Failures",
        analytics.get("total_failures", 0),
    )

with health_col4:
    st.metric(
        "Unresolved Failures",
        analytics.get("unresolved_failures", 0),
    )


# =============================
# Maintenance
# =============================

st.divider()

maintenance_col1, maintenance_col2 = st.columns(2)

with maintenance_col1:
    st.metric(
        "Maintenance Records",
        analytics.get("total_maintenance", 0),
    )

with maintenance_col2:

    unresolved_failures = analytics.get("unresolved_failures", 0)

    if unresolved_failures > 0:
        st.warning(
            f"{unresolved_failures} unresolved failure(s) "
            "recorded for this station."
        )
    else:
        st.success("No unresolved failures recorded.")


# =============================
# Station Health Summary
# =============================

st.divider()

st.subheader("Health Summary")

if analytics.get("unresolved_failures", 0) > 0:
    st.warning("This station has unresolved failures that may require attention.")
elif analytics.get("unresolved_alerts", 0) > 0:
    st.warning("This station has unresolved alerts that should be reviewed.")
else:
    st.success("This station currently has no unresolved alerts or failures.")
