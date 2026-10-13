import pandas as pd
import streamlit as st


st.subheader("Policy-as-Code")
st.caption("From contextual requirements to evidence-bound design-time evaluation")

st.markdown(
    """
    Policy-as-Code is the implementation layer between an operational
    requirement and an automated decision. In this PoC, selected TK/MUNDAT
    requirements are represented as Rego rules and evaluated by OPA against
    evidence declared in a static pipeline blueprint.
    """
)

# ---------------------------------------------------------------------
# TRANSLATION PIPELINE
# ---------------------------------------------------------------------

st.markdown("#### The Policy Translation Pipeline")

pipeline = [
    ("1. GDPR / regulation", "Legal source", "Contextual requirement"),
    ("2. TK/MUNDAT policy", "Operational interpretation", "What the use case requires"),
    ("3. Blueprint evidence", "Observable representation", "Nodes, connections, and metadata"),
    ("4. Rego rule", "Executable condition", "Deterministic Policy-as-Code"),
    ("5. InspectR result", "Explainable decision", "OK, FAIL, or HUMAN"),
]

for row in range(0, len(pipeline), 3):
    columns = st.columns(3)
    for column, (title, label, description) in zip(columns, pipeline[row : row + 3]):
        with column:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(label)
                st.write(description)

st.info(
    "The Rego rules do not interpret legal text directly. They evaluate explicit "
    "operational conditions against declared blueprint evidence."
)

# ---------------------------------------------------------------------
# RULE MAPPING
# ---------------------------------------------------------------------

st.markdown("#### Current TK/MUNDAT Rule Mapping")

rule_mapping = [
    {
        "Basis / category": "GDPR Art. 25",
        "Operational interpretation": "Privacy-by-design pipeline structure",
        "Rule ID": "TK-STRUCT-01",
        "Evidence": "pipeline.nodes; pipeline.connections",
        "Relationship": "Supporting operational proxy",
    },
    {
        "Basis / category": "GDPR Art. 30",
        "Operational interpretation": "Processing provenance",
        "Rule ID": "TK-DATA-01",
        "Evidence": "source_id; approved_source",
        "Relationship": "Partial operational support",
    },
    {
        "Basis / category": "GDPR Art. 30",
        "Operational interpretation": "Processing traceability",
        "Rule ID": "TK-TRACE-01",
        "Evidence": "has_logging",
        "Relationship": "Partial operational support",
    },
    {
        "Basis / category": "GDPR Art. 35",
        "Operational interpretation": "DPIA and risk-assessment checkpoint",
        "Rule ID": "TK-RISK-01",
        "Evidence": "pipeline.nodes.label",
        "Relationship": "Checkpoint-presence proxy",
    },
    {
        "Basis / category": "TK/MUNDAT safeguard",
        "Operational interpretation": "Human review before sharing",
        "Rule ID": "TK-HUMAN-01",
        "Evidence": "human_oversight",
        "Relationship": "Use-case governance safeguard",
    },
]

st.dataframe(
    pd.DataFrame(rule_mapping),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Basis / category": st.column_config.TextColumn(width="small"),
        "Operational interpretation": st.column_config.TextColumn(width="medium"),
        "Rule ID": st.column_config.TextColumn(width="small"),
        "Evidence": st.column_config.TextColumn(width="medium"),
        "Relationship": st.column_config.TextColumn(width="medium"),
    },
)

st.caption(
    "The mappings correspond to the current taxonomy and the five entries "
    "returned by the Rego `results` rule."
)

# ---------------------------------------------------------------------
# REGO RULES
# ---------------------------------------------------------------------

st.markdown("#### Rego Rules in the Current Architecture")

