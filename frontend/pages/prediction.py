# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
from api import get_api, post_api
from style import load_css
from components.sidebar import render_sidebar
from auth import require_login


st.set_page_config(
    page_title="Predictive Maintenance",
    layout="wide",
)

load_css()

require_login()

if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

render_sidebar()

# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="page-header">
        <div>
            <div class="eyebrow">AI • PREDICTIVE MAINTENANCE</div>
            <h1>Health Prediction</h1>
            <p>
                Analyze charging station sensor readings and identify
                potential health risks before failures occur.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Load Data
# =========================================================

stations = get_api("/charging-stations/all")
predictions = get_api("/prediction/all")


if stations is None:
    st.error(
        "Unable to load charging station data. "
        "Make sure the FastAPI backend is running."
    )
    st.stop()


# =========================================================
# Prediction Statistics
# =========================================================

total_predictions = len(predictions) if predictions else 0

healthy_predictions = 0
failure_predictions = 0

if predictions:
    for prediction in predictions:
        result = str(prediction.get("prediction", "")).lower()

        if "healthy" in result:
            healthy_predictions += 1
        else:
            failure_predictions += 1


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Predictions",
        total_predictions,
    )

with col2:
    st.metric(
        "Healthy Results",
        healthy_predictions,
    )

with col3:
    st.metric(
        "Risk / Failure Results",
        failure_predictions,
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# Prediction Input Card
# =========================================================

st.markdown(
    """
    <div class="section-title">
        <h2>Run Health Prediction</h2>
        <p>Enter the latest sensor readings for a charging station.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


station_options = {station["station_name"]: station["id"] for station in stations}


col1, col2 = st.columns(2)

with col1:

    selected_station = st.selectbox(
        "Charging Station",
        list(station_options.keys()),
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-50.0,
        max_value=150.0,
        value=30.0,
        step=0.1,
    )

with col2:

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.1,
    )

    power_consumption = st.number_input(
        "Power Consumption",
        min_value=0.0,
        value=10.0,
        step=0.1,
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# Run Prediction
# =========================================================

if st.button(
    "  Run Health Prediction",
    type="primary",
    use_container_width=True,
):

    prediction_data = {
        "charging_station_id": station_options[selected_station],
        "temperature": temperature,
        "humidity": humidity,
        "power_consumption": power_consumption,
    }

    result = post_api(
        "/predict",
        prediction_data,
    )

    if result is None:

        st.error(
            "Unable to generate prediction. " "Make sure the prediction API is running."
        )

    else:

        prediction_result = result.get(
            "prediction",
            "Unknown",
        )

        st.session_state.last_prediction = prediction_result
        st.session_state.last_prediction_station = selected_station
        st.session_state.last_prediction_temperature = temperature
        st.session_state.last_prediction_humidity = humidity
        st.session_state.last_prediction_power = power_consumption

        st.rerun()


# =========================================================
# Prediction Result
# =========================================================

if "last_prediction" in st.session_state:

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            <h2>Latest Prediction</h2>
            <p>AI assessment based on the submitted sensor readings.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.last_prediction
    station_name = st.session_state.last_prediction_station

    temperature = st.session_state.get(
        "last_prediction_temperature",
        0,
    )

    humidity = st.session_state.get(
        "last_prediction_humidity",
        0,
    )

    power = st.session_state.get(
        "last_prediction_power",
        0,
    )

    result_text = str(result)

    # -----------------------------------------------------
    # Result status
    # -----------------------------------------------------

    if "healthy" in result_text.lower():

        st.success(f"🟢 **Charging Station Healthy**  \n" f"{result_text}")

    else:

        st.error(f"🔴 **Potential Failure Detected**  \n" f"{result_text}")

    # -----------------------------------------------------
    # Prediction details
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Station",
            station_name,
        )

    with col2:
        st.metric(
            "Temperature",
            f"{temperature:.1f} °C",
        )

    with col3:
        st.metric(
            "Humidity",
            f"{humidity:.1f} %",
        )

    with col4:
        st.metric(
            "Power Consumption",
            f"{power:.1f}",
        )


# =========================================================
# Prediction History
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-title">
        <h2>Prediction History</h2>
        <p>Previously recorded charging station health predictions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


if predictions:

    table_data = []

    for prediction in predictions:

        result = prediction.get(
            "prediction",
            "Unknown",
        )

        table_data.append(
            {
                "ID": prediction.get("id"),
                "Station": prediction.get("charging_station_id"),
                "Temperature": prediction.get("temperature"),
                "Humidity": prediction.get("humidity"),
                "Power Consumption": prediction.get("power_consumption"),
                "Prediction": result,
            }
        )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No saved predictions are available yet.")
