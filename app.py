import streamlit as st
from src.catalog import GLOSSARY

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

    /* 3. Overview hero and status chips */
    .hero {
        background: linear-gradient(120deg, #142744 0%, #2B4A7A 100%);
        color: #FFFFFF; padding: 28px 32px; border-radius: 12px; margin: 8px 0 18px 0;
    }
    .hero-kicker { font-size: 0.85rem; opacity: 0.8; letter-spacing: 0.02em; }
    .hero-title  { font-size: 2.6rem; font-weight: 700; line-height: 1.2; margin: 4px 0 6px 0; }
    .hero-lead   { font-size: 1.15rem; max-width: 52rem; line-height: 1.5; }
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
    .chip {
        background: #F0F2F6; border: 1px solid #D5DBE5; border-radius: 999px;
        padding: 4px 12px; font-size: 0.9rem; color: #31333F;
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
st.sidebar.caption("InspectR PoC · iteration 1  \nRule set tk‑v2.0")


with st.sidebar.expander("Terms and acronyms"):
    st.markdown("\n\n".join(f"**{term}**: {text}" for term, text in GLOSSARY))

# --------------------------------------------------
# RUN SELECTED PAGE
# --------------------------------------------------

pg.run()