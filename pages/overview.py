import streamlit as st

from src.catalog import RULES, STATUS_MODEL
from src.research_content import MAIN_RQ
from src.scenarios import SCENARIOS

# ---------------------------------------------------------------- hero
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">MSc thesis · University of Oslo · DataPACT / SINTEF</div>
      <div class="hero-title">InspectR</div>
      <div class="hero-lead">Checks a <b>planned</b> data pipeline against compliance rules
      <b>before it is built</b>, and returns one traceable result per rule.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- how it works
st.subheader("How it works")
st.graphviz_chart(
    """
    digraph {
        rankdir=LR; bgcolor="transparent"; nodesep=0.3;
        node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=11
              fillcolor="#EEF2F8" color="#8A9BB5" margin="0.15,0.08"];
        edge [color="#8A9BB5"];
        bp  [label="Pipeline blueprint\\nJSON from the design tool"];
        req [label="Requirement\\nGDPR, organisation"];
        rule [label="Rule in Rego\\nIF trigger THEN control"];
        opa [label="OPA\\npolicy engine" fillcolor="#142744" fontcolor="white" color="#142744"];
        res [label="Result per rule\\nstatus · reason\\nevidence · remedy"];
        req -> rule -> opa; bp -> opa; opa -> res;
    }
    """,
    use_container_width=True,
)

# ---------------------------------------------------------------- statuses
st.markdown("**Six possible statuses per rule.** Missing evidence never gives PASS.")
chips = "".join(
    f'<span class="chip" title="{meaning}">{icon} {status.replace("_", " ")}</span>'
    for status, icon, meaning, _ in STATUS_MODEL
)
st.markdown(f'<div class="chips">{chips}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- why
st.subheader("Why")
for column, (title, text) in zip(
    st.columns(3),
    [
        ("Checking happens too late",
         "Showing that a pipeline meets its obligations still relies on manually "
         "gathered evidence. Automated checking of the design is lacking."),
        ("Policy-as-Code targets infrastructure",
         "Rule engines such as OPA check cloud and Kubernetes settings, "
         "not legal obligations on data-pipeline designs."),
        ("Designs lack the evidence",
         "Pipeline design tools export structure, not compliance facts "
         "such as special-category data or DPIA checkpoints."),
    ],
):
    with column.container(border=True):
        st.markdown(f"**{title}**")
        st.caption(text)
st.caption("Sources and gap analysis: see Research.")

# ---------------------------------------------------------------- RQ + status
st.subheader("Research question")
st.info(MAIN_RQ)

st.subheader("Current state (iteration 1)")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Use case", "TK / MUNDAT", help="Trondheim Kommune, municipal data sharing (DataPACT)")
c2.metric("Rules", len(RULES), help=", ".join(r["id"] for r in RULES))
c3.metric("Test scenarios", len(SCENARIOS), help="S0–S6, each one controlled change")
c4.metric("Automated tests", "29 + 20", help="29 Rego unit tests, 20 integration tests")
left, right = st.columns(2, gap="large")
with left:
    st.markdown("**In scope**")
    st.caption(
        "Design-time inspection of planned pipelines · evidence model · explicit "
        "result semantics for missing evidence · rules as interpretations, reviewed by experts"
    )
with right:
    st.markdown("**Out of scope**")
    st.caption(
        "Run-time monitoring · automated reading of legal text · proof of legal "
        "compliance or certification"
    )

# ---------------------------------------------------------------- navigation
st.subheader("Explore")
PAGES = [
    ("pages/research.py", "Research", "Related work, gaps, questions, candidate contributions"),
    ("pages/method.py", "Method", "From requirement to rule to result"),
    ("pages/case.py", "Case: TK / MUNDAT", "The pipeline, its evidence and the rules"),
    ("pages/inspection.py", "Inspect", "Run InspectR on a scenario or own blueprint"),
    ("pages/validation.py", "Validation", "Scenario matrix, tests, defects, limits"),
]
for column, (path, title, text) in zip(st.columns(len(PAGES)), PAGES):
    with column.container(border=True):
        st.page_link(path, label=f"**{title}**")
        st.caption(text)
