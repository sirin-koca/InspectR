import json
import subprocess

import streamlit as st

from src import evaluator
from src.catalog import ACCEPTANCE, DEFECTS, OPEN_QUESTIONS, RULES
from src.evaluator import evaluate
from src.scenarios import SCENARIOS, build
from src.ui import badge, page_header, table

page_header(
    "Validation",
    "How do we know the results are correct, and where are the limits?",
)

# ---------------------------------------------------------------- scenario matrix
st.subheader("Scenario matrix")
st.markdown(
    "Each scenario changes **one fact** in the enriched blueprint (details on "
    "the Inspect page). The expected status follows from the decision table; "
    "the observed status is computed live by OPA."
)


@st.cache_data(show_spinner="Evaluating all scenarios with OPA...")
def run_matrix() -> list[dict]:
    rows = []
    for key, label, change, _, expected in SCENARIOS:
        observed = {r["rule"]: r["status"] for r in evaluate(build(key))}
        row = {"Scenario": label}
        for rule in RULES:
            rid = rule["id"]
            mark = "✓" if observed.get(rid) == expected[rid] else f"✗ expected {expected[rid]}"
            row[rid] = f"{badge(observed.get(rid, 'ERROR'))} {mark}"
        rows.append(row)
    return rows


try:
    matrix = run_matrix()
    table(matrix)
    matched = sum(cell.endswith("✓") for row in matrix for cell in (row[r["id"]] for r in RULES))
    total = len(matrix) * len(RULES)
    st.caption(f"{matched}/{total} results match the expected status.")
except RuntimeError as error:
    st.error(f"OPA is not available: {error}")


st.subheader("What iteration 1 revealed")
st.markdown(
    "Testing the first rule set (six rules, three statuses) against controlled "
    "changes exposed five defects. Each one either hid findings or produced a "
    "confident wrong verdict. They motivated the six-status model."
)
table(DEFECTS, columns=["ID", "Defect in v1", "Observed effect", "Fix in v2"])

# ---------------------------------------------------------------- acceptance
st.subheader("Acceptance criteria")
table(
    [{"ID": i, "Criterion": c, "Status": s, "Note": n} for i, c, s, n in ACCEPTANCE],
)
st.caption("From the Scope and Evaluation Proposal (30 October 2026).")

# ---------------------------------------------------------------- limits
st.subheader("Limits of validity")
for text in [
    "**PASS is a design-level statement.** It means the blueprint declares the control, not that the pipeline is compliant or that the control works at runtime.",
    "**Rules are interpretations.** They operationalise TK requirements; they are not validated legal mappings until a domain expert reviews them (AC7).",
    "**Evidence is declared, not verified.** Every non-structural fact in V2 was added by hand.",
    "**Raw inLUMEN exports are read literally.** They use `kind`, not `type`, so TK-R2 and TK-R3 return NOT_APPLICABLE on them; an adapter (RQ2) is needed.",
]:
    st.markdown(f"- {text}")

# ---------------------------------------------------------------- questions
st.subheader("Open questions for SINTEF")
for i, question in enumerate(OPEN_QUESTIONS, 1):
    st.markdown(f"{i}. {question}")
