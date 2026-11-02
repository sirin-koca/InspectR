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
        "tk_requirement": ("DPIA / risk assessment", "Determine whether processing requires a DPIA and assess risk before relevant processing/sharing."),
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
        "tk_requirement": ("Traceability", "Document data provenance and processing performed during dataset construction."),
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
        "tk_requirement": ("Lawfulness", "Assess whether requested processing and sharing are legally permissible (here: is the new purpose compatible with the original one?)."),
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


# Facts the rules read, and where they can come from.
# Provenance: S = structural (graph), D = derivable from tooling, M = manual
# declaration, H = human judgement.
RULE_FACTS = [
    ("TK-R1", "data_source.contains_special_category_data", "Trigger", "M (future: D from schema/PII detection)"),
    ("TK-R1", "compliance_gate.dpia_checkpoint_defined", "Control", "M"),
    ("TK-R1", "compliance_gate.risk_assessment_checkpoint_defined", "Control", "M"),
    ("TK-R2", "node type data_integration", "Trigger", "S"),
    ("TK-R2", "data_integration.lineage_record_defined", "Control", "M (future: D from inLUMEN runs)"),
    ("TK-R3", "node type data_transfer", "Trigger", "S"),
    ("TK-R3", "data_source.contains_personal_data", "Trigger", "M (future: D from schema/PII detection)"),
    ("TK-R3", "compliance_gate.purpose_compatibility_declared", "Control", "H (declared, confirmed by an expert)"),
]

# Defects found in rule set v1 and how v2 fixes them (measured with OPA).
DEFECTS = [
    ("D1", "One missing control field made one rule undefined, and with it the whole result list.",
     "No results at all for V2 with dpia_checkpoint_defined removed.",
     "UNKNOWN row in every rule; one OPA query per rule; ERROR isolated to the failing rule."),
    ("D2", "A missing trigger fell into the 'not required' branch.",
     "False PASS for TK-001 and TK-002 with the special-category flag removed.",
     "Undetermined trigger gives UNKNOWN; only a trigger declared false gives NOT_APPLICABLE."),
    ("D3", "TK-005 returned HUMAN as soon as any gate lacked the purpose field.",
     "HUMAN on V2 for the wrong reason (the DPIA gate, not the sharing gate).",
     "TK-R3 ignores gates that do not carry the field."),
    ("D4", "'Not applicable' branches reported PASS with evidence that is not in the blueprint.",
     "Five vacuous PASS results on the raw inLUMEN export.",
     "NOT_APPLICABLE or UNKNOWN instead; derived evidence lists only what was examined."),
    ("D5", "OPA called at a fixed Windows path.",
     "Not runnable outside one machine.",
     "OPA_PATH, then PATH, then the old path."),
]

# PoC acceptance criteria from the Scope and Evaluation Proposal (30 Oct 2026).
ACCEPTANCE = [
    ("AC1", "Native inLUMEN export accepted through an adapter; manual enrichment listed separately.", "Open",
     "No adapter yet. Enrichment is documented on the Case page."),
    ("AC2", "Policy packs for three use cases without engine changes.", "Open",
     "One use case (TK). Rules are already isolated from the engine."),
    ("AC3", "Every finding has rule ID, status, policy-source reference, evidence path, reason, remedy.", "Met",
     "Enforced by the evaluator's result contract."),
    ("AC4", "Uniform result semantics; missing information gives UNKNOWN, never PASS.", "Met",
     "Decision tables plus regression tests for D1 and D2."),
    ("AC5", "opa test cases for pass, fail, missing and not-applicable per rule.", "Met",
     "29 Rego tests, at least one per decision-table row."),
    ("AC6", "Reproducible through Docker and CLI, deterministic output.", "Partial",
     "Deterministic and runnable via opa eval; no Docker image yet."),
    ("AC7", "Domain expert review of a policy sample.", "Open",
     "To be requested from SINTEF / TK."),
]

OPEN_QUESTIONS = [
    "Is three rules acceptable for iteration 1, or should TK-003 (data-sharing agreement) return as TK-R4?",
    "Should a design with special-category data and no compliance gate be FAIL (current) or UNKNOWN?",
    "Can inLUMEN export node type and the compliance fields, or is an adapter on the InspectR side preferred?",
    "Who at SINTEF or TK can review the three rules for fidelity (AC7)?",
    "Any confidentiality restriction on deriving rules from TK documents in a public repository?",
]
