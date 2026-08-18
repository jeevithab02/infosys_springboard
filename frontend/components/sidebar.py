# pyrefly: ignore [missing-import]
import streamlit as st


def render_sidebar():

    user = st.session_state.get("user")

    with st.sidebar:

        st.markdown(
            """
            <div class="brand">
                <div class="brand-icon">⚡</div>
                <div>
                    <h2>EV HEALTH</h2>
                    <p>Station Monitor</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.page_link(
            "app.py",
            label="Dashboard",
            icon="📊",
        )

        st.markdown("##### MONITORING")

        st.page_link(
            "pages/stations.py",
            label="Charging Stations",
            icon="⚡",
        )

        st.page_link(
            "pages/alerts.py",
            label="Alerts",
            icon="🚨",
        )

        st.page_link(
            "pages/failures.py",
            label="Failure History",
            icon="⚠️",
        )

        st.markdown("##### OPERATIONS")

        st.page_link(
            "pages/maintenance.py",
            label="Maintenance",
            icon="🔧",
        )

        st.page_link(
            "pages/sessions.py",
            label="Charging Sessions",
            icon="🔋",
        )

        st.page_link(
            "pages/operators.py",
            label="Operators",
            icon="👥",
        )

        st.markdown("##### ANALYTICS")

        st.page_link(
            "pages/analytics.py",
            label="Station Analytics",
            icon="📈",
        )

        st.markdown("##### AI")

        st.page_link(
            "pages/prediction.py",
            label="Predictive Maintenance",
            icon="🤖",
        )

        st.page_link(
            "pages/feedback.py",
            label="Feedback",
            icon="💬",
        )

        st.divider()

        if user:
            st.caption(f"Signed in as")
            st.write(f"**{user.get('name', 'User')}**")

        if st.button(
            "Logout",
            use_container_width=True,
        ):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
