# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
from api import get_api, post_api

# pyrefly: ignore [import-error]
from style import load_css
from components.sidebar import render_sidebar
from auth import require_login

st.set_page_config(
    page_title="Feedback",
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

st.title(" User Feedback")

st.caption(
    "Share feedback about charging stations and help improve "
    "the EV charging experience."
)


# =============================
# Load Data
# =============================

stations = get_api("/charging-stations/all")
feedback_list = get_api("/feedback/all")


if stations is None:
    st.error(
        "Unable to load charging station data. "
        "Make sure the FastAPI backend is running."
    )
    st.stop()


# =============================
# Submit Feedback
# =============================

st.subheader("Submit Feedback")

with st.form("feedback_form"):

    col1, col2 = st.columns(2)

    with col1:

        station_options = {
            station["station_name"]: station["id"] for station in stations
        }

        selected_station = st.selectbox(
            "Charging Station",
            list(station_options.keys()),
        )

        rating = st.select_slider(
            "Rating",
            options=[1, 2, 3, 4, 5],
            value=5,
        )

    with col2:

        comments = st.text_area(
            "Comments",
            placeholder="Enter your feedback...",
            height=120,
        )

    submitted = st.form_submit_button(
        "Submit Feedback",
        type="primary",
        use_container_width=True,
    )


# =============================
# Handle Submission
# =============================

if submitted:

    user = st.session_state.get("user")

    if not user:
        st.error("Please log in before submitting feedback.")
        st.stop()

    user_id = user.get("id")

    if user_id is None:
        st.error("Unable to identify the logged-in user.")
        st.stop()

    feedback_data = {
        "user_id": user_id,
        "charging_station_id": station_options[selected_station],
        "comments": comments if comments else None,
        "rating": rating,
    }

    result = post_api(
        "/feedback",
        feedback_data,
    )

    if result is not None:

        st.success("Feedback submitted successfully!")

        st.rerun()

    else:

        st.error(
            "Unable to submit feedback. " "Please check that the backend is running."
        )


# =============================
# Feedback History
# =============================

st.divider()

st.subheader("Recent Feedback")


if feedback_list:

    # -------------------------
    # Summary
    # -------------------------

    total_feedback = len(feedback_list)

    average_rating = (
        sum(feedback.get("rating", 0) for feedback in feedback_list) / total_feedback
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Feedback",
            total_feedback,
        )

    with col2:
        st.metric(
            "Average Rating",
            f"{average_rating:.1f} / 5",
        )

    with col3:
        five_star = sum(1 for feedback in feedback_list if feedback.get("rating") == 5)

        st.metric(
            "5-Star Reviews",
            five_star,
        )

    st.write("")

    # -------------------------
    # Feedback Cards
    # -------------------------

    station_lookup = {station["id"]: station["station_name"] for station in stations}

    for feedback in reversed(feedback_list):

        station_id = feedback.get("charging_station_id")

        station_name = station_lookup.get(
            station_id,
            f"Station {station_id}",
        )

        rating_value = feedback.get("rating", 0)

        stars = "⭐" * rating_value

        comments_text = feedback.get("comments")

        if not comments_text:
            comments_text = "No comments provided."

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(f"**{station_name}**")

                st.caption(f"User ID: {feedback.get('user_id')}")

                st.write(comments_text)

            with col2:

                st.markdown(f"### {stars}")

else:

    st.info("No feedback has been submitted yet.")
