# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
from api import get_api
from style import load_css
from components.sidebar import render_sidebar
from auth import require_login

st.set_page_config(
    page_title="Operators",
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

st.title("Operators")
st.caption("Manage and monitor charging station operators.")


# =============================
# Load Operators
# =============================

operators = get_api("/operators/all")

if operators is None:
    st.error(
        "Unable to load operator data. " "Make sure the FastAPI backend is running."
    )
    st.stop()


# =============================
# Summary
# =============================

total_operators = len(operators)

shifts = {operator.get("shift") for operator in operators if operator.get("shift")}

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Operators", total_operators)

with col2:
    st.metric("Active Shifts", len(shifts))


st.divider()


# =============================
# Operator Directory
# =============================

st.subheader("Operator Directory")

if operators:

    table_data = [
        {
            "ID": operator.get("id"),
            "Name": operator.get("name"),
            "Email": operator.get("email"),
            "Phone": operator.get("phone"),
            "Shift": operator.get("shift"),
        }
        for operator in operators
    ]

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No operators have been registered yet.")
