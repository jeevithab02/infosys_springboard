# pyrefly: ignore [missing-import]
import streamlit as st


def render_sidebar():

    with st.sidebar:

        # =========================
        # Brand
        # =========================

        st.markdown(
            """
            <div class="brand">
                <div class="brand-icon">EV</div>
                <div class="brand-text">
                    <div class="brand-title">EV HEALTH</div>
                    <div class="brand-subtitle">Station Monitor</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='sidebar-divider'></div>",
            unsafe_allow_html=True,
        )

        # =========================
        # Dashboard
        # =========================

        st.page_link(
            "app.py",
            label="Dashboard",
        )

        # =========================
        # Monitoring
        # =========================

        st.markdown(
            "<div class='sidebar-section'>MONITORING</div>",
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/stations.py",
            label="Charging Stations",
        )

        st.page_link(
            "pages/alerts.py",
            label="Alerts",
        )

        st.page_link(
            "pages/failures.py",
            label="Failure History",
        )

        # =========================
        # Operations
        # =========================

        st.markdown(
            "<div class='sidebar-section'>OPERATIONS</div>",
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/maintenance.py",
            label="Maintenance",
        )

        st.page_link(
            "pages/sessions.py",
            label="Charging Sessions",
        )

        st.page_link(
            "pages/operators.py",
            label="Operators",
        )

        # =========================
        # Analytics
        # =========================

        st.markdown(
            "<div class='sidebar-section'>ANALYTICS</div>",
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/analytics.py",
            label="Station Analytics",
        )

        # =========================
        # AI
        # =========================

        st.markdown(
            "<div class='sidebar-section'>AI</div>",
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/prediction.py",
            label="Predictive Maintenance",
        )

        # =========================
        # Feedback
        # =========================

        st.markdown(
            "<div class='sidebar-section'>FEEDBACK</div>",
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/feedback.py",
            label="Feedback",
        )

        # =========================
        # Signed-in User
        # =========================

        st.markdown(
            "<div class='sidebar-bottom'></div>",
            unsafe_allow_html=True,
        )

        user = st.session_state.get("user", {})
        name = user.get("name", "User")

        st.markdown(
            f"""
            <div class="signed-in">
                <div class="signed-label">SIGNED IN AS</div>
                <div class="signed-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================
        # Logout
        # =========================

        if st.button(
            "Logout",
            key="sidebar_logout",
            use_container_width=True,
        ):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.auth_page = "login"

            st.switch_page("app.py")
