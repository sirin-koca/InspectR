import pandas as pd
import streamlit as st


st.subheader("TK Use Case — MUNDAT")
st.caption("Trondheim Kommune data-sharing use case")

st.info(
    """
    InspectR uses a simplified TK/MUNDAT data-sharing workflow as its
    proof-of-concept case. The active engine evaluates six design-time rules
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
                "Description": "OPA evaluates six TK/MUNDAT Rego rules independently of the Streamlit interface.",
            },
            {
                "Aspect": "Output",
                "Description": "Rule-level PASS, FAIL, or HUMAN results with evidence, reasons, and remedies.",
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
        "Rule": "TK-001",
        "Requirement": "DPIA for elevated-risk processing",
        "Applicability": "Personal and special-category data are both declared.",
        "Evidence": "data_source flags; compliance_gate.dpia_completed",
        "PASS": "No trigger, or DPIA complete.",
        "FAIL": "DPIA required but incomplete.",
        "HUMAN": "Not currently returned for missing evidence.",
        "Boundary": "Does not assess DPIA quality or legal adequacy.",
    },
    {
        "Rule": "TK-002",
        "Requirement": "Risk assessment for special-category data",
        "Applicability": "A special-category data source is declared.",
        "Evidence": "data_source special-category flag; risk_assessment_completed",
        "PASS": "No special-category source, or assessment complete.",
        "FAIL": "Assessment explicitly incomplete.",
        "HUMAN": "Not currently returned for missing evidence.",
        "Boundary": "Does not assess risk content or mitigation quality.",
    },
    {
        "Rule": "TK-003",
        "Requirement": "Agreement before personal-data transfer",
        "Applicability": "Personal data and a data-transfer node are declared.",
        "Evidence": "personal-data flag; data_transfer; agreement flag",
        "PASS": "Transfer not triggered, or agreement verified.",
        "FAIL": "Transfer lacks verified agreement.",
        "HUMAN": "Not currently returned for missing evidence.",
        "Boundary": "Does not verify an external agreement or legal validity.",
    },
    {
        "Rule": "TK-004",
        "Requirement": "Lineage for integrated datasets",
        "Applicability": "A data-integration node is declared.",
        "Evidence": "data_integration; lineage_available",
        "PASS": "No integration, or lineage available.",
        "FAIL": "Integration lacks lineage.",
        "HUMAN": "Not currently returned for missing evidence.",
        "Boundary": "Does not verify lineage quality or runtime generation.",
    },
    {
        "Rule": "TK-005",
        "Requirement": "Purpose compatibility review",
        "Applicability": "A compliance gate provides purpose evidence.",
        "Evidence": "compliance_gate; purpose_compatible",
        "PASS": "Compatibility explicitly verified.",
        "FAIL": "Not used by the current rule.",
        "HUMAN": "Evidence is missing, false, or inconclusive.",
        "Boundary": "Does not perform contextual legal purpose analysis.",
    },
    {
        "Rule": "TK-006",
        "Requirement": "Complete sharing safeguards",
        "Applicability": "The required sharing safeguard nodes are present.",
        "Evidence": "DPIA, risk, agreement, recipient, and encryption controls",
        "PASS": "All five safeguards are explicitly true.",
        "FAIL": "One or more safeguards are missing or false.",
        "HUMAN": "Not currently returned by this rule.",
        "Boundary": "Does not verify runtime operation of the safeguards.",
    },
]

st.dataframe(
    pd.DataFrame(rules),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "The six rules are operational proxies for the TK/MUNDAT PoC. They do not "
    "establish complete GDPR compliance, reproduce the full MUNDAT process, or "
    "replace legal or organisational judgement."
)
