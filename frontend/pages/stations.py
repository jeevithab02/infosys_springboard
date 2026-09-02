# pyrefly: ignore [missing-import]
import streamlit as st
from api import get_api
from style import load_css
from components.sidebar import render_sidebar
from auth import require_login

st.set_page_config(
    page_title="Charging Stations",
    layout="wide",
)

load_css()
require_login()
if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

render_sidebar()

st.title(" Charging Stations")
st.caption("Monitor and view all registered EV charging stations.")

# Get stations from backend
stations = get_api("/charging-stations/all")

if stations is None:
    st.error(
        "Unable to load charging stations. " "Make sure the FastAPI backend is running."
    )
    st.stop()

# =============================
# Summary
# =============================

total_stations = len(stations)

charger_types = set(station.get("charger_type") for station in stations)

locations = set(station.get("location") for station in stations)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Stations", total_stations)

with col2:
    st.metric("Charger Types", len(charger_types))

with col3:
    st.metric("Locations", len(locations))

st.divider()

# =============================
# Filters
# =============================

st.subheader("Station Directory")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_location = st.selectbox("Filter by Location", ["All"] + sorted(locations))

with filter_col2:

    selected_charger = st.selectbox(
        "Filter by Charger Type", ["All"] + sorted(charger_types)
    )


# =============================
# Apply Filters
# =============================

filtered_stations = stations

if selected_location != "All":
    filtered_stations = [
        station
        for station in filtered_stations
        if station.get("location") == selected_location
    ]

if selected_charger != "All":
    filtered_stations = [
        station
        for station in filtered_stations
        if station.get("charger_type") == selected_charger
    ]


# =============================
# Station Table
# =============================

st.write(f"Showing **{len(filtered_stations)}** stations")

if filtered_stations:

    table_data = [
        {
            "ID": station.get("id"),
            "Station": station.get("station_name"),
            "Charger Type": station.get("charger_type"),
            "Location": station.get("location"),
        }
        for station in filtered_stations
    ]

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )

# =============================
# Station Details
# =============================

st.divider()

st.subheader("View Station Details")

station_names = [station.get("station_name") for station in filtered_stations]

if station_names:

    selected_station = st.selectbox(
        "Select a station",
        station_names,
        key="station_details_select",
    )

    if st.button("View Station Details", use_container_width=False):

        st.session_state.selected_station_name = selected_station

        st.switch_page("pages/station_details.py")

else:

    st.info("No charging stations match the selected filters.")
