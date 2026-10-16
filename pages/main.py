import streamlit as st

st.title("InspectR")
st.popover(
    "PoC",
).markdown(
"This app is a PoC (proof-of-concept) version of InspectR - a compliance automation engine. " \
"It deliberately implements only a small, concrete subset of the " \
" regulation relevant to the TK use case (TK UC). "
"**The current PoC evaluates the unified JSON blueprint directly; it does not "
"build a separate intermediate representation.**"
)

# --------------------------------------------------
# OVERVIEW
# What is InspectR?
# Why is it needed?
# What is the TK case?
# How does the architecture work?
# What rules are active?
# Can it run?
# What is the research contribution?
# --------------------------------------------------

st.subheader("A Framework for Compliance Automation")
st.divider()

col1, col2, col3, col4, col5= st.columns(5)

with col1:
    st.markdown("##### 1️⃣Regulatory Domain" \
    "\n This PoC uses a small subset of GDPR Articles as the regulatory " \
    "domain for the TK Use Case.")
    st.info(
    """
- **[GDPR Art. 25](https://gdpr-info.eu/art-25-gdpr/) - Privacy by Design: \n Pipeline Schema & Topography** 
- **[GDPR Art. 30](https://gdpr-info.eu/art-30-gdpr/) - RoPA: \n Metadata & Lineage Definitions**
- **[GDPR Art. 35](https://gdpr-info.eu/art-35-gdpr/) - DPIA: \n Risk-Assessment Checkpoint**

    - What documentation is required
    - personal data protection
    - secure access and sharing
    - provenance and traceability
    - only retrieving necessary data
    - identifying and approving data sources
    - logging pipeline activity
    - requiring human review before sharing
    """
) 

with col2:
    st.markdown("##### 2️⃣ Policy / The Semantic Gap")
    st.markdown(
    """
    Legal texts are human-centric, and vague.
    Modern pipelines are continuous and automated.
    """
    )
    st.info("""
    - How do we go **from fuzzy legal texts to deterministic software logic**?
    - How do we bridge the **"Semantic Gap"** at design-time before deployment?
    - **The answer is not implementing the entire law directly but implementing a relevant subset 
    in the context of the organisation and its processes.** 
    """
    )

with col3:
    st.markdown("##### 3️⃣ The Artifact: InspectR")
    st.markdown(
    """
    **Data Schema + Pipeline Manifest + Infrastructure/IaC → Unified JSON Blueprint → OPA/Rego Engine**
    """
    )
    st.info(
    """ 
    - Blueprint + policy -> decision\n\n
    - PASS/FAIL/HUMAN output with evidence, reason, and remedy.
    - OPA engine independently evaluates the static blueprint against Rego conditions.
    """
    )    

with col4:
    st.markdown("##### 4️⃣Research (RQs)")
    st.markdown("How can compliance requirements be **inspected at design-time** from static data-pipeline blueprints?")
    st.info(
    """
    - **RQ1 — Design-Time Inference:** What compliance-relevant properties can be reliably inferred from a static data-pipeline representation before execution?

    - **RQ2 — Requirement Operationalisation:** How can contextual regulatory and organisational requirements be operationalised as explainable, evidence-bound Policy-as-Code rules?

    - **RQ3 — Assessment Boundaries:** Under what conditions can static compliance assessment distinguish satisfied, violated, and indeterminate requirements, and what limitations follow?
    """
    ) 

with col5:
    st.markdown("##### 5️⃣Evaluation")
    st.markdown("Evaluating the **limits, expressiveness, and accuracy** of this architectural transformation")
    st.info(
    """
    - **Coverage** — % of legal rules that are statically checkable
    - **Evidence sufficiency** — availability and completeness of required blueprint evidence
    - **Explainability** — traceability from requirement to rule, evidence, result, and remedy
    - **Tri-state behaviour** — `PASS / FAIL / HUMAN` classifications and documented limits"""
    )
st.divider()