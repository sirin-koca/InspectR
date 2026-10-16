#
# TK-003 : data-sharing agreement checkpoint
#
# Personal data sharing requires data sharing agreement
# GDPR Articles 5(1)(a), 6, and 28
#
# Checks whether the design defines a data-sharing agreement checkpoint
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

agreement_checkpoint_value(gate) := object.get(
	object.get(gate, "properties", {}),
	"data_sharing_agreement_checkpoint_defined",
	object.get(object.get(gate, "properties", {}), "data_sharing_agreement_exists", null)
)

# 5. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: FAIL if personal data is being transferred, but ANY compliance gate missing a DSA
	pipeline_handles_personal_data
	pipeline_performs_transfer
	some gate in compliance_gates
	agreement_checkpoint_value(gate) == false

	final_report := {
		"rule": "TK-003",
		"status": "FAIL",
		"legal_reference": "GDPR Articles 5, 6, and 28",
		"reason": "Personal-data transfer is planned, but the blueprint does not define a data-sharing agreement checkpoint.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.data_sharing_agreement_checkpoint_defined", [gate.id]),
					"observed": agreement_checkpoint_value(gate),
					"expected": true,
					"condition": "A planned cross-boundary transfer requires a data-sharing agreement checkpoint."
				}
			],
			"derived_evidence": {
				"sharing_requires_agreement": true,
				"agreement_checkpoint_defined": false
			}
		},
		"remedy": "Define a data-sharing agreement checkpoint with the recipient and set 'data_sharing_agreement_checkpoint_defined: true' on the compliance gate."
	}
}

else := final_report if {
	# Path B: PASS if personal-data transfer is planned and a gate defines a DSA checkpoint
	pipeline_handles_personal_data
	pipeline_performs_transfer
	some gate in compliance_gates
	agreement_checkpoint_value(gate) == true

	final_report := {
		"rule": "TK-003",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5, 6, and 28",
		"reason": "The blueprint includes a data-sharing agreement checkpoint for the planned transfer.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.data_sharing_agreement_checkpoint_defined", [gate.id]),
					"observed": agreement_checkpoint_value(gate),
					"expected": true,
					"condition": "The planned transfer includes a data-sharing agreement checkpoint."
				}
			],
			"derived_evidence": {
				"sharing_requires_agreement": true,
				"agreement_checkpoint_defined": true,
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
				"agreement_checkpoint_defined": false
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
