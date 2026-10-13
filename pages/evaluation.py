import hashlib
import json

import pandas as pd
import streamlit as st

from src.evaluator import evaluate


RULE_ORDER = [
    "TK-STRUCT-01",
    "TK-DATA-01",
    "TK-TRACE-01",
    "TK-RISK-01",
    "TK-HUMAN-01",
]


def status_counts(results: list[dict]) -> str:
    counts = {status: 0 for status in ("OK", "FAIL", "HUMAN")}
    for result in results:
        counts[result["status"]] += 1
    return " · ".join(f"{status}: {counts[status]}" for status in counts)


def status_message(status: str) -> str:
    return {
        "OK": "🟢 OK",
        "FAIL": "🔴 FAIL",
        "HUMAN": "🟠 HUMAN",
    }.get(status, f"⚪ {status}")


def render_evidence(evidence: dict) -> None:
    input_evidence = evidence.get("input_evidence", [])
    if input_evidence:
        st.write("**Input evidence from the uploaded blueprint**")
        rows = []
        for item in input_evidence:
            if "fields" in item:
                for field in item["fields"]:
                    rows.append(
                        {
                            "Node": f"{item.get('node_label', '')} "
                            f"(id={item.get('node_id', '')})",
                            "Blueprint selector": field.get("selector"),
                            "Observed": field.get("observed"),
                            "Expected": field.get("expected"),
                            "Condition": field.get("condition"),
                        }
                    )
            else:
                rows.append(
                    {
                        "Node": "",
                        "Blueprint selector": item.get("selector"),
                        "Observed": item.get("observed"),
                        "Expected": item.get("expected"),
                        "Condition": item.get("condition"),
                    }
                )
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

    derived_evidence = evidence.get("derived_evidence")
    if derived_evidence:
        st.write("**Derived evidence calculated by Rego**")
        st.json(derived_evidence)


def render_results(results: list[dict]) -> None:
    st.caption(status_counts(results))
    for result in results:
        with st.expander(
            f"{status_message(result['status'])} — {result['rule']}"
        ):
            st.write(f"**Legal reference:** {result['legal_reference']}")
            st.write(result["reason"])
            st.write("**Evidence**")
            render_evidence(result["evidence"])
            if result["remedy"]:
                st.write("**Remedy**")
                st.write(result["remedy"])


def load_uploaded_blueprint(uploaded_file) -> dict:
    try:
        raw_json = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(
            f"{uploaded_file.name} is not valid UTF-8 JSON."
        ) from error

    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{uploaded_file.name} is not valid JSON: {error.msg}."
        ) from error


def uploaded_file_signature(uploaded_file) -> str:
    return hashlib.sha256(uploaded_file.getvalue()).hexdigest()


st.subheader("Evaluation")
st.caption(
    "Upload two static JSON pipeline blueprints and evaluate them independently "
    "with the same InspectR Policy-as-Code rules in realtime."
)

col1, col2 = st.columns([1, 1])
with col1:
    st.info(
    """
    **How the experiment works?**

    1. Upload the first JSON blueprint and run InspectR.
    2. Upload the second JSON blueprint and run InspectR.
    3. Inspect the two independent result sets side by side.
    4. Compare results only after both live evaluations have completed.
"""
)

with col2:
    st.warning(
    """
    **Important note**
    The evidence displayed by InspectR is generated during evaluation. 
    Some evidence comes directly from fields in the uploaded blueprint, 
    while other evidence is derived by the Rego policy when it inspects those fields.

    - Input evidence: The actual field read from the uploaded JSON.
    - Derived evidence: The conclusion or summary calculated by Rego.
    - Evidence location: The JSON path and node to which the evidence belongs.
    - Policy location: The rule and condition that evaluated it.
   """
)

st.markdown("#### UPLOAD - EVALUATE - COMPARE")
left, right = st.columns(2)

with left:
    st.markdown("**Blueprint 1**")
    first_file = st.file_uploader(
        "Upload the first JSON blueprint",
        type=["json"],
        key="comparison_blueprint_1",
    )
    if first_file is not None:
        first_signature = uploaded_file_signature(first_file)
        if st.session_state.get("comparison_signature_1") not in (
            None,
            first_signature,
        ):
            st.session_state.pop("comparison_results_1", None)
            st.session_state.pop("comparison_name_1", None)
        st.caption(first_file.name)
        with st.expander("Preview uploaded JSON"):
            try:
                st.json(load_uploaded_blueprint(first_file))
            except ValueError as error:
                st.error(str(error))
        if st.button(
            "Run InspectR on blueprint 1",
            type="primary",
            use_container_width=True,
            key="evaluate_comparison_blueprint_1",
        ):
            try:
                blueprint = load_uploaded_blueprint(first_file)
                with st.spinner("Evaluating blueprint 1 with InspectR..."):
                    st.session_state["comparison_results_1"] = evaluate(blueprint)
                st.session_state["comparison_name_1"] = first_file.name
                st.session_state["comparison_signature_1"] = first_signature
                st.success("Blueprint 1 evaluation complete.")
            except (RuntimeError, ValueError) as error:
                st.session_state.pop("comparison_results_1", None)
                st.error(f"Blueprint 1 evaluation failed: {error}")
    else:
        st.session_state.pop("comparison_results_1", None)
        st.session_state.pop("comparison_name_1", None)
        st.session_state.pop("comparison_signature_1", None)

