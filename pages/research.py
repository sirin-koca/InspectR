import streamlit as st

st.subheader("Research Problem")
st.caption("How to build compliance-aware data pipelines?")
st.markdown(
    """
    Regulatory and organisational policies are often expressed in
    qualitative, context-dependent language, while software systems require
    explicit conditions and observable evidence. This research investigates
    how selected requirements can be operationalised for design-time
    compliance assessment of data-pipeline blueprints."""
)

st.info(
    """
    - **To what extent can abstract legal requirements be translated into explicit, evidence-bound, 
    machine-assessable technical controls at design time of data pipelines?**
    - **Which regulatory compliance requirements can be inspected from static data pipeline representations
      at design time, and what are the limits of that inspection?**
    """
)



tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Research Profile",
    "Research Artifact",
    "Technical Architecture",
    "Research Questions",
    "Industrial Context",
    "Use Case"
])

def field(label, value):
    st.markdown(f"**{label}**")
    st.write(value)

with tab1:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        field("Core Domains:",
              "Systems Architecture, Software Engineering, " \
              "Compliance Automation, Policy-as-Code, AI/Data Operations")

        field("Application Domain",
              "Design-Time Compliance Validation, " \
              "AI/Data Operations, and Compliance-Aware Data Pipelines")

        field("Industrial Context",
              "SINTEF, DataPACT, inLUMEN, MUNDAT Use Case")
        
        field("Regulatory Domains",
        "GDPR, selected Articles 25, 30, and 35, EU AI Act (AIA)")

    with col2:
        field("Architectural Context",
              "Decoupled Compliance Automation and Maintenance, " \
              "Policy-as-Code (PaC) and OPA/Rego, " \
              "Evidence-Bound Design-Time Evaluation, "
              "LLM-generated data pipeline structures, "
              "Agentic workflows (potential)")

        field("Methodology",
              "Design Science Research (DSR)")

        field("Research Artifact",
              "_InspectR_ — a design-time compliance validation engine. "
              )
        field("Use Case",
        "DataPACT | Compliant, data-driven city of Trondheim (MUNDAT)"
        )
# ---------------------------------------------------------------------
# RESEARCH METHOD
# ---------------------------------------------------------------------

with tab2:
    st.write(
        "This project follows a **Design Science Research (DSR)** approach. "
        "It is used to investigate a real-world problem by designing, " \
        "implementing, and evaluating a bounded artifact. " \
        "A method for translating contextual requirements into "
        "evidence-bound, explainable design-time compliance checks "
        "over static data-pipeline blueprints."
    )

    st.subheader("InspectR")
    st.caption("Design-Time Compliance Validation Engine")
    dsr_steps = [
        ("1. Problem", "Identify the gap between contextual requirements and machine-assessable controls."),
        ("2. Objectives", "Define requirements for evidence, traceability, explainability, and uncertainty."),
        ("3. Design", "Construct the artifact, operational rules, evidence model, and result model."),
        ("4. Demonstration", "Apply the artifact to the bounded TK/MUNDAT GDPR case study."),
        ("5. Evaluation", "Assess coverage, repeatability, explainability, and limitations."),
        ("6. Knowledge", "Document design principles and conditions for transfer beyond the case."),
    ]

    for row in range(0, len(dsr_steps), 3):
        columns = st.columns(3)
        for column, (title, description) in zip(columns, dsr_steps[row : row + 3]):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.caption(description)
with tab3:
    st.subheader("Policy-as-Code Architecture")
    st.write(
        "Unified JSON pipeline blueprint evaluated directly by OPA/Rego. "
        "The blueprint combines schema, manifest and infrastructure metadata. "
        "Policy-as-Code · OPA/Rego · Static design representations"
    )

    st.subheader("Research Artifact")
    st.info("InspectR — Design-Time Compliance Validation Engine")
    st.caption("Policy engine evaluates evidence-bound rules against static pipeline blueprints")

with tab4:
    st.subheader("Industrial Context")
    st.write("SINTEF / DataPACT")
    st.write("Including inLUMEN-generated pipeline structures")

