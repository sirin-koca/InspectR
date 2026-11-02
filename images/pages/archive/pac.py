import pandas as pd
import streamlit as st

from src.catalog import DROPPED_RULES, RULE_SET_VERSION, RULES, STATUS_MODEL


st.subheader("Policy-as-Code")
st.caption("From TK/MUNDAT requirements to evidence-bound design-time OPA/Rego inspection")

st.markdown(
    f"""
    In this PoC, selected TK/MUNDAT requirements are operationalised as
    {len(RULES)} Rego rules (rule set `{RULE_SET_VERSION}`). Each rule has the form
    **IF trigger THEN control**. OPA evaluates the rules against declared
    design-time evidence in a static pipeline blueprint. The Python application
    orchestrates the inspection and presents the machine-readable findings.
    """
)

st.markdown("#### Active TK/MUNDAT rule mapping")

st.dataframe(
    pd.DataFrame(
        [
            {
                "Rule": rule["id"],
                "Requirement": rule["title"],
                "Legal basis": rule["legal_reference"],
                "Trigger": rule["trigger"],
                "Control": rule["control"],
                "Evidence class": rule["evidence_class"],
                "Possible statuses": ", ".join(rule["outcomes"]),
            }
            for rule in RULES
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "These are TK/MUNDAT-specific design-time operationalisations. They are "
    "not direct implementations of GDPR or EU AI Act text. Any rule can also "
    "return ERROR if InspectR itself fails."
)

with st.expander("Rules dropped from the v1 rule set"):
    st.dataframe(
        pd.DataFrame(DROPPED_RULES, columns=["Rule", "Requirement", "Reason"]),
        use_container_width=True,
        hide_index=True,
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

st.markdown(
    "Each fact in the blueprint is **true**, **false** or **undetermined** "
    "(absent, null, or not a boolean). An undetermined fact never produces PASS."
)

st.dataframe(
    pd.DataFrame(
        [
            {"Status": f"{icon} {status}", "Meaning": meaning, "Who acts next": actor}
            for status, icon, meaning, actor in STATUS_MODEL
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("#### Automation boundary")
st.warning(
    "A result is valid only relative to the TK/MUNDAT operational interpretation "
    "and blueprint evidence model. InspectR does not establish complete legal "
    "compliance or verify runtime behaviour."
)
