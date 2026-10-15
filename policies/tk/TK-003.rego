#
# TK-003
# Personal data sharing requires data sharing agreement
# GDPR Articles 5(1)(a), 6, and 28
#
# Checks whether a formal data-sharing agreement exists
# before personal data is shared with another party.
#
# Design-time rationale:
# Intended data sharing should be governed by documented
# agreements defining responsibilities and lawful processing.
#
# Outcome:
# FAIL when data sharing is planned without a sharing agreement.
#
package inspectr.tk.tk003

import rego.v1

# 1. Safely extract nodes from your input file
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

# 2. Helper Rule: Detect if ANY personal data is being processed in this workflow
pipeline_handles_personal_data if {
	some node in nodes
	node.type == "data_source"
	node.properties.contains_personal_data == true
}

# 3. Helper Rule: Is there a data transfer/export destination step planned?
pipeline_performs_transfer if {
	some node in nodes
	node.type == "data_transfer"
}

# 4. Helper Rule: Find compliance gates in the blueprint
compliance_gates := [gate | some gate in nodes; gate.type == "compliance_gate"]

# 5. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: FAIL if personal data is being transferred, but ANY compliance gate missing a DSA
	pipeline_handles_personal_data
	pipeline_performs_transfer
	some gate in compliance_gates
	gate.properties.data_sharing_agreement_exists == false

	final_report := {
		"rule": "TK-003",
		"status": "FAIL",
		"legal_reference": "GDPR Articles 5, 6, and 28",
		"reason": "Personal data sharing is planned, but a valid Data Sharing Agreement (DSA) has not been verified.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.data_sharing_agreement_exists", [gate.id]),
					"observed": false,
					"expected": true,
					"condition": "Cross-boundary municipal data transfer mandates a signed and documented data sharing agreement."
				}
			],
			"derived_evidence": {
				"sharing_requires_agreement": true,
				"agreement_exists": false
			}
		},
		"remedy": "Draft, execute, and document a formal Data Sharing Agreement with the recipient, then update your compliance gate properties to 'data_sharing_agreement_exists: true'."
	}
}

else := final_report if {
	# Path B: PASS if personal data transfer is planned, and a compliance gate verifies the DSA exists
	pipeline_handles_personal_data
	pipeline_performs_transfer
	some gate in compliance_gates
	gate.properties.data_sharing_agreement_exists == true

	final_report := {
		"rule": "TK-003",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5, 6, and 28",
		"reason": "Data sharing agreement is verified and present within the compliance gateway configuration.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.data_sharing_agreement_exists", [gate.id]),
					"observed": true,
					"expected": true,
					"condition": "Data sharing agreement explicitly tracks and satisfies legal transfer protocols."
				}
			],
			"derived_evidence": {
				"sharing_requires_agreement": true,
				"agreement_exists": true,
				"validated_gate_id": gate.id
			}
		},
		"remedy": null
	}
}

else := final_report if {
	# Path C: PASS automatically if no data transfer/sharing occurs, or if no personal data is involved
	not data_sharing_triggered

	final_report := {
		"rule": "TK-003",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5, 6, and 28",
		"reason": "Pipeline design context does not route personal data across organizational boundaries. A formal DSA is not required.",
		"evidence": {
			"input_evidence": [],
			"derived_evidence": {
				"sharing_requires_agreement": false,
				"agreement_exists": false
			}
		},
		"remedy": null
	}
}

# Helper rule to determine if the conditions for sharing checks are met
data_sharing_triggered if {
	pipeline_handles_personal_data
	pipeline_performs_transfer
}
