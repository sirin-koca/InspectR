import json
from pathlib import Path

import streamlit as st

from src.catalog import DROPPED_RULES, RULE_FACTS, RULES
from src.ui import page_header, table

page_header(
    "Case: TK / MUNDAT",
    "Which pipeline is inspected, and what evidence does its blueprint provide?",
)

st.markdown(
    "Trondheim Kommune (TK) receives requests from researchers and companies for "
    "municipal data. The **Sickleave** scenario assembles a research dataset from "
    "health-services and citizen-registry sources, integrates and anonymises it, "
    "and shares it with an external recipient. It involves special-category "
    "health data, integration of sources, and sharing for a new purpose."
)

V2 = json.loads(Path("data/tk_mundat_data_sharing_v2.json").read_text(encoding="utf-8"))
RAW = json.loads(Path("tk-uc/inlumen-tk-uc.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- pipeline
st.subheader("Pipeline design (enriched blueprint V2)")
FILL = {
    "compliance_gate": "#FFE3B3",
    "data_source": "#D9E5F4",
    "data_integration": "#D9E5F4",
    "data_transfer": "#F6D5D5",
}
RULE_OF = {"compliance_gate": "TK-R1 · TK-R3", "data_integration": "TK-R2", "data_transfer": "TK-R3", "data_source": "TK-R1 · TK-R3"}
nodes = "\n".join(
    f'"{n["id"]}" [label="{n["id"]}\\n({n["type"]})'
    + (f'\\n{RULE_OF[n["type"]]}' if n["type"] in RULE_OF else "")
    + f'" fillcolor="{FILL.get(n["type"], "#F2F2F2")}"];'
    for n in V2["pipeline"]["nodes"]
)
edges = "\n".join(
    f'"{c["from"]}" -> "{c["to"]}" [style={"dashed" if c["flow_type"] in ("metadata", "authorisation") else "solid"}];'
    for c in V2["pipeline"]["connections"]
)
st.graphviz_chart(
    f"""digraph {{
        rankdir=LR; bgcolor="transparent";
        node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=10 color="#8A9BB5"];
        edge [color="#8A9BB5" arrowsize=0.6];
        {nodes}
        {edges}
    }}""",
    use_container_width=True,
)
st.caption(
    "Coloured nodes are the ones the rules read. Dashed edges are metadata or "
    "authorisation flows; solid edges are control and data flows."
)

# ---------------------------------------------------------------- native vs enriched
st.subheader("Native export vs. enriched blueprint")
left, right = st.columns(2, gap="large")
with left.container(border=True):
    st.markdown("**Raw inLUMEN export**")
    st.write(
        f"{len(RAW['pipeline']['nodes'])} nodes with generic kinds "
        f"({', '.join(sorted({n['kind'] for n in RAW['pipeline']['nodes']}))}). "
        "Every `parameters` field is empty. None of the facts the rules need is present."
    )
with right.container(border=True):
    st.markdown("**Enriched blueprint (V2)**")
    st.write(
        f"{len(V2['pipeline']['nodes'])} typed nodes and "
        f"{len(V2['pipeline']['connections'])} connections. Compliance facts were "
        "added **manually** so the rules have evidence to read."
    )
st.markdown(
    "The enrichment is a research finding, not a workaround: it measures the gap "
    "between what pipeline tooling exports and what inspection needs (RQ1)."
)
table(
    [{"Rule": r, "Fact": f, "Role": role, "Provenance": p} for r, f, role, p in RULE_FACTS],
)
st.caption(
    "Provenance: S = structural (from the pipeline graph), D = derivable from "
    "tooling, M = manual declaration, H = human judgement. Today every non-structural "
    "fact is M or H."
)

# ---------------------------------------------------------------- rule set
st.subheader("Rule set")
table(
    [
        {
            "Rule": r["id"],
            "Title": r["title"],
            "TK requirement": r["tk_requirement"][0],
            "Legal basis": r["legal_reference"],
            "Evidence class": r["evidence_class"],
            "Statuses": ", ".join(r["outcomes"]),
        }
        for r in RULES
    ]
)
st.caption(
    "Three rules, one per evidence class (declared, derivable, judgement): together "
    "they exercise every status and can be tested exhaustively."
)
with st.expander("Rules dropped from iteration 1"):
    table(DROPPED_RULES, columns=["Rule", "Requirement", "Reason"])
