# pyrefly: ignore [missing-import]
import streamlit as st

from api import get_api
from style import load_css
from auth import require_login
from components.sidebar import render_sidebar
from auth import require_login

st.set_page_config(
    page_title="Maintenance",
    layout="wide",
)


load_css()

require_login()
render_sidebar()

# =============================
# Header
# =============================

st.title(" Maintenance")
st.caption("Track scheduled and completed charging station maintenance.")


# =============================
# Load Data
# =============================

maintenance = get_api("/maintenance/all")
stations = get_api("/charging-stations/all")


if maintenance is None:
    st.error(
        "Unable to load maintenance data. " "Make sure the FastAPI backend is running."
    )
    st.stop()


# =============================
# Summary
# =============================

total_maintenance = len(maintenance)

pending = [item for item in maintenance if item.get("status") == "Pending"]

scheduled = [item for item in maintenance if item.get("status") == "Scheduled"]

completed = [item for item in maintenance if item.get("status") == "Completed"]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Maintenance", total_maintenance)

with col2:
    st.metric("Pending", len(pending))

with col3:
    st.metric("Scheduled", len(scheduled))

with col4:
    st.metric("Completed", len(completed))


st.divider()


# =============================
# Filters
# =============================

st.subheader("Maintenance Schedule")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_status = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Scheduled",
            "Completed",
        ],
    )


with filter_col2:

    station_filter_options = ["All"]

    if stations:
        station_filter_options += [station.get("station_name") for station in stations]

    selected_station = st.selectbox(
        "Charging Station",
        station_filter_options,
    )


# =============================
# Station Lookup
# =============================

station_names = {}

if stations:

    station_names = {
        station.get("id"): station.get("station_name") for station in stations
    }


# =============================
# Apply Filters
# =============================

filtered_maintenance = maintenance


if selected_status != "All":

    filtered_maintenance = [
        item for item in filtered_maintenance if item.get("status") == selected_status
    ]


if selected_station != "All":

    selected_station_id = next(
        (
            station.get("id")
            for station in stations
            if station.get("station_name") == selected_station
        ),
        None,
    )

    filtered_maintenance = [
        item
        for item in filtered_maintenance
        if item.get("charging_station_id") == selected_station_id
    ]


st.write(f"Showing **{len(filtered_maintenance)}** maintenance records")


# =============================
# Maintenance Table
# =============================

table_data = []

for item in filtered_maintenance:

    station_id = item.get("charging_station_id")

    station_name = station_names.get(
        station_id,
        f"Station {station_id}",
    )

    status = item.get("status", "Unknown")

    if status == "Completed":
        display_status = "🟢 Completed"
    elif status == "Scheduled":
        display_status = "🔵 Scheduled"
    else:
        display_status = "🟡 Pending"

    table_data.append(
        {
            "ID": item.get("id"),
            "Station": station_name,
            "Maintenance Date": item.get("maintenance_date", "")[:10],
            "Status": display_status,
        }
    )


if table_data:

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No maintenance records match the selected filters.")
