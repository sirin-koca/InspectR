import json

import streamlit as st

from src.evaluator import evaluate
from src.scenarios import SCENARIOS, build
from src.ui import page_header, render_results

page_header(
    "Inspect",
    "What does InspectR conclude for a given blueprint, and on what evidence?",
)

UPLOAD = "Upload a blueprint"
labels = [label for _, label, *_ in SCENARIOS] + [UPLOAD]
by_label = {label: (key, change, expected) for key, label, change, _, expected in SCENARIOS}

choice = st.radio(
    "Blueprint",
    labels,
    horizontal=True,
    label_visibility="collapsed",
    key="inspect_choice",
)

blueprint, expected = None, None
if choice == UPLOAD:
    uploaded = st.file_uploader("JSON blueprint", type=["json"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            blueprint = json.loads(uploaded.getvalue().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            st.error(f"{uploaded.name} is not valid UTF-8 JSON: {error}")
    else:
        st.caption("Choose a JSON blueprint to inspect.")
else:
    key, change, expected = by_label[choice]
    blueprint = build(key)
    st.caption(f"**Change from the enriched blueprint:** {change}")

if blueprint is not None:
    try:
        with st.spinner("Evaluating with OPA..."):
            results = evaluate(blueprint)
    except (RuntimeError, ValueError) as error:
        results = None
        st.error(f"InspectR could not run: {error}")

    if results is not None:
        render_results(results, expected)
        if expected:
            ok = all(r["status"] == expected.get(r["rule"]) for r in results)
            (st.success if ok else st.error)(
                "All results match the expected statuses for this scenario."
                if ok else "At least one result differs from the expected status."
            )

    with st.expander("Blueprint JSON submitted to OPA"):
        st.code(json.dumps(blueprint, indent=2, ensure_ascii=False), language="json", line_numbers=True)
