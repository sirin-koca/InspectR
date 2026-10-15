import pandas as pd
import streamlit as st


st.subheader("Evidence Traceability")
st.caption(
    "Each active rule identifies the blueprint evidence it reads and the "
    "design-time conclusion it is allowed to make."
)

st.info(
    """
    **Input evidence** is read from the uploaded JSON blueprint. **Derived
    evidence** is calculated by Rego from that input. A result confirms only
    the encoded design-time control; it is not a legal determination.
    """
)


def render_rule_table(rows: list[dict]) -> None:
    st.table(
        pd.DataFrame(rows, columns=["Traceability item", "Definition"])
        .set_index("Traceability item")
    )


rules = [
    {
        "id": "TK-001",
        "title": "DPIA requirement and completion",
        "reference": "GDPR Article 35; TK/MUNDAT risk-assessment operationalisation",
        "rows": [
            ("Applicability", "A data_source contains personal and special-category data."),
            ("Input selectors", "pipeline.nodes[*].type; pipeline.nodes[*].properties.contains_personal_data; pipeline.nodes[*].properties.contains_special_category_data; pipeline.nodes[*].properties.dpia_completed"),
            ("PASS", "No DPIA trigger exists, or a required DPIA is declared complete."),
            ("FAIL", "A DPIA is required and a compliance gate declares it incomplete."),
            ("Boundary", "Does not assess DPIA quality, approval, or legal adequacy."),
        ],
    },
    {
        "id": "TK-002",
        "title": "Special-category data risk assessment",
        "reference": "GDPR Articles 9 and 35; TK/MUNDAT risk operationalisation",
        "rows": [
            ("Applicability", "A data_source contains special-category data."),
            ("Input selectors", "pipeline.nodes[*].properties.contains_special_category_data; pipeline.nodes[*].properties.risk_assessment_completed"),
            ("PASS", "No special-category source exists, or assessment is complete."),
            ("FAIL", "Special-category data exists and assessment is explicitly incomplete."),
            ("Boundary", "Does not evaluate risk content, mitigations, or residual risk."),
        ],
    },
    {
        "id": "TK-003",
        "title": "Data-sharing agreement",
        "reference": "GDPR Articles 5, 6, and 28; TK/MUNDAT sharing governance",
        "rows": [
            ("Applicability", "Personal data is processed and a data_transfer node exists."),
            ("Input selectors", "pipeline.nodes[*].properties.contains_personal_data; pipeline.nodes[*].type == data_transfer; pipeline.nodes[*].properties.data_sharing_agreement_exists"),
            ("PASS", "Transfer is not triggered, or agreement evidence is true."),
            ("FAIL", "Personal-data transfer is triggered and agreement evidence is false."),
            ("Boundary", "Does not verify the external agreement or its legal validity."),
        ],
    },
    {
        "id": "TK-004",
        "title": "Data lineage and provenance",
        "reference": "GDPR Articles 5(2) and 30; TK/MUNDAT traceability",
        "rows": [
            ("Applicability", "A data_integration node exists."),
            ("Input selectors", "pipeline.nodes[*].type == data_integration; pipeline.nodes[*].properties.lineage_available"),
            ("PASS", "No integration node exists, or lineage is available."),
            ("FAIL", "An integration node explicitly lacks lineage."),
            ("Boundary", "Does not verify lineage quality, completeness, or runtime generation."),
        ],
    },
    {
        "id": "TK-005",
        "title": "Purpose compatibility",
        "reference": "GDPR Articles 5(1)(b) and 6(4); TK/MUNDAT governance review",
        "rows": [
            ("Applicability", "A compliance_gate provides purpose-compatibility evidence."),
            ("Input selectors", "pipeline.nodes[*].type == compliance_gate; pipeline.nodes[*].properties.purpose_compatible"),
            ("PASS", "Purpose compatibility is explicitly true."),
            ("HUMAN", "Purpose compatibility is missing, false, or inconclusive."),
            ("Boundary", "Does not perform contextual legal purpose analysis."),
        ],
    },
    {
        "id": "TK-006",
        "title": "Complete sharing safeguards",
        "reference": "GDPR Articles 25 and 32; TK/MUNDAT sharing safeguards",
        "rows": [
            ("Applicability", "A sharing workflow contains the required safeguard nodes."),
            ("Input selectors", "dpia_check.dpia_completed; dpia_check.risk_assessment_completed; sharing_assessment.data_sharing_agreement_exists; sharing_assessment.recipient_approved; share_dataset.encrypted_in_transit"),
            ("PASS", "All five safeguards are explicitly true."),
            ("FAIL", "One or more safeguards are missing or false."),
            ("Boundary", "Does not verify that safeguards operate correctly at runtime."),
        ],
    },
]

for rule in rules:
    st.markdown(f"#### {rule['id']} — {rule['title']}")
    st.caption(rule["reference"])
    render_rule_table(
        [
            {"Traceability item": item, "Definition": definition}
            for item, definition in rule["rows"]
        ]
    )
