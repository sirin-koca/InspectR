#
# TK-R3 : Purpose compatibility before sharing personal data
#
# Replaces TK-005.
#
# Requirement  Requests from researchers, companies and other consumers who
#              want data for new purposes; TK need "Lawfulness".
# Legal basis  GDPR Art. 5(1)(b) (purpose limitation), Art. 6(4) (compatibility).
# Trigger      A data_transfer node exists AND some data_source declares
#              contains_personal_data: true.
# Control      purpose_compatibility_declared on a compliance_gate.
#              Gates that do not carry the field are ignored.
# Evidence     Legal judgement (class H): can be declared, never derived.
#              There is deliberately no PASS: the best outcome is HUMAN.
#
# Decision table (evaluated top to bottom, first match wins)
#   1  transfer exists, no source declares personal data true, and a
#      source flag is missing/invalid or there are no sources -> UNKNOWN
#   2  no transfer node, or every source declares false       -> NOT_APPLICABLE
#   3  applies, a gate declares the control false             -> FAIL
#   4  applies, no gate carries the field, or it is invalid   -> UNKNOWN
#   5  applies, every gate carrying the field declares true   -> HUMAN
#   6  anything else (should be unreachable)                  -> ERROR
#
package inspectr.tk.r3

import data.inspectr.lib
import rego.v1

rule_id := "TK-R3"

title := "Purpose compatibility before sharing personal data"

legal_reference := "GDPR Art. 5(1)(b), Art. 6(4)"

trigger_field := "contains_personal_data"

control_field := "purpose_compatibility_declared"

sources := lib.nodes_of_type("data_source")

transfers := lib.nodes_of_type("data_transfer")

gates := lib.nodes_of_type("compliance_gate")

# ---------- trigger ----------

personal_data_true if {
	some s in sources
	lib.is_true(s, trigger_field)
}

unusable_sources := [s.id | some s in sources; lib.not_usable(s, trigger_field)]

transfer_exists if count(transfers) > 0

applies if {
	transfer_exists
	personal_data_true
}

trigger_unknown if {
	transfer_exists
	not personal_data_true
	count(unusable_sources) > 0
}

trigger_unknown if {
	transfer_exists
	count(sources) == 0
}

# ---------- control ----------

carrying_gates := [g | some g in gates; lib.has_field(g, control_field)]

false_gate_ids := [g.id | some g in carrying_gates; lib.is_false(g, control_field)]

unusable_gate_ids := [g.id | some g in carrying_gates; lib.not_usable(g, control_field)]

# ---------- evidence ----------

trigger_evidence := array.concat(
	[{
		"selector": "pipeline.nodes[type==\"data_transfer\"]",
		"observed": [t.id | some t in transfers],
		"expected": "at least one node, if data leaves the municipality",
		"condition": "A data_transfer node means data is shared with another party.",
	}],
	[lib.evidence(s, trigger_field, "boolean", "Declares whether this source processes personal data.") | some s in sources],
)

control_evidence := [lib.evidence(g, control_field, true, "The design must declare that purpose compatibility was assessed before sharing.") |
	some g in carrying_gates
]

report(status, row, reason, remedy) := {
	"rule": rule_id,
	"title": title,
	"status": status,
	"decision_row": row,
	"legal_reference": legal_reference,
	"reason": reason,
	"evidence": {
		"input_evidence": array.concat(trigger_evidence, control_evidence),
		"derived_evidence": {
			"transfer_nodes": [t.id | some t in transfers],
			"sources_with_unusable_flag": unusable_sources,
			"gates_carrying_control": [g.id | some g in carrying_gates],
			"gates_with_control_false": false_gate_ids,
		},
	},
	"remedy": remedy,
}

# ---------- decision ----------

default result := {
	"rule": "TK-R3",
	"title": "Purpose compatibility before sharing personal data",
	"status": "ERROR",
	"decision_row": 6,
	"legal_reference": "GDPR Art. 5(1)(b), Art. 6(4)",
	"reason": "No decision-table row matched. This is a defect in the rule, not a finding about the blueprint.",
	"evidence": {"input_evidence": [], "derived_evidence": {}},
	"remedy": "Report to the InspectR developer: add a test for this input and close the gap in TK-R3.",
}

result := report(
	"UNKNOWN", 1,
	"Data is transferred, but InspectR cannot tell whether it is personal data: no source declares it as true, and the flag is missing or invalid on at least one source (or no data sources are declared).",
	"Declare contains_personal_data as true or false on every data_source node.",
) if {
	trigger_unknown
} else := report(
	"NOT_APPLICABLE", 2,
	"No personal data leaves the municipality in this design (no data_transfer node, or every source declares contains_personal_data: false).",
	null,
) if {
	not applies
} else := report(
	"FAIL", 3,
	sprintf("Personal data is shared, but gate(s) %v declare that purpose compatibility was not assessed.", [false_gate_ids]),
	"Assess purpose compatibility (GDPR Art. 6(4)) before sharing and set purpose_compatibility_declared: true on the gate.",
) if {
	count(false_gate_ids) > 0
} else := report(
	"UNKNOWN", 4,
	"Personal data is shared, but no compliance gate declares purpose_compatibility_declared as a boolean.",
	"Add purpose_compatibility_declared (true or false) to the sharing compliance gate.",
) if {
	count(carrying_gates) == 0
} else := report(
	"UNKNOWN", 4,
	sprintf("Gate(s) %v declare purpose_compatibility_declared with a non-boolean value.", [unusable_gate_ids]),
	"Set purpose_compatibility_declared to true or false.",
) if {
	count(unusable_gate_ids) > 0
} else := report(
	"HUMAN", 5,
	"The design declares a purpose-compatibility assessment before sharing. Compatibility is a legal judgement, so a legal or domain expert must confirm it.",
	"Have a legal or domain expert confirm the purpose-compatibility assessment (GDPR Art. 6(4)).",
) if {
	every g in carrying_gates {
		lib.is_true(g, control_field)
	}
}
