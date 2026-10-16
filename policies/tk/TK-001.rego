#
# TK-001 : dpia_checkpoint_defined
#

package inspectr.tk.tk001

import rego.v1

# 1. Safely parse nodes array from the uploaded compliance blueprint JSON
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

# 2. Helper Rule: Compute if a DPIA is legally triggered based on data profiles
dpia_is_legally_required if {
	some node in nodes
	node.type == "data_source"
	node.properties.contains_personal_data == true
	node.properties.contains_special_category_data == true
}

# 3. Helper Rule: Find any compliance gates in the pipeline
compliance_gates := [gate | some gate in nodes; gate.type == "compliance_gate"]

dpia_checkpoint_value(gate) := object.get(
	object.get(gate, "properties", {}),
	"dpia_checkpoint_defined",
	object.get(object.get(gate, "properties", {}), "dpia_completed", null)
)

# 4. SINGLE COMPLETE RULE DEFINITION: Routes exactly one final status report map to your UI
article := final_report if {
	# Path A: Fail if a DPIA is required but a checkpoint is not defined
	dpia_is_legally_required
	some gate in compliance_gates
	dpia_checkpoint_value(gate) == false

	final_report := {
		"rule": "TK-001",
		"status": "FAIL",
		"legal_reference": "GDPR Article 35",
		"reason": "A DPIA checkpoint is required by the design, but the blueprint declares that it is not defined.",
		"evidence": {
			"input_evidence": [{
				"selector": sprintf("pipeline.nodes[%s].properties.dpia_checkpoint_defined", [gate.id]),
				"observed": dpia_checkpoint_value(gate),
				"expected": true,
				"condition": "Processing special-category data requires a DPIA checkpoint in the planned pipeline."
			}],
			"derived_evidence": {
				"dpia_required_by_law": true,
				"dpia_checkpoint_defined": false
			}
		},
		"remedy": "Add a DPIA checkpoint to the planned pipeline and set 'dpia_checkpoint_defined: true' on the compliance gate."
	}
}

else := final_report if {
	# Path B: Pass if a DPIA is required and a checkpoint is defined
	dpia_is_legally_required
	some gate in compliance_gates
	dpia_checkpoint_value(gate) == true

	final_report := {
		"rule": "TK-001",
		"status": "PASS",
		"legal_reference": "GDPR Article 35",
		"reason": "The blueprint includes a DPIA checkpoint for the sensitive-data processing design.",
		"evidence": {
			"input_evidence": [{
				"selector": sprintf("pipeline.nodes[%s].properties.dpia_checkpoint_defined", [gate.id]),
				"observed": dpia_checkpoint_value(gate),
				"expected": true,
				"condition": "The planned pipeline includes a DPIA checkpoint before sensitive processing."
			}],
			"derived_evidence": {
				"dpia_legally_required": true,
				"dpia_gate_id": gate.id
			}
		},
		"remedy": null
	}
}

else := final_report if {
	# Path C: Pass inspection because no sensitive metrics are handled
	not dpia_is_legally_required

	final_report := {
		"rule": "TK-001",
		"status": "PASS",
		"legal_reference": "GDPR Article 35",
		"reason": "Data processing context does not handle sensitive special category data. A formal DPIA is not triggered.",
		"evidence": {
			"input_evidence": [],
			"derived_evidence": {
				"dpia_legally_required": false
			}
		},
		"remedy": null
	}
}
