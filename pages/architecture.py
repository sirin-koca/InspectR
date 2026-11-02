import streamlit as st

st.warning(
    "The current PoC evaluates the unified JSON blueprint directly; no separate "
    "intermediate representation is built."
)

st.image(
    "images/arch-inspectr.jpeg",
    caption="InspectR Architecture Overview",
)

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(
    """
    ### Why this architecture?

    1. **Blueprint** - a unified JSON design assembled from data schema, pipeline manifest, and infrastructure/IaC metadata.
    2. **Policy** - the operational interpretation encoded in Rego.
    3. **Decision engine** - InspectR utilizing OPA evaluates the policy independently from the application logic.
    4. **Evaluation** - InspectR reports the decision and evidence to the user - optionally triggers the agentic work-flow for self-correction.

    - **Design-time inspection**: The blueprint describes planned controls and checkpoints before deployment; it is not runtime evidence.
    - **Shift-Left Compliance**: Catching non-compliance at design-time (CI/CD / pull request phase) prevents 
    costly runtime compliance failures and data contamination. 
    - **Status model (PASS / FAIL / UNKNOWN / HUMAN / NOT_APPLICABLE, plus ERROR)**: Standard linters offer
    binary true/false decisions. Real-world compliance must also separate undetermined evidence (UNKNOWN),
    legal judgement (HUMAN), and rules that do not apply (NOT_APPLICABLE). ERROR marks a fault in InspectR,
    not a finding about the blueprint. 
    """
)

with col2:
    st.code(
            """
            LAW
            1. GDPR provision: Use Case TK 
            2. AIA: Use Case X 
            ↓
            Policy (Organisational requirements)
            ↓
            Observable evidence in the blueprint
            ↓
            Executable PaC rule
            ↓
            Evaluation: InspectR Engine
            ↓
            PASS / FAIL / UNKNOWN / HUMAN / NOT_APPLICABLE
            (ERROR = InspectR fault)
            """,
            language="text",                    
)  