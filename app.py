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

if "evaluation_results" not in st.session_state:
    st.session_state["evaluation_results"] = None

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

pages = [
    st.Page("pages/research.py", title=":: Research"),
    st.Page("pages/main.py", title=":: InspectR", default=True),
    st.Page("pages/datapipeline.py", title=":: Datapipeline"),
    st.Page("pages/pac.py", title=":: Engineering PaC"),
    st.Page("pages/tk_uc.py", title=":: Use Case"),
    st.Page("pages/taxonomy.py", title=":: Taxonomy"),
    st.Page("pages/architecture.py", title=":: Architecture"),
    st.Page("pages/evaluation.py", title=":: Evaluation"),
    st.Page("pages/evidence.py", title=":: Evidence"),
    st.Page("pages/about.py", title=":: About"),
]

pg = st.navigation(pages)

st.sidebar.image(
    "images/datapact-logo.png",
    width=140,
)
st.sidebar.image(
    "images/uio.png",
    width=145,
)
# --------------------------------------------------
# GLOBAL FOOTER
# --------------------------------------------------

st.markdown(
    """
    <style>
    .inspectr-footer {
        position: fixed;
        bottom: 20px;
        left: 270px;
        color: magenta;
        font-size: 0.85rem;
        z-index: 999;
    }
    </style>

    <div class="inspectr-footer">
        InspectR PoC 
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# RUN SELECTED PAGE
# --------------------------------------------------

pg.run()