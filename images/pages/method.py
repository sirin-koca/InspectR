import streamlit as st

from src.catalog import RULES, STATUS_MODEL
from src.ui import badge, page_header, table

page_header(
    "Method",
    "How does a written requirement become a machine-checkable verdict?",
)

# ---------------------------------------------------------------- chain
st.subheader("From requirement to verdict")
for column, (step, text) in zip(
    st.columns(5),
    [
        ("1 · Requirement", "What the TK documents and the law demand, in words."),
        ("2 · Rule", "The requirement scoped as IF trigger THEN control."),
        ("3 · Facts", "The blueprint fields the rule reads: true, false or undetermined."),
        ("4 · Evaluation", "OPA applies the rule's decision table to the facts."),
        ("5 · Result", "One status, with reason, evidence and remedy."),
    ],
):
    with column.container(border=True):
        st.markdown(f"**{step}**")
        st.caption(text)

# ---------------------------------------------------------------- logic
st.subheader("Decision logic")
st.markdown(
    "Every rule has the same shape. A fact the rule needs is **undetermined** "
    "when the blueprint gives no usable evidence for it (absent, null, or not "
    "a boolean). An undetermined fact never produces PASS."
)
table(
    [
        ("undetermined", "any", badge("UNKNOWN")),
        ("false", "any", badge("NOT_APPLICABLE")),
        ("true", "false", badge("FAIL")),
        ("true", "undetermined", badge("UNKNOWN")),
        ("true", "true", f"{badge('PASS')}  ({badge('HUMAN')} for judgement rules)"),
    ],
    columns=["Trigger", "Control", "Status"],
)
st.caption(f"{badge('ERROR')} sits outside the table: InspectR failed, not the blueprint.")
table(
[{"Status": badge(s), "Meaning": m, "Who acts next": a} for s, _, m, a in STATUS_MODEL],
)

# ---------------------------------------------------------------- worked example
st.subheader("Worked example: TK-R1")
r1 = RULES[0]
steps = st.tabs(["1 · Requirement", "2 · Rule", "3 · Rego", "4 · Facts in V2", "5 · Result"])
with steps[0]:
    st.markdown(f"**TK need ({r1['tk_requirement'][0]}):** “{r1['tk_requirement'][1]}”")
    st.caption(f"Legal basis: {r1['legal_reference']}")
with steps[1]:
    st.markdown(f"**IF** {r1['trigger']}  \n**THEN** {r1['control']}")
    st.caption(
        "Scoping decisions: special-category data (Art. 9) is the trigger; the DPIA "
        "and risk assessment are merged because they share trigger, gate and article."
    )
with steps[2]:
    st.code(
        """trigger_true if {
    some s in sources
    lib.is_true(s, "contains_special_category_data")
}

passing_gate_ids := [g.id |
    some g in relevant_gates
    every f in control_fields { lib.is_true(g, f) }
]

result := report("UNKNOWN", 1, ...) if { trigger_unknown }
     else := report("NOT_APPLICABLE", 2, ...) if { trigger_false }
     else := report("FAIL", 3, ...) if { trigger_true; count(gates) == 0 }
     else := report("FAIL", 4, ...) if { trigger_true; control_false }
     else := report("PASS", 5, ...) if { trigger_true; count(passing_gate_ids) > 0 }
     else := report("UNKNOWN", 6, ...) if { trigger_true }

default result := { ..."status": "ERROR"... }   # row 7, unreachable by design""",
        language="text",
    )
    st.caption("Excerpt of policies/tk/TK-R1.rego. Rows are evaluated top to bottom; the first match wins.")
with steps[3]:
    table(
        [
            ("health_services", "contains_special_category_data", "true", "Trigger"),
            ("citizen_registry", "contains_special_category_data", "false", "Trigger"),
            ("dpia_check", "dpia_checkpoint_defined", "true", "Control"),
            ("dpia_check", "risk_assessment_checkpoint_defined", "true", "Control"),
        ],
        columns=["Node", "Field", "Value", "Role"],
    )
    st.caption("These fields were added to the blueprint manually; inLUMEN does not export them (see Case).")
with steps[4]:
    st.success(
        "**🟢 PASS · decision-table row 5.** Special-category data is processed and gate "
        "'dpia_check' declares both a DPIA and a risk-assessment checkpoint."
    )
    st.caption("PASS means the design declares the control, not that the pipeline is compliant.")

# ---------------------------------------------------------------- reference
with st.expander("Definitions"):
    table(
        [
            ("Requirement", "What the law or the organisation demands, in words."),
            ("Obligation", "What the requirement demands once triggered."),
            ("Rule", "A requirement written as IF trigger THEN control."),
            ("Trigger", "The fact that makes the obligation apply."),
            ("Control", "The safeguard in the design that meets the obligation."),
            ("Fact", "A typed blueprint field a rule reads: true, false or undetermined."),
            ("Undetermined", "No usable evidence for a fact: absent, null, or wrong type."),
            ("Evidence", "The blueprint field read, its observed value and its expected value."),
            ("Machine-checkable", "Expressed as a typed field the engine can read without a human."),
            ("Status", "The outcome of one rule for one blueprint."),
            ("Result", "Status plus reason, evidence, legal reference and remedy."),
            ("Design-time", "Checked on the blueprint before the pipeline is built or run."),
            ("Fail-closed", "Undetermined evidence never becomes PASS."),
        ],
        columns=["Term", "Definition"],
    )

with st.expander("Design decisions and justification"):
    table(
        [
            ("Rule = IF trigger THEN control", "Legal obligations are conditional.", "Compliance-by-design (Governatori; LegalRuleML)"),
            ("Three fact values", "Forcing an undetermined fact into true or false invents information.", "Three-valued logic"),
            ("Undetermined → UNKNOWN, never PASS", "A false PASS hides a risk.", "Fail-closed principle"),
            ("NOT_APPLICABLE as own status", "'Does not apply' differs from 'satisfied'.", "AWS Config; SARIF"),
            ("HUMAN as own status", "Some requirements are legal judgements.", "SARIF 'review'"),
            ("ERROR separate from verdicts", "A tool failure says nothing about the blueprint.", "Kyverno 'error'"),
            ("Evidence in every result", "A verdict without evidence cannot be audited.", "GDPR Art. 5(2)"),
            ("Each rule evaluated in isolation", "One fault must not suppress other results.", "Fault isolation"),
            ("Each rule a complete decision table", "Every input reaches exactly one status; one test per row.", "Decision-table testing"),
        ],
        columns=["Decision", "Justification", "Grounding"],
    )
