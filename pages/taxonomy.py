import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path


# --------------------------------------------------
# LOAD TAXONOMY
# --------------------------------------------------

TAXONOMY_PATH = Path("data/inspectr_taxonomy.json")

with open(TAXONOMY_PATH, "r", encoding="utf-8") as file:
    taxonomy = json.load(file)

# --------------------------------------------------
# CONVERT JSON TREE TO PLOTLY DATA
# --------------------------------------------------

labels = []
parents = []
levels = []
descriptions = []
colors = []
rule_ids = []
evidence_fields = []
legal_references = []
relationships = []


def flatten_taxonomy(node, parent="", inherited_color="dodgerblue"):

    current_color = node.get("color", inherited_color)

    labels.append(node["label"])
    parents.append(parent)
    levels.append(node.get("level", ""))
    descriptions.append(node.get("description", ""))
    colors.append(current_color)
    rule_ids.append(node.get("rule_id", ""))
    evidence_fields.append(", ".join(node.get("evidence_fields", [])))
    legal_references.append(", ".join(node.get("legal_references", [])))
    relationships.append(node.get("relationship", ""))

    for child in node.get("children", []):
        flatten_taxonomy(
            child,
            parent=node["label"],
            inherited_color=current_color,
        )


flatten_taxonomy(taxonomy)


# --------------------------------------------------
# BUILD ICICLE
# --------------------------------------------------

fig = px.icicle(
    names=labels,
    parents=parents,
    values=[1] * len(labels),
    custom_data=[
        levels,
        descriptions,
        rule_ids,
        evidence_fields,
        legal_references,
        relationships,
    ],
    title="TK/MUNDAT GDPR Compliance Scope",
)

fig.update_traces(
    marker=dict(colors=colors),
    hovertemplate=(
        "<b>%{label}</b><br><br>"
        "<b>Level:</b> %{customdata[0]}<br>"
        "<b>Description:</b> %{customdata[1]}<br>"
        "<b>Rule:</b> %{customdata[2]}<br>"
        "<b>Evidence:</b> %{customdata[3]}<br>"
        "<b>GDPR basis:</b> %{customdata[4]}<br>"
        "<b>Relationship:</b> %{customdata[5]}"
        "<extra></extra>"
    ),
    textinfo="label",
)


fig.update_layout(
    margin=dict(t=80, l=0, r=0, b=0),
    font=dict(size=16),
    title_font=dict(size=26),
)


st.plotly_chart(
    fig,
    use_container_width=True,
)

st.popover(
    "About this taxonomy",
).write(
    """
    Machine-readable compliance taxonomy used by the InspectR PoC for the
    TK/MUNDAT GDPR Compliance Scope.

    The taxonomy is organised by the selected legal basis: GDPR Articles 25,
    30, and 35. Each article branch contains a TK/MUNDAT operational
    interpretation, an executable constraint where available, and the
    blueprint evidence used by InspectR.

    The governance branch contains a TK/MUNDAT safeguard that supports the
    use case but is not presented as a standalone GDPR article implementation.

    These are limited design-time operational proxies. They do not establish
    legal compliance with the GDPR as a whole.
    """
)
# -------------------------
# TAXONOMY SUMMARY TABLE
# -------------------------
overview_df = pd.DataFrame([
    {
        "Level": "Root",
        "Meaning": "Selected TK/MUNDAT regulatory scope",
        "Example": "TK/MUNDAT GDPR Compliance Scope",
    },
    {
        "Level": "Domain",
        "Meaning": "Selected GDPR article or TK governance category",
        "Example": "GDPR Article 25",
    },
    {
        "Level": "Dimension",
        "Meaning": "TK/MUNDAT operational interpretation",
        "Example": "Processing Traceability",
    },
    {
        "Level": "Atomic Element",
        "Meaning": "Observable concept or blueprint property",
        "Example": "Required TK Pipeline Stages",
    },
    {
        "Level": "Constraint",
        "Meaning": "Machine-checkable requirement attached to the blueprint",
        "Example": "Required Intake-to-Output Flow",
    },
    {
        "Level": "Rule metadata",
        "Meaning": "Rule ID, evidence fields, legal basis, and relationship type",
        "Example": "TK-006; share_dataset.properties.encrypted_in_transit",
    },
])

st.dataframe(
    overview_df,
    use_container_width=True,
    hide_index=True,
)
