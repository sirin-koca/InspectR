import pandas as pd
import streamlit as st

from src.catalog import RULES, STATUSES


st.subheader("TK Use Case — MUNDAT")
st.caption(
    "This page describes the bounded Sickleave scenario and its planned "
    "design-time compliance checkpoints."
)
st.caption("Trondheim Kommune data-sharing use case")

st.info(
    """
    InspectR uses a simplified TK/MUNDAT data-sharing workflow as its
    proof-of-concept case. The active engine evaluates three design-time rules
    against a compliance-enriched JSON blueprint. This is not a complete
    reproduction of the MUNDAT workflow or a complete legal assessment.
    """
)

st.markdown("#### Use-case context")

st.dataframe(
    pd.DataFrame(
        [
            {
                "Aspect": "Use case",
                "Description": "Municipal data-sharing requests assembled from one or more data sources.",
            },
            {
                "Aspect": "Input",
                "Description": "A static JSON blueprint containing nodes, connections, and declared evidence.",
            },
            {
                "Aspect": "Policy engine",
                "Description": "OPA evaluates three TK/MUNDAT Rego rules independently of the Streamlit interface.",
            },
            {
                "Aspect": "Output",
                "Description": "One result per rule (" + ", ".join(STATUSES) + ") with evidence, reason, and remedy.",
            },
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("#### TK/MUNDAT pipeline represented in the PoC")

st.dataframe(
    pd.DataFrame(
        [
            ("request", "Request intake"),
            ("classify_request", "Request and data classification"),
            ("dpia_check", "DPIA and risk-assessment gate"),
            ("metadata_catalog", "Catalogue records for sources and lineage"),
            ("data sources", "Municipal data sources"),
            ("extract_data", "Data processing"),
            ("integrate_dataset", "Data integration and lineage"),
            ("anonymisation", "Privacy control"),
            ("sharing_assessment", "Sharing agreement and recipient approval"),
            ("share_dataset", "Encrypted data transfer"),
        ],
        columns=["Blueprint node or group", "Purpose in the PoC"],
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("#### Active TK policy rules")

rules = [
    {
        "Rule": rule["id"],
        "Requirement": rule["title"],
        "Trigger": rule["trigger"],
        "Control": rule["control"],
        **{status: rule["outcomes"].get(status, "Not produced by this rule.") for status in STATUSES if status != "ERROR"},
        "Boundary": rule["boundary"],
    }
    for rule in RULES
]

st.dataframe(
    pd.DataFrame(rules),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "The three rules are operational proxies for the TK/MUNDAT PoC. They do not "
    "establish complete GDPR compliance, reproduce the full MUNDAT process, or "
    "replace legal or organisational judgement."
)
