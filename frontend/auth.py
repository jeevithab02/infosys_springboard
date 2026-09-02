# pyrefly: ignore [missing-import]
import streamlit as st

# pyrefly: ignore [import-error]
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def login():

    st.markdown(
        """
        <div class="auth-header">
            <h1>EV Health Monitor</h1>
            <p>EV Charging Station Health Monitoring</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Center the login form
    left, center, right = st.columns([1, 1.5, 1])

    with center:

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )

            role = st.radio(
                "Login as",
                options=["User", "Admin"],
                horizontal=True,
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

            if submitted:

                if not email or not password:
                    st.error("Please enter both email and password.")
                    return

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/login",
                        json={
                            "email": email,
                            "password": password,
                        },
                        timeout=5,
                    )

                    if response.status_code == 200:

                        user = response.json()
                        user["role"] = role

                        st.session_state.logged_in = True
                        st.session_state.user = user

                        st.rerun()

                    elif response.status_code == 401:

                        st.error("Invalid email or password.")

                    else:

                        st.error(
                            f"Login failed. Status code: " f"{response.status_code}"
                        )

                except requests.exceptions.RequestException:

                    st.error(
                        "Unable to connect to the backend. "
                        "Make sure FastAPI is running."
                    )

        st.write("")

        if st.button(
            "Don't have an account?  Sign Up",
            use_container_width=True,
        ):

            st.session_state.auth_page = "signup"
            st.rerun()


def signup():

    st.markdown(
        """
        <div class="auth-header">
            <h1>Create Account</h1>
            <p>EV Charging Station Health Monitoring</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Center the signup form
    left, center, right = st.columns([1, 1.5, 1])

    with center:

        with st.form("signup_form"):

            name = st.text_input(
                "Name",
                placeholder="Enter your name",
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

            if submitted:

                if not name or not email or not password:
                    st.error("Please fill in all required fields.")
                    return

                if password != confirm_password:
                    st.error("Passwords do not match.")
                    return

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/users",
                        json={
                            "name": name,
                            "email": email,
                            "password": password,
                        },
                        timeout=5,
                    )

                    if response.status_code in (200, 201):

                        st.success("Account created successfully!")

                        st.session_state.auth_page = "login"
                        st.rerun()

                    elif response.status_code == 400:

                        st.error("An account with this email already exists.")

                    else:

                        try:

                            detail = response.json().get(
                                "detail",
                                "Unable to create account.",
                            )

                        except Exception:

                            detail = "Unable to create account."

                        st.error(detail)

                except requests.exceptions.RequestException:

                    st.error(
                        "Unable to connect to the backend. "
                        "Make sure FastAPI is running."
                    )

        st.write("")

        if st.button(
            "Already have an account?  Login",
            use_container_width=True,
        ):

            st.session_state.auth_page = "login"
            st.rerun()


def require_login():

    if not st.session_state.get("logged_in", False):

        st.session_state.auth_page = "login"

        st.switch_page("app.py")
