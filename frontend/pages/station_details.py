# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
from api import get_api
from style import load_css
from auth import require_login
from components.sidebar import render_sidebar
from auth import require_login
from charts import multi_line_chart

st.set_page_config(
    page_title="Station Details",
    layout="wide",
)
load_css()
require_login()
if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

render_sidebar()

# =============================
# Load Data
# =============================

stations = get_api("/charging-stations/all")
telemetry = get_api("/telemetry/all")
alerts = get_api("/alerts/all")


if stations is None:
    st.error("Unable to load charging station data.")
    st.stop()


# =============================
# Station Selection
# =============================

st.title("Station Details")
st.caption("View station information and latest telemetry.")

station_options = {station["station_name"]: station["id"] for station in stations}

default_station = st.session_state.get(
    "selected_station_name", list(station_options.keys())[0]
)

selected_name = st.selectbox(
    "Select Charging Station",
    list(station_options.keys()),
    index=list(station_options.keys()).index(default_station),
)
selected_id = station_options[selected_name]

selected_station = next(station for station in stations if station["id"] == selected_id)


# =============================
# Station Information
# =============================

st.divider()

st.subheader(selected_station["station_name"])

info1, info2, info3 = st.columns(3)

with info1:
    st.metric("Station ID", selected_station["id"])

with info2:
    st.metric("Location", selected_station["location"])

with info3:
    st.metric("Charger Type", selected_station["charger_type"])


# =============================
# Latest Telemetry
# =============================

st.divider()

st.subheader("Latest Telemetry")

station_telemetry = [
    record
    for record in (telemetry or [])
    if record.get("charging_station_id") == selected_id
]

if station_telemetry:

    latest = station_telemetry[-1]

    temp_col, humidity_col, power_col = st.columns(3)

    with temp_col:
        st.metric("Temperature", f"{latest.get('temperature', 0):.2f} °C")

    with humidity_col:
        st.metric("Humidity", f"{latest.get('humidity', 0):.2f} %")

    with power_col:
        st.metric("Power Consumption", f"{latest.get('power_consumption', 0):.2f}")
        # =============================
    # Telemetry History
    # =============================

    st.markdown("#### Telemetry History")

    reading_numbers = list(range(1, len(station_telemetry) + 1))

    telemetry_chart_data = {
        "Temperature (°C)": [
            record.get("temperature", 0) for record in station_telemetry
        ],
        "Humidity (%)": [record.get("humidity", 0) for record in station_telemetry],
        "Power Consumption": [
            record.get("power_consumption", 0) for record in station_telemetry
        ],
    }

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    fig = multi_line_chart(reading_numbers, telemetry_chart_data)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("No telemetry records available for this station.")


# =============================
# Station Alerts
# =============================

st.divider()

st.subheader("Station Alerts")

station_alerts = [
    alert for alert in (alerts or []) if alert.get("charging_station_id") == selected_id
]

if station_alerts:

    for alert in station_alerts[-5:][::-1]:

        resolved = alert.get("is_resolved", False)

        if resolved:
            status = "<span class='dot dot-success'></span>Resolved"
        else:
            status = "<span class='dot dot-danger'></span>Unresolved"

        st.markdown(
            f"""
            **{alert.get('alert_type', 'Alert')}**

            {alert.get('description', 'No description')}

            <strong>{status}</strong>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

else:
    st.success("No alerts recorded for this station.")