rules = [
    (
        "TK-STRUCT-01 — Required intake-to-output flow",
        "Checks that the seven required TK stages exist and that the six expected "
        "connections form the documented flow.",
        "pipeline.nodes\npipeline.connections",
        "OK when the required stages and expected edges are present; otherwise FAIL.",
    ),
    (
        "TK-DATA-01 — Source provenance and approval",
        "Checks each source node for a non-empty source identifier and an approved "
        "source declaration.",
        "node.kind == \"source\"\ncompliance_extensions.source_id\ncompliance_extensions.approved_source",
        "OK when all source nodes provide both declarations; otherwise FAIL.",
    ),
    (
        "TK-TRACE-01 — Stage logging",
        "Checks whether every pipeline node declares logging capability.",
        "pipeline.nodes[*].compliance_extensions.has_logging",
        "OK when every stage declares true; otherwise FAIL.",
    ),
    (
        "TK-RISK-01 — Compliance and risk checks",
        "Checks whether the blueprint contains the dedicated "
        "`run_compliance_checks` stage.",
        "pipeline.nodes[*].label == \"run_compliance_checks\"",
        "OK when the checkpoint exists; otherwise FAIL.",
    ),
    (
        "TK-HUMAN-01 — Human review before sharing",
        "Checks the sharing-decision stage for explicit human-review evidence.",
        "prepare_sharing_decision\ncompliance_extensions.human_oversight",
        "OK when human review is explicitly represented; HUMAN when evidence is "
        "missing; FAIL when it is explicitly disabled.",
    ),
]

for title, purpose, evidence, outcome in rules:
    with st.expander(title):
        left, right = st.columns([1.4, 1])
        with left:
            st.write(purpose)
            st.code(evidence, language="text")
        with right:
            st.markdown("**Expected outcome**")
            st.write(outcome)

# ---------------------------------------------------------------------
# RESULT SEMANTICS
# ---------------------------------------------------------------------

st.markdown("#### Result Semantics")

result_columns = st.columns(3)
result_definitions = [
    (
        "🟢 OK",
        "The available blueprint evidence satisfies the encoded operational rule.",
    ),
    (
        "🔴 FAIL",
        "The available blueprint evidence violates the encoded operational rule.",
    ),
    (
        "🟠 HUMAN",
        "Evidence is missing, ambiguous, or insufficient for an automated conclusion.",
    ),
]

for column, (title, description) in zip(result_columns, result_definitions):
    with column:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(description)

# ---------------------------------------------------------------------
# AUTOMATION BOUNDARY
# ---------------------------------------------------------------------

st.markdown("#### Automation Boundary")

left, right = st.columns(2, gap="large")

with left:
    st.markdown("**The PoC can evaluate**")
    st.markdown(
        """
        - Explicit evidence against explicit conditions.
        - Required stages and connections.
        - Declared source and logging metadata.
        - Presence of a risk-check checkpoint.
        - Declared human-review evidence.
        """
    )

with right:
    st.markdown("**The PoC cannot establish**")
    st.markdown(
        """
        - The legal meaning or completeness of the interpretation.
        - Complete GDPR compliance.
        - A complete Article 30 record of processing activities.
        - A complete Article 35 DPIA or legal risk determination.
        - Runtime behaviour or the legal sufficiency of declared metadata.
        """
    )

st.warning(
    "A deterministic Rego result is valid only relative to the operational "
    "interpretation and evidence model that define the rule."
)

# ---------------------------------------------------------------------
# DESIGN PRINCIPLES
# ---------------------------------------------------------------------

with st.expander("Policy-as-Code design principles"):
    principles = [
        ("Evidence-bound", "Every automated conclusion refers to explicit blueprint evidence."),
        ("Traceable", "A result can be followed back to a requirement, rule, and evidence field."),
        ("Explainable", "Results include a reason, evidence, and remedy."),
        ("Uncertainty-aware", "Insufficient evidence is not silently treated as compliance."),
        ("Separated", "Policy evaluation is separated from application orchestration."),
        ("Design-time", "The current scope is static blueprint inspection before execution."),
    ]

    for title, description in principles:
        st.markdown(f"**{title}:** {description}")
