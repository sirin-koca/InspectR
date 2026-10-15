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

# 4. SINGLE COMPLETE RULE DEFINITION: Routes exactly one final status report map to your UI
article := final_report if {
	# Path A: Trigger a validation failure if a DPIA is required but any gate is unverified
	dpia_is_legally_required
	some gate in compliance_gates
	gate.properties.dpia_completed == false

	final_report := {
		"rule": "TK-001",
		"status": "FAIL",
		"legal_reference": "GDPR Article 35",
		"reason": "A DPIA is legally required due to sensitive data processing but has not been verified as completed.",
		"evidence": {
			"input_evidence": [{
				"selector": sprintf("pipeline.nodes[%s].properties.dpia_completed", [gate.id]),
				"observed": gate.properties.dpia_completed,
				"expected": true,
				"condition": "Processing special category data requires a verified DPIA gate."
			}],
			"derived_evidence": {
				"dpia_required_by_law": true,
				"dpia_gate_completed": false
			}
		},
		"remedy": "Conduct a DPIA and update your compliance_gate node properties to 'dpia_completed: true'."
	}
}

else := final_report if {
	# Path B: Pass inspection if a DPIA is required and a verified gate is confirmed true
	dpia_is_legally_required
	some gate in compliance_gates
	gate.properties.dpia_completed == true

	final_report := {
		"rule": "TK-001",
		"status": "PASS",
		"legal_reference": "GDPR Article 35",
		"reason": "DPIA compliance obligations are satisfied. A verified compliance gate was found in the data pipeline blueprint.",
		"evidence": {
			"input_evidence": [{
				"selector": sprintf("pipeline.nodes[%s].properties.dpia_completed", [gate.id]),
				"observed": gate.properties.dpia_completed,
				"expected": true,
				"condition": "Compliance gate explicitly tracks and satisfies DPIA execution metrics."
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