# ---------------------------------------------------------------------
# RESEARCH QUESTIONS
# ---------------------------------------------------------------------
with tab5:
    st.subheader("Research Questions")

    questions = [
        (
            "RQ1 — Requirement operationalisation",
            "How can context-dependent regulatory requirements be operationalised "
            "into machine-assessable policy specifications while preserving their "
            "meaning and scope?",
        ),
        (
            "RQ2 — Evidence and explainability",
            "What evidence model supports explainable and defensible design-time "
            "compliance assessment across heterogeneous data-pipeline representations?",
        ),
        (
            "RQ3 — Uncertainty and validity",
            "How can uncertainty and insufficient evidence be represented, and how "
            "can the validity and usefulness of automated assessment results be evaluated?",
        ),
    ]

    columns = st.columns(3)
    for column, (title, question) in zip(columns, questions):
        with column:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(question)

with tab6:
    st.subheader("Use Case")
    st.write(
        "The research artifact is applied to a bounded use case: "
        "the TK/MUNDAT data pipeline and its GDPR compliance requirements."
    )

    
# ---------------------------------------------------------------------
# METHOD AND CASE STUDY
# ---------------------------------------------------------------------

    with st.expander("How the method is investigated", expanded=False):
        left, right = st.columns(2)

        with left:
            st.markdown("**Design and development**")
            st.markdown(
                """
                1. Identify a contextual regulatory or organisational requirement.
                2. Define its operational interpretation and scope.
                3. Specify the evidence required in a static pipeline blueprint.
                4. Encode the interpretation as an explainable Policy-as-Code rule.
                """
            )

        with right:
            st.markdown("**Demonstration and evaluation**")
            st.markdown(
                """
                1. Apply the artifact to a bounded pipeline case.
                2. Inspect positive, negative, and incomplete evidence.
                3. Analyse results, explanations, repeatability, and limitations.
                """
            )

    with st.expander("Role of the TK/MUNDAT case study"):
        st.write(
            "The TK/MUNDAT data-sharing scenario is the bounded empirical case "
            "used to investigate the general research problem. The PoC uses selected "
            "GDPR Articles 25, 30, and 35 and a simplified inLUMEN pipeline blueprint."
        )
        st.caption(
            "The case study demonstrates the method; it does not define the scope "
            "of the research questions."
        )

    # ---------------------------------------------------------------------
    # CONTRIBUTION AND EVALUATION BASIS
    # ---------------------------------------------------------------------

    with st.expander("Contribution under investigation", expanded=False):
        st.write(
            "The contribution under investigation is a method for translating "
            "contextual requirements into evidence-bound, explainable design-time "
            "compliance checks over static data-pipeline blueprints."
        )
        st.caption(
            "The contribution is not Policy-as-Code or OPA itself. Those are "
            "established technologies; the thesis investigates their design and "
            "use in this evidence-bound assessment method."
        )

    with st.expander("PoC evidence and evaluation basis", expanded=False):
        st.markdown(
            """
            - **Architectural separation:** Policy is separated from application logic.
            - **Independent evaluation:** OPA evaluates Rego rules against blueprint evidence.
            - **Traceability:** Each rule exposes its interpretation, evidence, result, and remedy.
            - **Evidence sufficiency:** `PASS`, `FAIL`, and `HUMAN` distinguish a
            defined design control, a missing design control, and insufficient evidence.
            - **Reproducibility:** The same blueprint produces repeatable rule results.
            - **Limit visibility:** Missing evidence, alternative interpretations, and
            rule limitations are documented.
            """
        )

    # ---------------------------------------------------------------------
    # SCOPE AND LIMITATIONS
    # ---------------------------------------------------------------------

    with st.expander("Scope and limitations"):
        st.warning(
            """
            This PoC does not encode an entire regulation, determine legal compliance
            automatically, or validate runtime behaviour. It evaluates declared
            design-time evidence against a bounded set of operational rules. A
            successful result means that the encoded rule was satisfied by the
            available evidence; it is not proof of legal compliance as a whole.
            """
        )

    st.caption(
        "An intermediate representation may support future portability across "
        "blueprint formats, but it is outside the scope of this PoC."
    )
