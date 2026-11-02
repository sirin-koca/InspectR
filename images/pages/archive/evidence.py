import pandas as pd
import streamlit as st

from src.catalog import RULES, STATUS_ICON


st.subheader("Evidence Traceability")
st.caption(
    "Each active rule identifies the blueprint evidence it reads and the "
    "design-time conclusion it is allowed to make."
)

st.info(
    """
    **Input evidence** is read from the uploaded JSON blueprint. **Derived
    evidence** is calculated by Rego from that input. A fact is **undetermined**
    when the field is absent, null, or not a boolean; it then yields UNKNOWN,
    never PASS. A result confirms only that the planned design declares the
    encoded control; it is not evidence that the design has been implemented
    or a legal determination.
    """
)


def render_rule_table(rows: list[dict]) -> None:
    st.table(
        pd.DataFrame(rows, columns=["Traceability item", "Definition"])
        .set_index("Traceability item")
    )


for rule in RULES:
    st.markdown(f"#### {rule['id']} — {rule['title']}")
    st.caption(
        f"{rule['legal_reference']} · Evidence class: {rule['evidence_class']} · "
        f"Replaces {rule['replaces']}"
    )
    rows = [
        ("Trigger", rule["trigger"]),
        ("Control", rule["control"]),
        ("Input selectors", "; ".join(rule["selectors"])),
        *[(f"{STATUS_ICON[status]} {status}", text) for status, text in rule["outcomes"].items()],
        (f"{STATUS_ICON['ERROR']} ERROR", "InspectR could not evaluate the rule (technical fault)."),
        ("Boundary", rule["boundary"]),
    ]
    render_rule_table(
        [{"Traceability item": item, "Definition": definition} for item, definition in rows]
    )