with right:
    st.markdown("**Blueprint 2**")
    second_file = st.file_uploader(
        "Upload the second JSON blueprint",
        type=["json"],
        key="comparison_blueprint_2",
    )
    if second_file is not None:
        second_signature = uploaded_file_signature(second_file)
        if st.session_state.get("comparison_signature_2") not in (
            None,
            second_signature,
        ):
            st.session_state.pop("comparison_results_2", None)
            st.session_state.pop("comparison_name_2", None)
        st.caption(second_file.name)
        with st.expander("Preview uploaded JSON"):
            try:
                st.json(load_uploaded_blueprint(second_file))
            except ValueError as error:
                st.error(str(error))
        if st.button(
            "Run InspectR on blueprint 2",
            type="primary",
            use_container_width=True,
            key="evaluate_comparison_blueprint_2",
        ):
            try:
                blueprint = load_uploaded_blueprint(second_file)
                with st.spinner("Evaluating blueprint 2 with InspectR..."):
                    st.session_state["comparison_results_2"] = evaluate(blueprint)
                st.session_state["comparison_name_2"] = second_file.name
                st.session_state["comparison_signature_2"] = second_signature
                st.success("Blueprint 2 evaluation complete.")
            except (RuntimeError, ValueError) as error:
                st.session_state.pop("comparison_results_2", None)
                st.error(f"Blueprint 2 evaluation failed: {error}")
    else:
        st.session_state.pop("comparison_results_2", None)
        st.session_state.pop("comparison_name_2", None)
        st.session_state.pop("comparison_signature_2", None)

results_1 = st.session_state.get("comparison_results_1")
results_2 = st.session_state.get("comparison_results_2")
name_1 = st.session_state.get("comparison_name_1", "Blueprint 1")
name_2 = st.session_state.get("comparison_name_2", "Blueprint 2")

if results_1 is not None or results_2 is not None:
    st.divider()
    st.markdown("#### Live evaluation results")
    result_columns = st.columns(2)

    for column, name, results in (
        (result_columns[0], name_1, results_1),
        (result_columns[1], name_2, results_2),
    ):
        with column:
            st.markdown(f"**{name}**")
            if results is None:
                st.caption("Not evaluated yet.")
            else:
                render_results(results)

if results_1 is not None and results_2 is not None:
    st.divider()
    st.markdown("#### Comparison of live evaluation results")
    st.write(
        "This comparison is generated from the two completed InspectR "
        "evaluations. It does not contain expected or hard-coded statuses."
    )

    results_by_rule_1 = {result["rule"]: result for result in results_1}
    results_by_rule_2 = {result["rule"]: result for result in results_2}
    comparison_rows = []

    for rule in RULE_ORDER:
        status_1 = results_by_rule_1.get(rule, {}).get("status", "MISSING")
        status_2 = results_by_rule_2.get(rule, {}).get("status", "MISSING")
        comparison_rows.append(
            {
                "Rule": rule,
                name_1: status_1,
                name_2: status_2,
                "Change": (
                    "No change"
                    if status_1 == status_2
                    else f"{status_1} → {status_2}"
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(comparison_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("##### Rule-level evidence comparison")
    for rule in RULE_ORDER:
        result_1 = results_by_rule_1.get(rule)
        result_2 = results_by_rule_2.get(rule)
        with st.expander(
            f"{rule}: {(result_1 or {}).get('status', 'MISSING')} vs "
            f"{(result_2 or {}).get('status', 'MISSING')}"
        ):
            evidence_columns = st.columns(2)
            for column, name, result in (
                (evidence_columns[0], name_1, result_1),
                (evidence_columns[1], name_2, result_2),
            ):
                with column:
                    st.markdown(
                        f"**{name} — "
                        f"{result.get('status', 'MISSING')}**"
                    )
                    if result:
                        st.write(result["reason"])
                        render_evidence(result["evidence"])
                    else:
                        st.caption("This rule did not return a result.")

    st.info(
        """
        **How to read this comparison**

        The table compares the results produced by the same InspectR rules for
        the two uploaded blueprints. A change means that the available
        evidence in the files led to a different result; it does not mean that
        the policy itself changed.

        - **OK** means that the evidence required by the encoded rule was found
          and satisfied.
        - **FAIL** means that the evidence was found but did not satisfy the
          rule, or that the rule identified a negative condition.
        - **HUMAN** means that the available evidence is insufficient for an
          automated conclusion and requires human review.

        The extended blueprint is intentionally designed to expose this
        distinction. Its human-oversight evidence explicitly represents a
        decision that still requires human attention, so InspectR must not
        treat the result as automatically satisfied. This is an intentional
        demonstration of how the evaluation surfaces a governance issue rather
        than hiding it.

        These are design-time results for the rules encoded in this PoC. They
        explain what the submitted blueprint evidence supports, but they do
        not establish complete legal or organisational compliance.
        """
    )
