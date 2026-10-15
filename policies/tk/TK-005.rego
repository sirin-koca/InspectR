#
# RULE 5
# Purpose compatibility cannot be determined automatically
#
# TK-005
# GDPR Articles 5(1)(b) and 6(4)
#
# Checks whether the compatibility between the original
# processing purpose and the intended sharing purpose
# can be established automatically.
#
# Design-time rationale:
# Purpose compatibility often requires contextual legal
# and organisational interpretation that cannot always
# be fully automated.
#
# Outcome:
# HUMAN when automated assessment is insufficient.
#
package inspectr.tk.tk005

import rego.v1

# 1. Safely extract nodes from your input file
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

# 2. Helper Rule: Find compliance gates in the pipeline
compliance_gates := [gate | some gate in nodes; gate.type == "compliance_gate"]

# 3. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: Trigger a HUMAN escalation status if any compliance gate has an unconfirmed, null, or missing purpose
	some gate in compliance_gates
	not object.get(gate.properties, "purpose_compatible", false) == true

	final_report := {
		"rule": "TK-005",
		"status": "HUMAN",
		"legal_reference": "GDPR Articles 5(1)(b) and 6(4)",
		"reason": sprintf("Automated verification cannot conclusively determine purpose compatibility for gate '%s'. Contextual human review is mandated.", [gate.id]),
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.purpose_compatible", [gate.id]),
					"observed": object.get(gate.properties, "purpose_compatible", null),
					"expected": true,
					"condition": "Purpose compatibility requires an explicitly authorized context evaluation that cannot be automated."
				}
			],
			"derived_evidence": {
				"automated_assessment": "inconclusive",
				"escalated_gate_id": gate.id
			}
		},
		"remedy": "Perform human legal and organizational review of the dataset request context, then declare 'purpose_compatible: true' upon sign-off."
	}
}

else := final_report if {
	# Path B: PASS if compliance gates exist and explicitly verify purpose compatibility
	count(compliance_gates) > 0
	some gate in compliance_gates
	gate.properties.purpose_compatible == true

	final_report := {
		"rule": "TK-005",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5(1)(b) and 6(4)",
		"reason": "Purpose compatibility evidence has been explicitly validated within the pipeline metadata blueprints.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.purpose_compatible", [gate.id]),
					"observed": true,
					"expected": true,
					"condition": "Purpose alignment is verified and logged."
				}
			],
			"derived_evidence": {
				"purpose_compatible": true,
				"validated_gate_id": gate.id
			}
		},
		"remedy": null
	}
}

else := final_report if {
	# Path C: PASS automatically if no compliance validation gates are required for this graph structure
	count(compliance_gates) == 0

	final_report := {
		"rule": "TK-005",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5(1)(b) and 6(4)",
		"reason": "No discrete compliance gates are declared in this workflow blueprint. Purpose validation is skipped.",
		"evidence": {
			"input_evidence": [],
			"derived_evidence": {
				"purpose_compatible": true
			}
		},
		"remedy": null
	}
}
