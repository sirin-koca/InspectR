import streamlit as st

st.markdown("""
<style>
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 { color: #142744; }
[data-testid="stMetric"] {
    background: #f3f6fa;
    padding: 14px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.caption("INSPECTR  /  FOUNDATIONS")
st.title("Understanding Data Pipelines")
st.markdown(
    "**How data moves, how pipelines form graphs, "
    "and where compliance risks emerge.**"
)

st.info(
    "A data pipeline is a sequence of connected processing operations "
    "that collect, transform, store, and deliver data."
)

# -------------------------------------------------------
# 1. PIPELINE GRAPH
# -------------------------------------------------------

st.header("01  ·  A Data Pipeline Is a Graph")

st.write(
    "A pipeline can be represented as a **directed graph**: "
    "nodes represent processing steps, and directed edges "
    "represent data movement or dependencies between them."
)

st.graphviz_chart("""
digraph Pipeline {
    graph [
        rankdir=LR,
        bgcolor="transparent",
        pad="0.3",
        nodesep="0.45",
        ranksep="0.6"
    ];

    node [
        shape=box,
        style="rounded,filled",
        fillcolor="#EAF0F8",
        color="#B9C9DE",
        fontcolor="#142744",
        fontname="Helvetica",
        fontsize=12,
        margin="0.20,0.14"
    ];

    edge [
        color="#7086A4",
        penwidth=1.8,
        arrowsize=0.7
    ];

    A [label="Source A\\nHR records"];
    B [label="Source B\\nSurvey data"];
    C [label="Ingestion"];
    D [label="Transform"];
    E [label="Aggregate"];
    F [label="Storage"];
    G [label="Research output"];

    A -> C;
    B -> C;
    C -> D;
    D -> E;
    E -> F;
    F -> G;
}
""", use_container_width=True)

st.caption(
    "Illustrative graph inspired by the TK/MUNDAT context; "
    "not an authoritative representation of deployed infrastructure."
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown("**Nodes — what happens to data**")
    st.write(
        "Sources, ingestion, transformation, aggregation, "
        "storage, and delivery."
    )

with right:
    st.markdown("**Edges — how data moves**")
    st.write(
        "Connections describe where data flows. "
        "A node can have multiple inputs and outputs."
    )

st.write(
    "Many orchestrated pipelines are modeled as "
    "**Directed Acyclic Graphs (DAGs)**. "
    "A DAG has directed dependencies without cycles. "
    "Not every data pipeline is a DAG: streaming systems "
    "may contain continuous processing and feedback loops."
)

# -------------------------------------------------------
# 2. COMPLIANCE RISKS
# -------------------------------------------------------

st.divider()
st.header("02  ·  Where Compliance Risks Emerge")

st.write(
    "Compliance concerns extend beyond individual processing steps. "
    "They can arise from the data itself, its intended use, "
    "the connections between stages, and the infrastructure."
)

risks = [
    (
        "Personal data exposure",
        "Sensitive or identifiable information enters a pipeline "
        "without an appropriate protection strategy.",
        "Data classification and declared protection measures",
    ),
    (
        "Purpose mismatch",
        "Data collected for one purpose is routed to processing "
        "or destinations incompatible with the declared purpose.",
        "Declared purpose, sources, destinations, and permitted uses",
    ),
    (
        "Missing lineage",
        "The architecture does not adequately describe where "
        "data originates, how it is transformed, or where it goes.",
        "Source, transformation, and destination metadata",
    ),
    (
        "Inadequate security",
        "The proposed storage or transmission configuration "
        "does not satisfy an applicable security control.",
        "Encryption and infrastructure security declarations",
    ),
    (
        "Uncontrolled retention",
        "Data storage has no documented retention policy or "
        "exceeds a specifically established retention limit.",
        "Retention configuration and applicable policy threshold",
    ),
    (
        "Insufficient evidence",
        "Required compliance metadata is missing, ambiguous, "
        "or cannot be established from the blueprint.",
        "Completeness and quality of the declared evidence",
    ),
]

for title, problem, check in risks:
    with st.expander(title):
        st.markdown(f"**Risk:** {problem}")
        st.markdown(f"**Design-time check:** {check}")

st.caption(
    "These are engineering risk categories, not automatic "
    "determinations of GDPR violations."
)

# -------------------------------------------------------
# 3. THREE INPUTS
# -------------------------------------------------------

st.divider()
st.header("03  ·  What Is Needed to Check Compliance?")

st.write(
    "A compliance-aware pipeline blueprint needs information "
    "about the data, its processing workflow, and its infrastructure."
)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.subheader("1. Data Schema")
    st.caption("DATA LAYER")
    st.write("**What does the data look like?**")
    st.markdown(
        "Fields, data types, personal-data classification, "
        "and protection metadata."
    )

with c2:
    st.subheader("2. Pipeline Manifest")
    st.caption("APPLICATION LAYER")
    st.write("**How does the application move data?**")
    st.markdown(
        "Processing stages, sources, destinations, "
        "declared purposes, and dependencies."
    )

with c3:
    st.subheader("3. Infrastructure")
    st.caption("INFRASTRUCTURE LAYER")
    st.write("**Where does the data live?**")
    st.markdown(
        "Storage configuration, encryption, "
        "retention settings, and deployment properties."
    )

st.markdown("#### From three inputs to one blueprint")

st.graphviz_chart("""
digraph Blueprint {
    graph [
        rankdir=TB,
        bgcolor="transparent",
        nodesep="0.3",
        ranksep="0.5"
    ];

    node [
        shape=box,
        style="rounded,filled",
        fontname="Helvetica",
        fontsize=12,
        margin="0.2,0.14",
        color="#BCCBDD",
        fillcolor="#EAF0F8",
        fontcolor="#142744"
    ];

    schema [label="Data Schema"];
    manifest [label="Pipeline Manifest"];
    infra [label="Infrastructure / IaC"];

    blueprint [
        label="Unified Data Pipeline Blueprint\\nJSON",
        fillcolor="#D9E5F4"
    ];

    inspectr [
        label="InspectR + OPA/Rego",
        fillcolor="#142744",
        fontcolor="white",
        color="#142744"
    ];

    results [
        label="Results + Evidence\\nPASS / FAIL / HUMAN",
        fillcolor="#EAF0F8"
    ];

    schema -> blueprint;
    manifest -> blueprint;
    infra -> blueprint;
    blueprint -> inspectr;
    inspectr -> results;
}
""", use_container_width=True)

st.caption(
    "Conceptual InspectR input architecture. "
    "The three categories are an architectural decomposition, "
    "not a universally mandatory file format."
)

# -------------------------------------------------------
# 4. INTERACTIVE POLICY EXAMPLE
# -------------------------------------------------------

st.divider()
st.header("04  ·  Explore a Design-Time Compliance Check")

st.write(
    "Change the declared properties below to see how "
    "a simplified policy decision could work."
)

with st.container(border=True):
    has_sensitive_data = st.toggle(
        "Pipeline contains sensitive personal data",
        value=True,
    )

    protection = st.selectbox(
        "Declared data protection",
        ["Not specified", "None", "Anonymisation"],
    )

    encryption = st.selectbox(
        "Encryption at rest",
        ["Not specified", "Enabled", "Disabled"],
    )

    public_destination = st.checkbox(
        "Data is sent to a public destination",
        value=False,
    )

    failures = []
    missing = []

    if has_sensitive_data:
        if protection == "None":
            failures.append(
                "Sensitive data has no declared protection."
            )
        elif protection == "Not specified":
            missing.append(
                "Data protection strategy is not documented."
            )

    if encryption == "Disabled":
        failures.append(
            "Encryption at rest is explicitly disabled."
        )
    elif encryption == "Not specified":
        missing.append(
            "Encryption configuration is not documented."
        )

    if public_destination and has_sensitive_data:
        if protection == "None":
            failures.append(
                "Sensitive data is routed to a public "
                "destination without a declared protection."
            )
        elif protection == "Not specified":
            missing.append(
                "Public-release protection requires review."
            )

    if failures:
        st.error("FAIL — Declared properties violate example controls.")
        for item in failures:
            st.write(f"• {item}")
    elif missing:
        st.warning("HUMAN — Evidence is incomplete.")
    else:
        st.success("PASS — Example checks satisfied.")

    if missing:
        st.markdown("**Missing evidence**")
        for item in missing:
            st.write(f"• {item}")

st.caption(
    "Educational simulation only. This section does not call OPA "
    "or execute InspectR's actual Rego policies. "
    "Anonymisation is a design declaration here, not runtime evidence."
)

# -------------------------------------------------------
# 5. TK / MUNDAT RELEVANCE
# -------------------------------------------------------

st.divider()
st.header("05  ·  Connection to TK / MUNDAT")

st.write(
    "The GRC ENGINEERING document proposes mapping "
    "MUNDAT requirements to design-time policy checks."
)

st.dataframe(
    [
        {
            "Reference": "TK.FR.10",
            "Concern": "PII identification and tagging",
            "Example check": "Personal data lacks declared protection",
        },
        {
            "Reference": "TK.FR.08",
            "Concern": "Pipeline design and metadata",
            "Example check": "Sensitive data routed to an unsafe destination",
        },
        {
            "Reference": "TK.NFR.01",
            "Concern": "Encryption and security",
            "Example check": "Encryption disabled",
        },
    ],
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "Mappings above are drawn from GRC ENGINEERING. "
    "They are proposed design-time checks, not legal conclusions "
    "or proof of actual MUNDAT configurations."
)

st.divider()
st.markdown(
    "**InspectR's role:** evaluate declared pipeline architecture "
    "properties before deployment and return structured decisions "
    "with reasons and evidence. It does not execute the pipeline "
    "or certify real-world legal compliance."
)
