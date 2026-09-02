# pyrefly: ignore [missing-import]
import streamlit as st
from api import get_api
from style import load_css
from components.sidebar import render_sidebar
from auth import require_login

st.set_page_config(
    page_title="Charging Sessions",
    layout="wide",
)


load_css()
require_login()
if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

render_sidebar()

st.title("Charging Sessions")
st.caption("Monitor historical EV charging activity and energy usage.")

# =============================
# Load Data
# =============================

sessions = get_api("/charging-session/all")
stations = get_api("/charging-stations/all")

if sessions is None:
    st.error(
        "Unable to load charging sessions. " "Make sure the FastAPI backend is running."
    )
    st.stop()

stations = stations or []

# Map station ID -> station name
station_map = {station.get("id"): station.get("station_name") for station in stations}

# =============================
# Summary
# =============================

total_sessions = len(sessions)

total_energy = sum(session.get("energy_consumed", 0) or 0 for session in sessions)

total_cost = sum(session.get("cost", 0) or 0 for session in sessions)

avg_energy = total_energy / total_sessions if total_sessions else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sessions", total_sessions)

with col2:
    st.metric("Energy Consumed", f"{total_energy:.2f} kWh")

with col3:
    st.metric("Total Cost", f"₹{total_cost:.2f}")

with col4:
    st.metric("Avg. Energy / Session", f"{avg_energy:.2f} kWh")

st.divider()

# =============================
# Filters
# =============================

st.subheader("Session History")

filter_col1, filter_col2 = st.columns(2)

station_options = ["All"] + sorted([name for name in station_map.values() if name])

with filter_col1:
    selected_station = st.selectbox(
        "Filter by Station",
        station_options,
    )

with filter_col2:
    vehicle_search = st.text_input(
        "Search Vehicle",
        placeholder="e.g. EV1075",
    )

# =============================
# Apply Filters
# =============================

filtered_sessions = sessions

if selected_station != "All":

    selected_station_id = next(
        (
            station_id
            for station_id, station_name in station_map.items()
            if station_name == selected_station
        ),
        None,
    )

    filtered_sessions = [
        session
        for session in filtered_sessions
        if session.get("station_id") == selected_station_id
    ]

if vehicle_search:

    filtered_sessions = [
        session
        for session in filtered_sessions
        if vehicle_search.lower() in str(session.get("vehicle_id", "")).lower()
    ]

# =============================
# Session Table
# =============================

st.write(f"Showing **{len(filtered_sessions)}** of " f"**{total_sessions}** sessions")

if filtered_sessions:

    table_data = []

    for session in filtered_sessions:

        station_id = session.get("station_id")

        table_data.append(
            {
                "ID": session.get("id"),
                "Station": station_map.get(
                    station_id,
                    f"Station {station_id}",
                ),
                "Vehicle": session.get("vehicle_id"),
                "Start Time": session.get("start_time"),
                "End Time": session.get("end_time"),
                "Energy (kWh)": session.get("energy_consumed"),
                "Cost (₹)": session.get("cost"),
            }
        )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No charging sessions match the selected filters.")
