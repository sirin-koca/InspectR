import streamlit as st

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="InspectR | PoC",
    page_icon="👁️‍🗨️",
    layout="wide",
    initial_sidebar_state="expanded",
)
# --------------------------------------------------
# THE ONE GLOBAL CSS BLOCK 
#    (app-wide tweaks)
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* 1. Makes the navigation menu text bigger */
    [data-testid="stSidebarNavItems"] span {
        font-size: 1.1rem !important; 
    }
    [data-testid="stSidebarNavItems"] svg {
        transform: scale(1.1); 
    }

    /* 2. Diasable top space/padding on every page */
    section.stMain .block-container {
        padding-top: 10px !important; 
        padding-bottom: 1rem !important;
    }

    /* 3. Custom reusable class for markdown background fields */
    .custom-card {
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 8px; 
        color: #31333F;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "blueprint" not in st.session_state:
    st.session_state["blueprint"] = None

if "blueprint_filename" not in st.session_state:
    st.session_state["blueprint_filename"] = None


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

pages = [
    st.Page("pages/overview.py", title="Overview", default=True),
    st.Page("pages/research.py", title="Research"),
    st.Page("pages/method.py", title="Method"),
    st.Page("pages/case.py", title="Case: TK / MUNDAT"),
    st.Page("pages/inspection.py", title="Inspect"),
    st.Page("pages/validation.py", title="Validation"),
]
# Earlier exploratory pages are kept in pages/archive/ and are not shown.

pg = st.navigation(pages)

st.sidebar.image(
    "images/datapact-logo.png",
    width=140,
)
st.sidebar.image(
    "images/uio.png",
    width=145,
)
st.sidebar.caption("InspectR · iteration 1 · rule set tk-v2.0")

# --------------------------------------------------
# RUN SELECTED PAGE
# --------------------------------------------------

pg.run()