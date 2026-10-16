import hashlib
import json

import pandas as pd
import streamlit as st

from src.evaluator import evaluate


def status_counts(results: list[dict]) -> str:
    counts = {status: 0 for status in ("PASS", "FAIL", "HUMAN")}
    for result in results:
        counts[result["status"]] += 1
    return " · ".join(f"{status}: {counts[status]}" for status in counts)


def status_message(status: str) -> str:
    return {
        "PASS": "🟢 PASS",
        "FAIL": "🔴 FAIL",
        "HUMAN": "🟠 HUMAN",
    }.get(status, f"⚪ {status}")


def render_evidence(evidence: dict) -> None:
    input_evidence = evidence.get("input_evidence", [])
    if input_evidence:
        st.caption("Input evidence")
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
            height=min(240, 80 + len(rows) * 35),
            column_config={
                "Blueprint selector": st.column_config.TextColumn(
                    "Blueprint selector",
                    width="large",
                ),
                "Observed": st.column_config.TextColumn(width="small"),
                "Expected": st.column_config.TextColumn(width="small"),
                "Condition": st.column_config.TextColumn(width="large"),
            },
        )

    derived_evidence = evidence.get("derived_evidence")
    if derived_evidence:
        st.caption("Derived design-time evidence calculated by Rego")
        st.json(derived_evidence)


def render_results(results: list[dict]) -> None:
    counts = {status: 0 for status in ("PASS", "FAIL", "HUMAN")}
    for result in results:
        counts[result["status"]] += 1

    summary_columns = st.columns(3)
    for column, status in (
        (summary_columns[0], "PASS"),
        (summary_columns[1], "FAIL"),
        (summary_columns[2], "HUMAN"),
    ):
        with column:
            st.metric(status, counts[status])

    st.caption(
        " · ".join(
            f"{status}: {counts[status]}"
            for status in ("PASS", "FAIL", "HUMAN")
        )
    )
    for result in results:
        with st.expander(
            f"{status_message(result['status'])} — {result['rule']}"
        ):
            st.caption(result["legal_reference"])
            st.markdown(result["reason"])
            with st.container(border=True):
                render_evidence(result["evidence"])
            if result["remedy"]:
                st.info(f"**Remedy**  \n{result['remedy']}")


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
    "Upload one static JSON pipeline blueprint and inspect its planned "
    "compliance checkpoints with the InspectR Policy-as-Code rules."
)

with st.container(border=True):
    st.markdown("#### Inspect a pipeline blueprint")
    st.caption(
        "Upload a JSON blueprint containing data, workflow and infrastructure metadata, then run the six TK/MUNDAT design-time rules."
    )
    uploaded_file = st.file_uploader(
        "JSON blueprint",
        type=["json"],
        key="evaluation_blueprint",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_signature = uploaded_file_signature(uploaded_file)
        if st.session_state.get("evaluation_signature") not in (
            None,
            file_signature,
        ):
            st.session_state.pop("evaluation_results", None)
            st.session_state.pop("evaluation_name", None)

        try:
            uploaded_blueprint = load_uploaded_blueprint(uploaded_file)
        except ValueError as error:
            uploaded_blueprint = None
            st.error(str(error))

        action_columns = st.columns([2, 1])
        with action_columns[0]:
            st.caption(f"Selected file: **{uploaded_file.name}**")
        with action_columns[1]:
            run_evaluation = st.button(
                "Run InspectR",
                type="primary",
                use_container_width=True,
                key="evaluate_blueprint",
            )

        if run_evaluation:
            try:
                if uploaded_blueprint is None:
                    raise ValueError("Upload a valid JSON blueprint before evaluation.")
                with st.spinner("Evaluating blueprint with InspectR..."):
                    st.session_state["evaluation_results"] = evaluate(
                        uploaded_blueprint
                    )
                st.session_state["evaluation_name"] = uploaded_file.name
                st.session_state["evaluation_signature"] = file_signature
                st.success("Design-time blueprint inspection complete.")
            except (RuntimeError, ValueError) as error:
                st.session_state.pop("evaluation_results", None)
                st.error(f"Blueprint evaluation failed: {error}")
    else:
        st.caption("Choose a JSON blueprint to begin.")
        st.session_state.pop("evaluation_results", None)
        st.session_state.pop("evaluation_name", None)
        st.session_state.pop("evaluation_signature", None)

results = st.session_state.get("evaluation_results")
name = st.session_state.get("evaluation_name", "Uploaded blueprint")

if uploaded_file is not None and uploaded_blueprint is not None:
    st.divider()
    blueprint_column, results_column = st.columns([1, 1], gap="large")

    with blueprint_column:
        st.markdown("#### Blueprint JSON")
        st.caption("The exact planned design submitted to OPA.")
        with st.container(border=True):
            st.code(
                json.dumps(uploaded_blueprint, indent=2, ensure_ascii=False),
                language="json",
                line_numbers=True,
                wrap_lines=False,
            )

    with results_column:
        st.markdown(f"#### Results — `{name}`")
        st.caption(
            "Design-time findings from the active TK/MUNDAT policy. "
            "Expand a rule to inspect its evidence and remedy."
        )
        if results is None:
            st.info("Run InspectR to display the evaluation results.")
        else:
            render_results(results)
