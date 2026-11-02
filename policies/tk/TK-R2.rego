#
# TK-R2 : Lineage record for integrated data
#
# Replaces TK-004.
#
# Requirement  TK needs "metadata and lineage" and "Traceability: document
#              data provenance and processing"; MUNDAT activity "integrate data".
# Legal basis  GDPR Art. 5(2) (accountability); Art. 30 where applicable.
# Trigger      The design contains a node with type: data_integration.
# Control      Every such node declares lineage_record_defined: true.
# Evidence     Declared today; could be derived from inLUMEN runs (class D).
#
# Decision table (evaluated top to bottom, first match wins)
#   1  (input has no pipeline.nodes: rejected by evaluator.py before OPA)
#   2  no data_integration node                              -> NOT_APPLICABLE
#   3  an integration node declares the control false        -> FAIL
#   4  an integration node has the control missing/invalid   -> UNKNOWN
#   5  every integration node declares the control true      -> PASS
#   6  anything else (should be unreachable)                 -> ERROR
#
# Known limit: a raw inLUMEN export uses "kind", not "type", so it has no
# data_integration node and returns NOT_APPLICABLE. That is a correct reading
# of the input but not of the pipeline; the planned adapter (RQ2) fixes it.
#
package inspectr.tk.r2

import data.inspectr.lib
import rego.v1

rule_id := "TK-R2"

title := "Lineage record for integrated data"

legal_reference := "GDPR Art. 5(2), Art. 30"

control_field := "lineage_record_defined"

integrations := lib.nodes_of_type("data_integration")

false_ids := [n.id | some n in integrations; lib.is_false(n, control_field)]

unusable_ids := [n.id | some n in integrations; lib.not_usable(n, control_field)]

control_evidence := [lib.evidence(n, control_field, true, "An integration step must declare a lineage record so the combined dataset is traceable to its sources.") |
	some n in integrations
]

report(status, row, reason, remedy) := {
	"rule": rule_id,
	"title": title,
	"status": status,
	"decision_row": row,
	"legal_reference": legal_reference,
	"reason": reason,
	"evidence": {
		"input_evidence": control_evidence,
		"derived_evidence": {
			"integration_nodes": [n.id | some n in integrations],
			"nodes_with_control_false": false_ids,
			"nodes_with_control_unusable": unusable_ids,
		},
	},
	"remedy": remedy,
}

default result := {
	"rule": "TK-R2",
	"title": "Lineage record for integrated data",
	"status": "ERROR",
	"decision_row": 6,
	"legal_reference": "GDPR Art. 5(2), Art. 30",
	"reason": "No decision-table row matched. This is a defect in the rule, not a finding about the blueprint.",
	"evidence": {"input_evidence": [], "derived_evidence": {}},
	"remedy": "Report to the InspectR developer: add a test for this input and close the gap in TK-R2.",
}

result := report(
	"NOT_APPLICABLE", 2,
	"The design declares no data_integration node, so no lineage record is required by this rule.",
	null,
) if {
	count(integrations) == 0
} else := report(
	"FAIL", 3,
	sprintf("Integration step(s) %v declare that no lineage record is defined.", [false_ids]),
	"Define a catalogue-backed lineage record for each listed integration node and set lineage_record_defined: true.",
) if {
	count(false_ids) > 0
} else := report(
	"UNKNOWN", 4,
	sprintf("Integration step(s) %v do not declare lineage_record_defined as a boolean, so InspectR cannot decide.", [unusable_ids]),
	"Declare lineage_record_defined as true or false on each listed integration node.",
) if {
	count(unusable_ids) > 0
} else := report(
	"PASS", 5,
	sprintf("All %d integration step(s) declare a lineage record.", [count(integrations)]),
	null,
) if {
	every n in integrations {
		lib.is_true(n, control_field)
	}
}
