import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* =========================================================
           GLOBAL
        ========================================================= */

        :root {
            --bg: #f5f8f7;
            --surface: #ffffff;
            --surface-soft: #f8faf9;
            --border: #dce5e2;

            --text: #102532;
            --text-dark: #0b1f2a;
            --text-muted: #5d7685;

            --green: #20c563;
            --green-dark: #16a653;
            --green-soft: #eaf8ef;

            --blue-soft: #eef5ff;
            --orange-soft: #fff6e9;
            --yellow-soft: #fffbe5;

            --shadow: 0 8px 25px rgba(16, 37, 50, 0.06);
            --shadow-hover: 0 12px 30px rgba(16, 37, 50, 0.09);

            --radius: 18px;
        }


        /* =========================================================
           APP BACKGROUND
        ========================================================= */

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .main {
            background: var(--bg);
        }

        .block-container {
            max-width: 1500px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            padding-left: 3.5rem;
            padding-right: 3.5rem;
        }


        /* =========================================================
           REMOVE DEFAULT STREAMLIT HEADER
        ========================================================= */

        header[data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.96);
            border-bottom: 1px solid #edf1ef;
        }

        [data-testid="stHeaderActionElements"] {
            display: none;
        }

        button[data-testid="stBaseButton-headerNoPadding"] {
            display: none;
        }


        /* =========================================================
           TYPOGRAPHY
        ========================================================= */

        html,
        body,
        [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Helvetica,
                Arial,
                sans-serif;
        }

        h1,
        h2,
        h3,
        h4 {
            color: var(--text-dark) !important;
            font-weight: 700 !important;
            letter-spacing: -0.4px;
        }

        h1 {
            font-size: 42px !important;
            line-height: 1.15 !important;
        }

        h2 {
            font-size: 30px !important;
        }

        h3 {
            font-size: 24px !important;
        }

        p,
        label,
        .stMarkdown {
            color: var(--text-muted);
        }

        .stCaption {
            color: var(--text-muted) !important;
        }


        /* =========================================================
           SIDEBAR
        ========================================================= */

        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
            padding-left: 1.4rem;
            padding-right: 1.4rem;
        }

        section[data-testid="stSidebar"] * {
            color: var(--text);
        }

        /* Hide Streamlit's automatic multipage navigation so only our
           custom nav (rendered below) is visible in the sidebar. */

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Sidebar brand area (matches components/sidebar.py markup) */

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;

            padding: 0.75rem 0 1.25rem 0;
        }

        .brand-icon {
            width: 46px;
            height: 46px;
            min-width: 46px;
            border-radius: 13px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: var(--green);
            color: white !important;

            font-size: 15px;
            font-weight: 800;

            box-shadow: 0 8px 18px rgba(32, 197, 99, 0.18);
        }

        .brand-text {
            min-width: 0;
        }

        .brand-title {
            color: var(--text-dark) !important;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 0.3px;
            line-height: 1.2;
        }

        .brand-subtitle {
            color: var(--text-muted) !important;
            font-size: 13px;
            margin-top: 2px;
        }

        .sidebar-divider {
            height: 1px;
            width: 100%;

            margin: 0 0 0.9rem 0;

            background: var(--border);
        }

        .sidebar-section {
            margin: 1.3rem 0 0.5rem 2px;

            color: #90a4b0 !important;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 1.4px;
            text-transform: uppercase;
        }

        .sidebar-bottom {
            margin-top: 1.6rem;

            border-top: 1px solid var(--border);
        }

        .signed-in {
            padding: 1rem 0 0.6rem 2px;
        }

        .signed-label {
            color: #90a4b0 !important;

            font-size: 10px;
            font-weight: 800;

            letter-spacing: 1.2px;
        }

        .signed-name {
            margin-top: 4px;

            color: var(--text-dark) !important;
            font-size: 15px;
            font-weight: 700;
        }

        .signed-role {
            margin-top: 3px;

            display: inline-flex;

            padding: 2px 10px;

            background: var(--green-soft);
            color: var(--green-dark) !important;

            border-radius: 20px;

            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        /* Nav links */

        section[data-testid="stSidebar"] [data-testid="stPageLink"] {
            border-radius: 12px;
            margin-bottom: 2px;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: 14.5px !important;
            font-weight: 500 !important;
            color: var(--text) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
            background: var(--surface-soft);
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] {
            background: var(--blue-soft);
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] p {
            color: var(--text-dark) !important;
            font-weight: 700 !important;
        }


        /* =========================================================
           HERO / DASHBOARD HEADER
        ========================================================= */

        .hero-header {
            width: 100%;
            box-sizing: border-box;

            display: flex;
            align-items: flex-start;
            justify-content: space-between;

            gap: 30px;

            margin-bottom: 2.2rem;
            padding: 0;

            background: transparent;
            border: none;
            box-shadow: none;
        }

        .hero-content {
            display: flex;
            align-items: center;
            gap: 18px;
        }

        .hero-content > div {
            min-width: 0;
        }

        .hero-label {
            margin-bottom: 8px;

            color: #658092;
            font-size: 11px;
            font-weight: 800;

            letter-spacing: 2.2px;
            text-transform: uppercase;
        }

        .hero-header h1 {
            margin: 0 !important;

            color: var(--text-dark) !important;

            font-size: 42px !important;
            font-weight: 750 !important;
            line-height: 1.15 !important;
        }

        .hero-header p {
            margin-top: 12px;
            margin-bottom: 0;

            color: var(--text-muted);
            font-size: 17px;
        }


        /* System status */

        .system-status {
            display: flex;
            align-items: center;
            gap: 12px;

            min-width: 190px;

            padding: 15px 18px;

            background: white;

            border: 1px solid var(--border);
            border-radius: 16px;

            box-shadow: var(--shadow);
        }

        .system-status strong {
            display: block;

            color: var(--text-dark);
            font-size: 14px;
            font-weight: 750;
        }

        .system-status small {
            display: block;

            margin-top: 4px;

            color: var(--text-muted);
            font-size: 12px;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            min-width: 12px;

            border-radius: 50%;

            background: var(--green);

            box-shadow:
                0 0 0 6px rgba(32, 197, 99, 0.12);
        }


        /* =========================================================
           SECTION HEADINGS
        ========================================================= */

        .section-title {
            margin-top: 2rem;
            margin-bottom: 1.3rem;

            color: var(--text-dark);

            font-size: 25px;
            font-weight: 750;
        }

        .section-subtitle {
            margin-top: -8px;
            margin-bottom: 24px;

            color: var(--text-muted);
            font-size: 16px;
        }

        .stMarkdown h3 {
            margin-top: 1.5rem !important;
            margin-bottom: 1.2rem !important;
        }


        /* =========================================================
           METRIC CARDS
        ========================================================= */

        [data-testid="stMetric"] {
            min-height: 135px;

            padding: 25px 28px;

            background: var(--surface);

            border: 1px solid var(--border);
            border-radius: var(--radius);

            box-shadow: var(--shadow);

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;

            font-size: 15px !important;
            font-weight: 500 !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-dark) !important;

            font-size: 36px !important;
            font-weight: 800 !important;

            line-height: 1.1 !important;
        }

        [data-testid="stMetricDelta"] {
            color: var(--green-dark) !important;
        }


        /* =========================================================
           GENERIC DASHBOARD CARDS
        ========================================================= */

        .dashboard-card {
            display: flex;
            align-items: center;

            width: 100%;
            min-height: 105px;

            box-sizing: border-box;

            padding: 25px 28px;

            background: var(--surface);

            border: 1px solid var(--border);
            border-radius: var(--radius);

            box-shadow: var(--shadow);

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }

        .dashboard-card h3 {
            margin: 0 0 8px 0 !important;

            color: var(--text-dark) !important;
            font-size: 20px !important;
        }

        .dashboard-card p {
            margin: 0;

            color: var(--text-muted);
            font-size: 15px;
        }

        .dashboard-card strong {
            color: var(--text-dark);
        }


        /* =========================================================
           CARD ICONS
        ========================================================= */

        .card-icon {
            width: 62px;
            height: 62px;
            min-width: 62px;

            margin-right: 22px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 15px;

            font-size: 25px;
        }

        .alert-icon {
            background: var(--orange-soft);
            border: 1px solid #ffd49f;
        }

        .maintenance-icon {
            background: var(--blue-soft);
            border: 1px solid #cfe2ff;
        }


        /* =========================================================
           DIVIDERS
        ========================================================= */

        hr {
            margin-top: 2.5rem !important;
            margin-bottom: 2.5rem !important;

            border: none !important;
            border-top: 1px solid var(--border) !important;
        }

        [data-testid="stDivider"] {
            border-color: var(--border) !important;
        }


        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button {
            min-height: 48px;

            border-radius: 13px;

            border: 1px solid var(--border);

            background: white;

            color: #35566a;

            font-size: 15px;
            font-weight: 600;

            box-shadow: 0 3px 10px rgba(16, 37, 50, 0.04);

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        .stButton > button:hover {
            background: var(--green-soft);

            border-color: #b9e8cb;

            color: var(--green-dark);

            transform: translateY(-1px);

            box-shadow: 0 7px 16px rgba(16, 37, 50, 0.07);
        }

        .stButton > button:active {
            transform: translateY(0);
        }


        /* =========================================================
           INPUTS
        ========================================================= */

        div[data-baseweb="input"] {
            background: white !important;

            border: 1px solid var(--border) !important;

            border-radius: 12px !important;

            box-shadow: none !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #9fdcb7 !important;

            box-shadow: 0 0 0 3px rgba(32, 197, 99, 0.08) !important;
        }

        input {
            color: var(--text-dark) !important;
        }

        input::placeholder {
            color: #a5b2b8 !important;
        }


        /* =========================================================
           SELECTBOX
        ========================================================= */

        div[data-baseweb="select"] > div {
            background: white !important;

            border: 1px solid var(--border) !important;

            border-radius: 12px !important;

            min-height: 48px;

            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: #9fdcb7 !important;

            box-shadow: 0 0 0 3px rgba(32, 197, 99, 0.08) !important;
        }

        div[data-baseweb="select"] span {
            color: var(--text-dark) !important;
        }


        /* =========================================================
           TEXT INPUT LABELS
        ========================================================= */

        .stTextInput label,
        .stSelectbox label {
            color: var(--text-muted) !important;

            font-size: 15px !important;
            font-weight: 500 !important;
        }


        /* =========================================================
           DATA TABLES
        ========================================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);

            border-radius: 16px;

            overflow: hidden;

            box-shadow: var(--shadow);

            background: white;
        }

        [data-testid="stDataFrame"] iframe {
            border-radius: 16px;
        }


        /* =========================================================
           EXPANDERS
        ========================================================= */

        [data-testid="stExpander"] {
            background: white !important;

            border: 1px solid var(--border) !important;

            border-radius: 15px !important;

            box-shadow: var(--shadow);
        }

        [data-testid="stExpander"] summary {
            color: var(--text-dark) !important;
            font-weight: 600;
        }


        /* =========================================================
           ALERT / INFO / WARNING BOXES
        ========================================================= */

        [data-testid="stAlert"] {
            border-radius: 15px !important;

            border: 1px solid var(--border) !important;
        }

        .stAlert {
            font-size: 15px;
        }


        /* =========================================================
           WARNING / HEALTH SUMMARY CUSTOM CARDS
        ========================================================= */

        .health-warning {
            width: 100%;
            box-sizing: border-box;

            padding: 20px 24px;

            background: var(--yellow-soft);

            border: 1px solid #eee4ad;
            border-radius: 15px;

            color: #806c2d;

            font-size: 16px;
        }


        /* =========================================================
           PAGE CONTENT CARDS
        ========================================================= */

        .content-card {
            width: 100%;
            box-sizing: border-box;

            padding: 28px;

            background: white;

            border: 1px solid var(--border);
            border-radius: var(--radius);

            box-shadow: var(--shadow);
        }


        /* =========================================================
           FAILURE HISTORY / RECORD CARDS
        ========================================================= */

        .failure-card {
            width: 100%;
            box-sizing: border-box;

            padding: 25px;

            background: white;

            border: 1px solid var(--border);
            border-radius: 15px;

            box-shadow: var(--shadow);

            margin-bottom: 16px;
        }

        .failure-card h3 {
            margin: 0 0 10px 0 !important;

            color: var(--text-dark) !important;
        }


        /* =========================================================
           STATUS BADGES
        ========================================================= */

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;

            padding: 7px 12px;

            border-radius: 20px;

            font-size: 13px;
            font-weight: 600;
        }

        .status-success {
            background: var(--green-soft);
            color: var(--green-dark);
        }

        .status-warning {
            background: var(--orange-soft);
            color: #a76d18;
        }

        .status-danger {
            background: #fff0f1;
            color: #c43c4b;
        }


        /* =========================================================
           STATUS DOTS (replace emoji status circles)
        ========================================================= */

        .dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            margin-right: 7px;
            position: relative;
            top: -1px;
        }

        .dot-success { background: var(--green); }
        .dot-danger  { background: #e5484d; }
        .dot-warning { background: #e5a13b; }
        .dot-info    { background: #3b82e5; }


        /* =========================================================
           CHART CARDS
        ========================================================= */

        .chart-card {
            width: 100%;
            box-sizing: border-box;

            padding: 24px 26px;

            background: var(--surface);

            border: 1px solid var(--border);
            border-radius: var(--radius);

            box-shadow: var(--shadow);
        }

        .chart-card-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;

            margin-bottom: 4px;
        }

        .chart-card-header h4 {
            margin: 0 0 4px 0 !important;

            color: var(--text-dark) !important;
            font-size: 18px !important;
            font-weight: 700 !important;
        }

        .chart-card-header p {
            margin: 0;

            color: var(--text-muted);
            font-size: 13.5px;
        }

        .chip {
            display: inline-flex;
            align-items: center;

            padding: 4px 11px;

            border-radius: 20px;

            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.4px;
            text-transform: uppercase;

            white-space: nowrap;
        }

        .chip-green {
            background: var(--green-soft);
            color: var(--green-dark);
        }

        .chip-blue {
            background: var(--blue-soft);
            color: #2f66c9;
        }

        .rating-stars {
            font-size: 20px;
            letter-spacing: 2px;
            color: #e5a13b;
            text-align: right;
        }


        /* =========================================================
           QUICK ACCESS
        ========================================================= */

        .quick-access-card {
            background: white;

            border: 1px solid var(--border);

            border-radius: 16px;

            padding: 18px;

            box-shadow: var(--shadow);
        }


        /* =========================================================
           LOGIN / SIGNUP
           Keep the existing clean light appearance
        ========================================================= */

        .auth-header {
            text-align: center;

            margin-top: 3.5rem;
            margin-bottom: 2.8rem;
        }

        .auth-header h1 {
            margin-bottom: 0.8rem !important;

            color: var(--text-dark) !important;

            font-size: 42px !important;
            font-weight: 750 !important;
        }

        .auth-header p {
            margin: 0;

            color: var(--text-muted);

            font-size: 17px;
        }

        /* Login form */

        [data-testid="stForm"] {
            background: white;

            border: 1px solid var(--border);

            border-radius: 22px;

            padding: 32px 44px;

            box-shadow:
                0 15px 40px rgba(16, 37, 50, 0.07);
        }

        [data-testid="stForm"] label {
            color: #496a7c !important;
        }

        [data-testid="stForm"] input {
            min-height: 50px;
        }

        [data-testid="stFormSubmitButton"] > button {
            min-height: 52px;

            border: none !important;
            border-radius: 13px !important;

            background: var(--green) !important;

            color: white !important;

            font-size: 17px !important;
            font-weight: 600 !important;

            box-shadow: none !important;
        }

        [data-testid="stFormSubmitButton"] > button:hover {
            background: var(--green-dark) !important;

            color: white !important;
        }


        /* =========================================================
           SCROLLBAR
        ========================================================= */

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f3f6f5;
        }

        ::-webkit-scrollbar-thumb {
            background: #c5d0cd;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #aabbb5;
        }


        /* =========================================================
           RESPONSIVE
        ========================================================= */

        @media (max-width: 1200px) {

            .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }

            .hero-header h1 {
                font-size: 36px !important;
            }

            [data-testid="stMetricValue"] {
                font-size: 32px !important;
            }
        }


        @media (max-width: 900px) {

            .hero-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 20px;
            }

            .system-status {
                width: 100%;
                box-sizing: border-box;
            }

            .hero-header h1 {
                font-size: 30px !important;
            }

            .block-container {
                padding-left: 1.2rem;
                padding-right: 1.2rem;
            }

            .dashboard-card {
                padding: 20px;
            }
        }


        @media (max-width: 600px) {

            .block-container {
                padding-top: 1.5rem;
            }

            .hero-header {
                margin-bottom: 1.5rem;
            }

            .hero-header h1 {
                font-size: 26px !important;
            }

            .hero-label {
                font-size: 9px;
                letter-spacing: 1.6px;
            }

            .hero-header p {
                font-size: 14px;
            }

            [data-testid="stMetric"] {
                min-height: 110px;
                padding: 20px;
            }

            [data-testid="stMetricValue"] {
                font-size: 29px !important;
            }

            .dashboard-card {
                padding: 18px;
            }

            .card-icon {
                width: 52px;
                height: 52px;
                min-width: 52px;
                margin-right: 15px;
            }

            .auth-header {
                margin-top: 2rem;
            }

            .auth-header h1 {
                font-size: 32px !important;
            }

            [data-testid="stForm"] {
                padding: 25px 22px;
            }
        }


        /* =========================================================
           HIDE STREAMLIT HEADING ANCHOR ICONS
        ========================================================= */

        [data-testid="stHeaderActionElements"] {
            display: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
