# pyrefly: ignore [missing-import]
import streamlit as st

from api import get_api
from style import load_css
from auth import require_login
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Failure History",
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

st.title("Failure History")
st.caption("Track previous charging station failures and their resolution status.")


# =============================
# Load Data
# =============================

failures = get_api("/failure-history/all")
stations = get_api("/charging-stations/all")


if failures is None:
    st.error(
        "Unable to load failure history. " "Make sure the FastAPI backend is running."
    )
    st.stop()


# =============================
# Summary
# =============================

total_failures = len(failures)

unresolved_failures = [
    failure for failure in failures if failure.get("resolved") == "No"
]

resolved_failures = [
    failure for failure in failures if failure.get("resolved") == "Yes"
]


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Failures", total_failures)

with col2:
    st.metric("Unresolved", len(unresolved_failures))

with col3:
    st.metric("Resolved", len(resolved_failures))


st.divider()


# =============================
# Filters
# =============================

st.subheader("Failure Monitoring")

failure_types = sorted(
    set(
        failure.get("failure_type")
        for failure in failures
        if failure.get("failure_type")
    )
)

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_type = st.selectbox("Failure Type", ["All"] + failure_types)

with filter_col2:

    selected_status = st.selectbox("Status", ["All", "Unresolved", "Resolved"])


# =============================
# Apply Filters
# =============================

filtered_failures = failures


if selected_type != "All":

    filtered_failures = [
        failure
        for failure in filtered_failures
        if failure.get("failure_type") == selected_type
    ]


if selected_status == "Unresolved":

    filtered_failures = [
        failure for failure in filtered_failures if failure.get("resolved") == "No"
    ]

elif selected_status == "Resolved":

    filtered_failures = [
        failure for failure in filtered_failures if failure.get("resolved") == "Yes"
    ]


st.write(f"Showing **{len(filtered_failures)}** failure records")


# =============================
# Station Lookup
# =============================

station_names = {}

if stations:

    station_names = {
        station.get("id"): station.get("station_name") for station in stations
    }


# =============================
# Failure Records
# =============================

for failure in filtered_failures:

    station_id = failure.get("charging_station_id")

    station_name = station_names.get(station_id, f"Station {station_id}")

    resolved = failure.get("resolved")

    if resolved == "Yes":
        status_text = "🟢 Resolved"
    else:
        status_text = "🔴 Unresolved"

    with st.container(border=True):

        failure_col1, failure_col2 = st.columns([4, 1])

        with failure_col1:

            st.markdown(f"### {failure.get('failure_type', 'Failure')}")

            st.write(failure.get("description", "No description available."))

            st.caption(f"{station_name} · " f"Station ID: {station_id}")

        with failure_col2:

            st.markdown(f"**{status_text}**")

            failure_date = failure.get("failure_date", "")

            if failure_date:

                st.caption(failure_date[:10])
