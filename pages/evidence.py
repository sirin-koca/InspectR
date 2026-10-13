import pandas as pd
import streamlit as st


st.subheader("Evidence Traceability")
st.caption(
    "This page documents where each InspectR rule obtains its design-time "
    "evidence and how the evidence produces a result."
)

st.info(
    """
    **Input evidence** is read from the uploaded JSON blueprint. **Derived
    evidence** is calculated by Rego from that input. The JSON selectors below
    identify the source of the evidence; they are not precomputed results.
    """
)


def render_rule_table(rows: list[dict]) -> None:
    st.table(
        pd.DataFrame(rows, columns=["Traceability item", "Definition"])
        .set_index("Traceability item")
    )


rules = [
    {
        "id": "TK-STRUCT-01",
        "title": "Pipeline structure",
        "reference": "MUNDAT pipeline structure; supporting operational proxy for GDPR Article 25",
        "rows": [
            {
                "Traceability item": "Input evidence",
                "Definition": "Node labels and connection endpoints in the uploaded blueprint.",
            },
            {
                "Traceability item": "JSON selector",
                "Definition": "pipeline.nodes[*].label; pipeline.connections[*].from; pipeline.connections[*].to",
            },
            {
                "Traceability item": "Evaluation",
                "Definition": "Checks the seven required stages and six expected connections.",
            },
            {
                "Traceability item": "Result",
                "Definition": "OK when the required stages and connections match; otherwise FAIL.",
            },
            {
                "Traceability item": "Remedy",
                "Definition": "Add missing stages or connect the stages in the documented order.",
            },
            {
                "Traceability item": "Boundary",
                "Definition": "Checks declared graph structure, not runtime behaviour or complete privacy-by-design compliance.",
            },
        ],
    },
    {
        "id": "TK-DATA-01",
        "title": "Data-source provenance and approval",
        "reference": "MUNDAT data-source and provenance requirement; partial operational support for GDPR Article 30",
        "rows": [
            {
                "Traceability item": "Input evidence",
                "Definition": "Source-node compliance metadata: source identifier and approval declaration.",
            },
            {
                "Traceability item": "JSON selector",
                "Definition": "pipeline.nodes[*][kind=source].compliance_extensions.source_id; pipeline.nodes[*][kind=source].compliance_extensions.approved_source",
            },
            {
                "Traceability item": "Evaluation",
                "Definition": "Checks that every source has a non-empty source_id and approved_source is true.",
            },
            {
                "Traceability item": "Result",
                "Definition": "OK when all source nodes satisfy both conditions; otherwise FAIL.",
            },
            {
                "Traceability item": "Remedy",
                "Definition": "Add or correct the source identifier and approval evidence.",
            },
            {
                "Traceability item": "Boundary",
                "Definition": "Does not verify the source, approval authority, legal basis, or factual truth of the declaration.",
            },
        ],
    },
    {
        "id": "TK-TRACE-01",
        "title": "Processing traceability",
        "reference": "MUNDAT logging and traceability requirement; partial operational support for GDPR Article 30",
        "rows": [
            {
                "Traceability item": "Input evidence",
                "Definition": "Logging declaration on every pipeline node.",
            },
            {
                "Traceability item": "JSON selector",
                "Definition": "pipeline.nodes[*].compliance_extensions.has_logging",
            },
            {
                "Traceability item": "Evaluation",
                "Definition": "Checks whether has_logging is true for every node.",
            },
            {
                "Traceability item": "Result",
                "Definition": "OK when all nodes declare logging; otherwise FAIL and the affected node labels are returned.",
            },
            {
                "Traceability item": "Remedy",
                "Definition": "Declare logging capability for every pipeline stage.",
            },
            {
                "Traceability item": "Boundary",
                "Definition": "Does not verify that logs are produced, complete, protected, or retained.",
            },
        ],
    },
    {
        "id": "TK-RISK-01",
        "title": "DPIA and risk-assessment checkpoint",
        "reference": "MUNDAT DPIA and risk-assessment requirement; checkpoint-presence proxy for GDPR Article 35",
        "rows": [
            {
                "Traceability item": "Input evidence",
                "Definition": "Presence of the dedicated compliance and risk-check stage.",
            },
            {
                "Traceability item": "JSON selector",
                "Definition": "pipeline.nodes[*].label == \"run_compliance_checks\"",
            },
            {
                "Traceability item": "Evaluation",
                "Definition": "Checks whether a node with the exact label run_compliance_checks exists.",
            },
            {
                "Traceability item": "Result",
                "Definition": "OK when the checkpoint exists; otherwise FAIL.",
            },
            {
                "Traceability item": "Remedy",
                "Definition": "Add a stage for the documented compliance, DPIA, and risk checks.",
            },
            {
                "Traceability item": "Boundary",
                "Definition": "Does not determine whether a DPIA is required, completed, accurate, or legally adequate.",
            },
        ],
    },
    {
        "id": "TK-HUMAN-01",
        "title": "Human review before sharing",
        "reference": "MUNDAT sharing-decision review requirement; TK/MUNDAT governance safeguard",
        "rows": [
            {
                "Traceability item": "Input evidence",
                "Definition": "Human-oversight declaration on the sharing-decision stage.",
            },
            {
                "Traceability item": "JSON selector",
                "Definition": "pipeline.nodes[*][label=prepare_sharing_decision].compliance_extensions.human_oversight",
            },
            {
                "Traceability item": "Evaluation",
                "Definition": "true means explicit review evidence; false means review is disabled; missing means evidence is insufficient.",
            },
            {
                "Traceability item": "Result",
                "Definition": "OK for true, FAIL for false, and HUMAN when the field is missing.",
            },
            {
                "Traceability item": "Remedy",
                "Definition": "Declare human review or an override checkpoint before sharing.",
            },
            {
                "Traceability item": "Boundary",
                "Definition": "Does not verify that review occurs in practice or establish complete GDPR compliance.",
            },
        ],
    },
]

for rule in rules:
    st.markdown(f"#### {rule['id']} — {rule['title']}")
    st.caption(rule["reference"])
    render_rule_table(rule["rows"])

st.caption(
    "The displayed evidence is traceable to blueprint selectors and Rego "
    "conditions. A rule result confirms only the encoded design-time control; "
    "it is not a legal determination."
)
