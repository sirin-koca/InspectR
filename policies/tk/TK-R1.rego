#
# TK-R1 : DPIA and risk-assessment checkpoint for special-category data
#
# Replaces TK-001 (DPIA checkpoint) and TK-002 (risk-assessment checkpoint),
# which had the same trigger.
#
# Requirement  TK need "DPIA / risk assessment"; MUNDAT activity
#              "perform DPIA and risk assessment"; Sickleave dataset.
# Legal basis  GDPR Art. 35(1), Art. 35(3)(b) where applicable; Art. 9.
# Trigger      Any data_source declares contains_special_category_data: true.
# Controls     One compliance_gate declares both
#              dpia_checkpoint_defined: true and
#              risk_assessment_checkpoint_defined: true.
# Evidence     Manually declared (class M). inLUMEN does not export it today.
#
# Decision table (evaluated top to bottom, first match wins)
#   1  no source declares true, and a source flag is missing/invalid
#      or there are no data sources                         -> UNKNOWN
#   2  every source declares false                           -> NOT_APPLICABLE
#   3  trigger true, no compliance_gate in the design        -> FAIL
#   4  trigger true, a gate declares a control false         -> FAIL
#   5  trigger true, one gate declares both controls true    -> PASS
#   6  trigger true, controls missing/invalid                -> UNKNOWN
#   7  anything else (should be unreachable)                 -> ERROR
#
package inspectr.tk.r1

import data.inspectr.lib
import rego.v1

rule_id := "TK-R1"

title := "DPIA and risk-assessment checkpoint for special-category data"

legal_reference := "GDPR Art. 35(1), Art. 35(3)(b), Art. 9"

trigger_field := "contains_special_category_data"

control_fields := ["dpia_checkpoint_defined", "risk_assessment_checkpoint_defined"]

sources := lib.nodes_of_type("data_source")

gates := lib.nodes_of_type("compliance_gate")

# ---------- trigger ----------

trigger_true if {
	some s in sources
	lib.is_true(s, trigger_field)
}

unusable_sources := [s.id | some s in sources; lib.not_usable(s, trigger_field)]

trigger_unknown if {
	not trigger_true
	count(unusable_sources) > 0
}

trigger_unknown if {
	not trigger_true
	count(sources) == 0
}

trigger_false if {
	not trigger_true
	count(sources) > 0
	count(unusable_sources) == 0
}

# ---------- controls ----------

# Gates that carry at least one of the two control fields.
relevant_gate_ids := {g.id | some g in gates; some f in control_fields; lib.has_field(g, f)}

relevant_gates := [g | some g in gates; g.id in relevant_gate_ids]

control_false if {
	some g in relevant_gates
	some f in control_fields
	lib.is_false(g, f)
}

passing_gate_ids := [g.id |
	some g in relevant_gates
	every f in control_fields {
		lib.is_true(g, f)
	}
]

# ---------- evidence ----------

trigger_evidence := [lib.evidence(s, trigger_field, "boolean", "Declares whether this source processes special-category data (GDPR Art. 9).") |
	some s in sources
]

# If no gate carries the fields, show all gates so the reader sees where they are missing.
gates_to_show := relevant_gates if count(relevant_gates) > 0

else := gates

control_evidence := [lib.evidence(g, f, true, "A compliance gate must declare this checkpoint before sensitive processing.") |
	some g in gates_to_show
	some f in control_fields
]

report(status, row, reason, remedy, ev) := {
	"rule": rule_id,
	"title": title,
	"status": status,
	"decision_row": row,
	"legal_reference": legal_reference,
	"reason": reason,
	"evidence": {
		"input_evidence": ev,
		"derived_evidence": {
			"special_category_trigger": trigger_state,
			"sources_with_unusable_flag": unusable_sources,
			"compliance_gates": [g.id | some g in gates],
			"gates_with_both_controls": passing_gate_ids,
		},
	},
	"remedy": remedy,
}

trigger_state := "true" if trigger_true

else := "unknown" if trigger_unknown

else := "false"

# ---------- decision ----------

default result := {
	"rule": "TK-R1",
	"title": "DPIA and risk-assessment checkpoint for special-category data",
	"status": "ERROR",
	"decision_row": 7,
	"legal_reference": "GDPR Art. 35(1), Art. 35(3)(b), Art. 9",
	"reason": "No decision-table row matched. This is a defect in the rule, not a finding about the blueprint.",
	"evidence": {"input_evidence": [], "derived_evidence": {}},
	"remedy": "Report to the InspectR developer: add a test for this input and close the gap in TK-R1.",
}

result := report(
	"UNKNOWN", 1,
	"InspectR cannot decide whether special-category data is processed: no data source declares it as true, and the flag is missing or invalid on at least one source (or no data sources are declared).",
	"Declare contains_special_category_data as true or false on every data_source node.",
	trigger_evidence,
) if {
	trigger_unknown
} else := report(
	"NOT_APPLICABLE", 2,
	"Every data source declares contains_special_category_data: false, so a DPIA and risk assessment are not triggered by this rule.",
	null,
	trigger_evidence,
) if {
	trigger_false
} else := report(
	"FAIL", 3,
	"Special-category data is processed, but the design contains no compliance gate for the DPIA and risk assessment.",
	"Add a compliance_gate before sensitive processing that declares dpia_checkpoint_defined: true and risk_assessment_checkpoint_defined: true.",
	trigger_evidence,
) if {
	trigger_true
	count(gates) == 0
} else := report(
	"FAIL", 4,
	"Special-category data is processed, but a compliance gate declares the DPIA or risk-assessment checkpoint as not defined.",
	"Define the missing checkpoint in the design and set the field to true.",
	array.concat(trigger_evidence, control_evidence),
) if {
	trigger_true
	control_false
} else := report(
	"PASS", 5,
	sprintf("Special-category data is processed and gate '%s' declares both a DPIA and a risk-assessment checkpoint.", [passing_gate_ids[0]]),
	null,
	array.concat(trigger_evidence, control_evidence),
) if {
	trigger_true
	count(passing_gate_ids) > 0
} else := report(
	"UNKNOWN", 6,
	"Special-category data is processed, but no compliance gate declares both checkpoints as booleans. The fields are missing or invalid.",
	"Declare dpia_checkpoint_defined and risk_assessment_checkpoint_defined as true or false on the compliance gate.",
	array.concat(trigger_evidence, control_evidence),
) if {
	trigger_true
}
