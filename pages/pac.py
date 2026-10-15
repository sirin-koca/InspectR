import pandas as pd
import streamlit as st


st.subheader("Policy-as-Code")
st.caption("From TK/MUNDAT requirements to evidence-bound OPA/Rego evaluation")

st.markdown(
    """
    In this PoC, selected TK/MUNDAT requirements are operationalised as
    six Rego rules. OPA evaluates those rules against declared evidence in a
    static pipeline blueprint. The Python application orchestrates the
    evaluation and presents the machine-readable findings.
    """
)

st.markdown("#### Active TK/MUNDAT rule mapping")

rule_mapping = [
    {
        "Rule": "TK-001",
        "Requirement": "DPIA for elevated-risk processing",
        "Evidence": "data_source personal/special-category flags; dpia_completed",
        "PASS": "No DPIA trigger, or required DPIA is complete",
        "FAIL": "DPIA is required but explicitly incomplete",
    },
    {
        "Rule": "TK-002",
        "Requirement": "Risk assessment for special-category data",
        "Evidence": "special-category source; risk_assessment_completed",
        "PASS": "No special-category source, or assessment is complete",
        "FAIL": "Special-category source lacks a completed assessment",
    },
    {
        "Rule": "TK-003",
        "Requirement": "Agreement before personal-data transfer",
        "Evidence": "personal-data source; data_transfer; agreement flag",
        "PASS": "Transfer is not triggered, or agreement is verified",
        "FAIL": "Personal-data transfer lacks a verified agreement",
    },
    {
        "Rule": "TK-004",
        "Requirement": "Lineage for integrated datasets",
        "Evidence": "data_integration; lineage_available",
        "PASS": "No integration, or lineage is available",
        "FAIL": "Integration is declared without lineage",
    },
    {
        "Rule": "TK-005",
        "Requirement": "Purpose compatibility review",
        "Evidence": "compliance_gate; purpose_compatible",
        "PASS": "Compatibility is explicitly verified",
        "HUMAN": "Evidence is missing, false, or inconclusive",
    },
    {
        "Rule": "TK-006",
        "Requirement": "Complete sharing safeguards",
        "Evidence": "DPIA, risk, agreement, recipient, and encryption controls",
        "PASS": "All five safeguards are explicitly true",
        "FAIL": "One or more safeguards are missing or false",
    },
]

st.dataframe(
    pd.DataFrame(rule_mapping),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "These are TK/MUNDAT-specific design-time operationalisations. They are "
    "not direct implementations of GDPR or EU AI Act text."
)

st.markdown("#### Evaluation flow")

flow_columns = st.columns(5)
for column, (step, description) in zip(
    flow_columns,
    [
        ("1. Blueprint", "Static JSON evidence"),
        ("2. Policy", "TK/MUNDAT interpretation"),
        ("3. Rego", "Executable conditions"),
        ("4. OPA", "Independent evaluation"),
        ("5. Result", "Evidence and remedy"),
    ],
):
    with column:
        with st.container(border=True):
            st.markdown(f"**{step}**")
            st.caption(description)

st.markdown("#### Result semantics")

result_columns = st.columns(3)
for column, title, description in zip(
    result_columns,
    ("🟢 PASS", "🔴 FAIL", "🟠 HUMAN"),
    (
        "The available evidence satisfies the encoded operational rule.",
        "The evidence explicitly violates the encoded operational rule.",
        "The evidence is missing, ambiguous, or insufficient for automation.",
    ),
):
    with column:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(description)

st.markdown("#### Automation boundary")
st.warning(
    "A result is valid only relative to the TK/MUNDAT operational interpretation "
    "and blueprint evidence model. InspectR does not establish complete legal "
    "compliance or verify runtime behaviour."
)
