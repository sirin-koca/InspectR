import pandas as pd
import streamlit as st


st.subheader("Policy-as-Code")
st.caption("From TK/MUNDAT requirements to evidence-bound design-time OPA/Rego inspection")

st.markdown(
    """
    In this PoC, selected TK/MUNDAT requirements are operationalised as
    six Rego rules. OPA evaluates those rules against declared design-time
    evidence in a static pipeline blueprint. The Python application orchestrates
    the inspection and presents the machine-readable findings.
    """
)

st.markdown("#### Active TK/MUNDAT rule mapping")

rule_mapping = [
    {
        "Rule": "TK-001",
        "Requirement": "DPIA for elevated-risk processing",
        "Evidence": "data_source personal/special-category flags; dpia_checkpoint_defined",
        "PASS": "No DPIA trigger, or a DPIA checkpoint is defined",
        "FAIL": "DPIA is required but its checkpoint is not defined",
    },
    {
        "Rule": "TK-002",
        "Requirement": "Risk assessment for special-category data",
        "Evidence": "special-category source; risk_assessment_checkpoint_defined",
        "PASS": "No special-category source, or a risk checkpoint is defined",
        "FAIL": "Special-category source lacks a defined risk checkpoint",
    },
    {
        "Rule": "TK-003",
        "Requirement": "Agreement before personal-data transfer",
        "Evidence": "personal-data source; data_transfer; agreement flag",
        "PASS": "Transfer is not triggered, or an agreement checkpoint is defined",
        "FAIL": "Personal-data transfer lacks a defined agreement checkpoint",
    },
    {
        "Rule": "TK-004",
        "Requirement": "Lineage for integrated datasets",
        "Evidence": "data_integration; lineage_record_defined",
        "PASS": "No integration, or a lineage record is identified",
        "FAIL": "Integration is declared without a lineage record",
    },
    {
        "Rule": "TK-005",
        "Requirement": "Purpose compatibility review",
        "Evidence": "compliance_gate; purpose_compatibility_declared",
        "PASS": "Compatibility is declared in the design",
        "HUMAN": "Evidence is missing, false, or inconclusive",
    },
    {
        "Rule": "TK-006",
        "Requirement": "Complete sharing safeguards",
        "Evidence": "DPIA, risk, agreement, recipient, and encryption controls",
        "PASS": "All five planned safeguards are defined",
        "FAIL": "One or more planned safeguards are missing or false",
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
        "The blueprint defines the control required by the encoded design-time rule.",
        "The blueprint explicitly lacks or disables a required design-time control.",
        "The blueprint is missing enough information for automated inspection.",
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
