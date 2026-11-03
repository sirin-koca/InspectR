import streamlit as st

from src.research_content import (
    CONTRIBUTIONS, DIRECTIONS, EVALUATION, GAPS, KEY_WORKS, MAIN_RQ,
    METHOD_REFERENCE, RQS, SUB_QUESTIONS,
)
from src.ui import page_header


def md_table(header: list[str], rows) -> None:
    """Markdown table: wraps long text and keeps links clickable."""
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c).replace("|", "/") for c in row) + " |" for row in rows]
    st.markdown("\n".join(lines))


page_header(
    "Research",
    "What is known, what is missing, and what can InspectR add?",
)
st.markdown(
    "The argument runs as one chain: **key works → gaps → research questions → candidate "
    "contributions → evaluation**. Contributions are candidates to be tested, not claims. "
    f"Method: Design Science Research ([{METHOD_REFERENCE[0]}]({METHOD_REFERENCE[1]}))."
)

# ---------------------------------------------------------------- key works
st.subheader("Litterature review: key works")
md_table(
    ["ID", "Work", "Offers", "Stated limit or future work", "Relevance to InspectR"],
    [(i, f"[{c}]({u})", o, l, r) for i, c, u, o, l, r in KEY_WORKS],
)

# ---------------------------------------------------------------- gaps
st.subheader("Research gaps")
md_table(["ID", "Gap", "Supported by", "Addressed by"], GAPS)

# ---------------------------------------------------------------- RQs
st.subheader("Research questions")
st.markdown(f"**Main RQ.** {MAIN_RQ}")
for column, (rq, title, question) in zip(st.columns(3), RQS):
    with column.container(border=True):
        st.markdown(f"**{rq} · {title}**")
        st.write(question)
st.markdown("**Candidate sub-questions**")
md_table(["RQ", "Sub-question", "Gap"], SUB_QUESTIONS)

# ---------------------------------------------------------------- contributions
st.subheader("Candidate contributions")
md_table(
    ["ID", "Candidate contribution", "Type", "Gap", "RQ", "Evidence so far"],
    CONTRIBUTIONS,
)

# ---------------------------------------------------------------- evaluation
st.subheader("Evaluation")
md_table(["Metric", "Answers", "Baseline"], EVALUATION)
st.caption("From the Scope and Evaluation Proposal (30 October 2026).")

# ---------------------------------------------------------------- directions
st.subheader("Possible research directions")
md_table(["Direction", "Gap", "Source"], DIRECTIONS)
