import streamlit as st

from src.catalog import RULE_SET_VERSION, RULES, STATUSES
from src.ui import page_header, table

page_header(
    "InspectR",
    "Design-time compliance inspection of data-pipeline blueprints · "
    "MSc thesis, University of Oslo · SINTEF / DataPACT",
)

st.markdown(
    "InspectR checks a **planned** data pipeline against compliance rules "
    "**before it is built**. It reads a machine-readable pipeline blueprint, "
    "evaluates Policy-as-Code rules with Open Policy Agent (OPA), and returns "
    "one traceable result per rule: status, reason, evidence and remedy."
)

# ---------------------------------------------------------------- problem
st.subheader("Problem")
left, mid, right = st.columns(3)
with left.container(border=True):
    st.markdown("**Missing tooling**")
    st.write(
        "Design-time privacy compliance has been studied with models "
        "([Torre et al.](https://link.springer.com/article/10.1007/s10270-021-00935-5); "
        "[Pandit et al.](https://link.springer.com/chapter/10.1007/978-3-030-33220-4_2)), "
        "but automated, tool-supported checking integrated into design "
        "environments is still lacking "
        "([SLR on GDPR modelling](https://arxiv.org/html/2604.16361))."
    )
with mid.container(border=True):
    st.markdown("**Different target for Policy-as-Code**")
    st.write(
        "Policy-as-Code with OPA mostly targets infrastructure, CI/CD and "
        "Kubernetes configurations "
        "([MDPI Computers, 2026](https://www.mdpi.com/2073-431X/15/7/453)), "
        "not data or AI pipeline designs."
    )
with right.container(border=True):
    st.markdown("**Missing evidence in the blueprint**")
    st.write(
        "inLUMEN exports pipeline structure but no compliance evidence "
        "(personal-data flags, DPIA status, approvals). The PoC therefore "
        "uses a manually enriched blueprint."
    )

# ---------------------------------------------------------------- RQs
st.subheader("Research questions")
st.markdown(
    "**Main RQ.** How can a design-time policy engine be architected to inspect "
    "compliance properties of data/AI pipeline blueprints in a way that is "
    "traceable, reliable and independent of the use case and pipeline tool?"
)
for column, (title, text) in zip(
    st.columns(3),
    [
        ("RQ1 · Evidence model",
         "What compliance-relevant information must a blueprint contain for "
         "policy-based inspection, and how much can pipeline tooling derive "
         "versus manual annotation?"),
        ("RQ2 · Architecture",
         "Which architectural design supports reuse across use cases and "
         "blueprint formats (intermediate representation with adapters, "
         "policy packs, explicit result semantics)?"),
        ("RQ3 · Evaluation",
         "How reliable, explainable and efficient are InspectR's findings "
         "compared with manual expert review, across DataPACT use cases?"),
    ],
):
    with column.container(border=True):
        st.markdown(f"**{title}**")
        st.write(text)

# ---------------------------------------------------------------- artefact
st.subheader("Artefact (iteration 1)")
st.graphviz_chart(
    """
    digraph {
        rankdir=LR; bgcolor="transparent";
        node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=11 fillcolor="#EEF2F8" color="#8A9BB5"];
        edge [color="#8A9BB5"];
        req [label="TK requirement\\n(text)"];
        rule [label="Rego rule\\nIF trigger THEN control"];
        bp [label="Pipeline blueprint\\n(JSON facts)"];
        opa [label="OPA\\nevaluation" fillcolor="#142744" fontcolor="white" color="#142744"];
        res [label="Result per rule\\nstatus · reason\\nevidence · remedy"];
        req -> rule -> opa; bp -> opa; opa -> res;
    }
    """,
    use_container_width=True,
)
c1, c2, c3 = st.columns(3)
c1.metric("Rules", len(RULES), help=f"Rule set {RULE_SET_VERSION}")
c2.metric("Statuses", len(STATUSES), help=", ".join(STATUSES))
c3.metric("Use cases", 1, help="TK/MUNDAT (Trondheim Kommune)")

# ---------------------------------------------------------------- method + scope
st.subheader("Method and scope")
st.markdown(
    "Design Science Research ([Hevner et al., 2004](https://aisel.aisnet.org/misq/vol28/iss1/6/)) "
    "with two to three build–evaluate iterations. This PoC is **iteration 1**: "
    "one use case, three rules, the blueprint evaluated directly (no "
    "intermediate representation yet)."
)
table(
    [
        ("Design-time inspection of planned pipelines", "Runtime monitoring and enforcement"),
        ("Evidence model and (planned) intermediate representation", "Automated interpretation of legal text"),
        ("Rules as organisational interpretations, validated by domain experts", "Proof of legal compliance or certification"),
        ("Explicit result semantics for undetermined evidence", "Broad AI Act coverage"),
    ],
    columns=["In scope", "Out of scope"],
)
st.caption(
    "Contribution: an architecture, an evidence model and an evaluated artefact. "
    "Not a contribution: legal interpretation, Policy-as-Code or OPA themselves."
)
