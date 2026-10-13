import pandas as pd
import streamlit as st


st.subheader("TK Use Case - MUNDAT")
st.caption("Trondheim Kommune (TK) data-sharing use case")

st.info(
    """
    This page explains the TK/MUNDAT scenario that InspectR uses as its
    proof-of-concept evaluation case. The blueprint is a simplified,
    design-time representation of the documented TK data-sharing flow. It is
    not a complete reproduction of the MUNDAT workflow or TK's actual
    production implementation.
    """
)

# ---------------------------------------------------------------------
# USE-CASE CONTEXT
# ---------------------------------------------------------------------

st.markdown("#### Use-Case Context")

context = [
    {
        "Aspect": "Use case",
        "Description": "Municipal data-sharing requests assembled from one or more data sources.",
    },
    {
        "Aspect": "Compliance concern",
        "Description": "The request, data access, compliance checks, and sharing decision should be represented and traceable.",
    },
    {
        "Aspect": "Regulatory scope",
        "Description": "Selected GDPR Articles 25, 30, and 35, operationalised for the TK/MUNDAT context.",
    },
    {
        "Aspect": "InspectR input",
        "Description": "A static inLUMEN pipeline blueprint containing nodes, connections, and declared compliance metadata.",
    },
    {
        "Aspect": "InspectR output",
        "Description": "Rule-level OK, FAIL, or HUMAN results with evidence, reasons, and remediation.",
    },
]

st.dataframe(
    pd.DataFrame(context),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------------------
# SELECTED DESIGN-TIME COMPLIANCE ISSUES
# ---------------------------------------------------------------------

st.markdown("#### TK UC Compliance Issues (selected subset)")

selected_compliance_issues = [
    {
        "TK compliance issue": "Pipeline structure and compliance checkpoints",
        "Design-time evidence": "Node labels and connections",
        "How InspectR checks it": "TK-STRUCT-01 verifies the seven required stages and six expected connections.",
        "Assessment boundary": "Checks declared blueprint structure; does not verify runtime behaviour.",
    },
    {
        "TK compliance issue": "Data-source provenance and approval",
        "Design-time evidence": "Source node: source_id and approved_source",
        "How InspectR checks it": "TK-DATA-01 verifies that each source has an identifier and is marked approved.",
        "Assessment boundary": "Checks declared metadata; does not verify the source or approval externally.",
    },
    {
        "TK compliance issue": "Processing traceability",
        "Design-time evidence": "has_logging on each pipeline node",
        "How InspectR checks it": "TK-TRACE-01 verifies that every stage declares logging capability.",
        "Assessment boundary": "Does not verify that logs are produced, complete, or retained.",
    },
    {
        "TK compliance issue": "DPIA and risk-assessment checkpoint",
        "Design-time evidence": "A node labelled run_compliance_checks",
        "How InspectR checks it": "TK-RISK-01 verifies that a dedicated compliance and risk-check stage exists.",
        "Assessment boundary": "Does not assess whether a DPIA was completed or is legally adequate.",
    },
    {
        "TK compliance issue": "Human review before sharing",
        "Design-time evidence": "human_oversight on prepare_sharing_decision",
        "How InspectR checks it": "TK-HUMAN-01 returns OK, FAIL, or HUMAN based on the declared value.",
        "Assessment boundary": "Checks declared review evidence; does not verify review in practice.",
    },
]

st.dataframe(
    pd.DataFrame(selected_compliance_issues),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "This is a selected design-time subset. InspectR evaluates machine-readable "
    "blueprint evidence; it does not establish complete GDPR compliance."
)

# ---------------------------------------------------------------------
# TK PIPELINE BLUEPRINT
# ---------------------------------------------------------------------

st.markdown("#### TK Pipeline Blueprint")

pipeline_stages = [
    {
        "Order": 1,
        "Stage": "Request intake",
        "Blueprint label": "tk_request_intake",
        "Purpose in the PoC": "Receive the data-sharing request.",
    },
    {
        "Order": 2,
        "Stage": "Request validation",
        "Blueprint label": "validate_request",
        "Purpose in the PoC": "Validate the request before data retrieval.",
    },
    {
        "Order": 3,
        "Stage": "Data retrieval",
        "Blueprint label": "retrieve_relevant_data",
        "Purpose in the PoC": "Identify and retrieve relevant data.",
    },
    {
        "Order": 4,
        "Stage": "Compliance preparation",
        "Blueprint label": "process_data_for_compliance",
        "Purpose in the PoC": "Prepare and process data for compliance checks.",
    },
    {
        "Order": 5,
        "Stage": "Compliance and risk checks",
        "Blueprint label": "run_compliance_checks",
        "Purpose in the PoC": "Provide the dedicated compliance and risk checkpoint.",
    },
    {
        "Order": 6,
        "Stage": "Sharing decision support",
        "Blueprint label": "prepare_sharing_decision",
        "Purpose in the PoC": "Prepare the sharing recommendation and review point.",
    },
    {
        "Order": 7,
        "Stage": "Decision output",
        "Blueprint label": "tk_decision_output",
        "Purpose in the PoC": "Produce the final decision output.",
    },
]

st.dataframe(
    pd.DataFrame(pipeline_stages),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Order": st.column_config.NumberColumn(format="%d"),
    },
)

