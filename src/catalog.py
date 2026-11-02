"""
Single source of truth for the rule set and status model shown in the app.

Pages read from here instead of keeping their own copies, so the UI cannot
drift from the Rego rules again. The Rego files in policies/tk remain the
authority on behaviour; this file only describes them.
"""

RULE_SET_VERSION = "tk-v2.0"

# (status, icon, meaning, who acts next)
STATUS_MODEL = [
    ("PASS", "🟢", "The obligation applies and the blueprint declares every required control as true.", "Nobody (design level only)"),
    ("FAIL", "🔴", "The obligation applies and the blueprint declares a required control as false.", "Designer: add the control"),
    ("UNKNOWN", "🟡", "A fact the rule needs is undetermined: absent, null, or not a boolean.", "Designer or inLUMEN: supply the fact"),
    ("HUMAN", "🟠", "Everything checkable is declared, but the final decision is a legal judgement.", "Legal or domain expert"),
    ("NOT_APPLICABLE", "⚪", "The trigger facts are declared false, so the obligation does not apply.", "Nobody"),
    ("ERROR", "⛔", "InspectR could not evaluate the rule. Not a finding about the blueprint.", "InspectR developer"),
]

STATUSES = tuple(s for s, *_ in STATUS_MODEL)
STATUS_ICON = {s: icon for s, icon, *_ in STATUS_MODEL}

RULES = [
    {
        "id": "TK-R1",
        "title": "DPIA and risk-assessment checkpoint",
        "replaces": "TK-001, TK-002",
        "legal_reference": "GDPR Art. 35(1), Art. 35(3)(b), Art. 9",
        "evidence_class": "Declared",
        "trigger": "A data_source declares contains_special_category_data: true.",
        "control": "One compliance_gate declares dpia_checkpoint_defined: true and risk_assessment_checkpoint_defined: true.",
        "selectors": [
            "pipeline.nodes[type==data_source].properties.contains_special_category_data",
            "pipeline.nodes[type==compliance_gate].properties.dpia_checkpoint_defined",
            "pipeline.nodes[type==compliance_gate].properties.risk_assessment_checkpoint_defined",
        ],
        "outcomes": {
            "PASS": "Trigger true and one gate declares both checkpoints true.",
            "FAIL": "Trigger true and no compliance gate exists, or a gate declares a checkpoint false.",
            "UNKNOWN": "Trigger undetermined, or trigger true and checkpoints undetermined.",
            "NOT_APPLICABLE": "Every data source declares the trigger false.",
        },
        "boundary": "Does not assess whether a DPIA was carried out, its quality, or its legal adequacy.",
    },
    {
        "id": "TK-R2",
        "title": "Lineage record for integrated data",
        "replaces": "TK-004",
        "legal_reference": "GDPR Art. 5(2), Art. 30",
        "evidence_class": "Derivable (from inLUMEN runs, future)",
        "trigger": "The design contains a data_integration node.",
        "control": "Every data_integration node declares lineage_record_defined: true.",
        "selectors": [
            "pipeline.nodes[type==data_integration]",
            "pipeline.nodes[type==data_integration].properties.lineage_record_defined",
        ],
        "outcomes": {
            "PASS": "Every integration node declares a lineage record.",
            "FAIL": "An integration node declares lineage_record_defined: false.",
            "UNKNOWN": "An integration node has the field undetermined.",
            "NOT_APPLICABLE": "The design has no data_integration node.",
        },
        "boundary": "Does not verify lineage quality, completeness, or runtime generation.",
    },
    {
        "id": "TK-R3",
        "title": "Purpose compatibility before sharing",
        "replaces": "TK-005",
        "legal_reference": "GDPR Art. 5(1)(b), Art. 6(4)",
        "evidence_class": "Judgement",
        "trigger": "A data_transfer node exists and a data_source declares contains_personal_data: true.",
        "control": "The compliance gates that carry purpose_compatibility_declared all declare true.",
        "selectors": [
            "pipeline.nodes[type==data_transfer]",
            "pipeline.nodes[type==data_source].properties.contains_personal_data",
            "pipeline.nodes[type==compliance_gate].properties.purpose_compatibility_declared",
        ],
        "outcomes": {
            "HUMAN": "Compatibility is declared; a legal or domain expert must confirm it. This rule has no PASS.",
            "FAIL": "A gate declares purpose_compatibility_declared: false.",
            "UNKNOWN": "Personal-data flag undetermined, or no gate carries a boolean compatibility field.",
            "NOT_APPLICABLE": "No data_transfer node, or every source declares no personal data.",
        },
        "boundary": "Does not perform the legal compatibility assessment itself.",
    },
]

DROPPED_RULES = [
    ("TK-003", "Data-sharing agreement", "Dropped to keep scope small; can return as TK-R4 with the structure of TK-R1."),
    ("TK-006", "Complete sharing safeguards", "Dropped: depended on fixed node IDs and repeated checks of other rules."),
]
