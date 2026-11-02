"""Shared UI helpers for the InspectR pages."""

import json

import pandas as pd
import streamlit as st

from src.catalog import STATUS_ICON, STATUSES


def page_header(title: str, question: str) -> None:
    """Every page opens with its title and the one question it answers."""
    st.title(title)
    st.caption(question)


def badge(status: str) -> str:
    return f"{STATUS_ICON.get(status, '⚪')} {status}"


def as_text(value) -> str:
    """Evidence values mix booleans, strings and lists; show them as JSON text."""
    return value if isinstance(value, str) else json.dumps(value)


def table(rows, columns=None, height=None) -> None:
    frame = pd.DataFrame(rows, columns=columns) if columns else pd.DataFrame(rows)
    kwargs = {"use_container_width": True, "hide_index": True}
    if height:
        kwargs["height"] = height
    st.dataframe(frame, **kwargs)


def render_evidence(evidence: dict) -> None:
    rows = [
        {
            "Blueprint selector": item.get("selector"),
            "Observed": as_text(item.get("observed")),
            "Expected": as_text(item.get("expected")),
            "Condition": item.get("condition"),
        }
        for item in evidence.get("input_evidence", [])
    ]
    if rows:
        st.caption("Input evidence: what OPA read from the blueprint")
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Blueprint selector": st.column_config.TextColumn(width="large"),
                "Observed": st.column_config.TextColumn(width="small"),
                "Expected": st.column_config.TextColumn(width="small"),
                "Condition": st.column_config.TextColumn(width="large"),
            },
        )
    derived = evidence.get("derived_evidence")
    if derived:
        st.caption("Derived evidence: what Rego concluded from the input")
        st.json(derived, expanded=False)


def render_summary(results: list[dict]) -> None:
    counts = {status: 0 for status in STATUSES}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    for column, status in zip(st.columns(len(STATUSES)), STATUSES):
        column.metric(badge(status).replace("_", " "), counts[status])


def render_results(results: list[dict], expected: dict | None = None) -> None:
    render_summary(results)
    for result in results:
        rule, status = result["rule"], result["status"]
        check = ""
        if expected and rule in expected:
            check = "  ✓ as expected" if expected[rule] == status else f"  ✗ expected {expected[rule]}"
        title = f" · {result['title']}" if result.get("title") else ""
        with st.expander(f"{badge(status)} — {rule}{title}{check}"):
            row = result.get("decision_row")
            st.caption(
                f"{result['legal_reference']}"
                + (f" · decision-table row {row}" if row is not None else "")
            )
            st.markdown(result["reason"])
            render_evidence(result["evidence"])
            if result["remedy"]:
                st.info(f"**Remedy:** {result['remedy']}")