st.caption(
    "TK-STRUCT-01 checks these seven labels and the six expected connections. "
    "The page describes the blueprint; the evaluation page runs the Rego policy."
)

st.caption(
    "DPIA scope: the current PoC checks for a designated risk-assessment "
    "checkpoint. It does not verify that a DPIA was completed or that it "
    "is legally adequate; both are outside the scope of this project."
)
# ---------------------------------------------------------------------
# GDPR SCOPE AND EXECUTABLE RULES
# ---------------------------------------------------------------------

st.markdown("#### TK/MUNDAT GDPR Scope and Executable Rules")

rule_mapping = [
    {
        "GDPR basis / category": "GDPR Art. 25",
        "TK/MUNDAT interpretation": "Privacy-by-design pipeline structure",
        "Rule ID": "TK-STRUCT-01",
        "Rule checks": "Seven required stages and their expected connections",
        "Blueprint evidence": "pipeline.nodes; pipeline.connections",
        "Relationship": "Supporting operational proxy",
    },
    {
        "GDPR basis / category": "GDPR Art. 30",
        "TK/MUNDAT interpretation": "Processing provenance",
        "Rule ID": "TK-DATA-01",
        "Rule checks": "Every source has a source identifier and approval status",
        "Blueprint evidence": "compliance_extensions.source_id; approved_source",
        "Relationship": "Partial operational support",
    },
    {
        "GDPR basis / category": "GDPR Art. 30",
        "TK/MUNDAT interpretation": "Processing traceability",
        "Rule ID": "TK-TRACE-01",
        "Rule checks": "Every pipeline stage declares logging capability",
        "Blueprint evidence": "compliance_extensions.has_logging",
        "Relationship": "Partial operational support",
    },
    {
        "GDPR basis / category": "GDPR Art. 35",
        "TK/MUNDAT interpretation": "DPIA and risk-assessment checkpoint",
        "Rule ID": "TK-RISK-01",
        "Rule checks": "A dedicated compliance and risk-check stage exists",
        "Blueprint evidence": "pipeline.nodes.label",
        "Relationship": "Checkpoint-presence proxy",
    },
    {
        "GDPR basis / category": "TK/MUNDAT safeguard",
        "TK/MUNDAT interpretation": "Human review before sharing",
        "Rule ID": "TK-HUMAN-01",
        "Rule checks": "The sharing-decision stage declares human review or override evidence",
        "Blueprint evidence": "compliance_extensions.human_oversight",
        "Relationship": "Use-case governance safeguard",
    },
]

st.dataframe(
    pd.DataFrame(rule_mapping),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "These mappings describe limited design-time operationalisations. They do "
    "not establish legal compliance with the GDPR as a whole."
)

# ---------------------------------------------------------------------
# EVIDENCE MODEL AND LIMITATIONS
# ---------------------------------------------------------------------

left, right = st.columns(2)

with left:
    st.markdown("#### Evidence inspected by InspectR")
    st.markdown(
        """
        - **Pipeline structure:** node labels and connections.
        - **Source provenance:** source identifiers and approval declarations.
        - **Traceability:** declared logging capability on each stage.
        - **Risk checkpoint:** presence of `run_compliance_checks`.
        - **Sharing safeguard:** human-review or override metadata on
          `prepare_sharing_decision`.
        """
    )

with right:
    st.markdown("#### What the PoC does not establish")
    st.markdown(
        """
        - Complete GDPR compliance.
        - A complete Article 30 record of processing activities.
        - A complete Article 35 DPIA or legal risk determination.
        - The legal sufficiency of a source approval or logging declaration.
        - That the simplified blueprint is TK's actual production workflow.
        """
    )

st.success(
    "InspectR evaluates declared blueprint evidence against five independent "
    "TK/MUNDAT Rego rules. A successful result means that the encoded rule "
    "was satisfied by the available evidence, not that the underlying legal "
    "obligation has been fully discharged."
)
