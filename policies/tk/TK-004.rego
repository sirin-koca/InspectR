#
# RULE 4
# Data lineage must exist for integrated datasets
#
# TK-004
# GDPR Articles 5(2) and 30
#
# Checks whether integrated datasets provide lineage
# and provenance information.
#
# Design-time rationale:
# Traceability supports accountability, auditing,
# record-keeping, and transparency obligations.
#
# Outcome:
# FAIL when dataset lineage information is missing.
#

package inspectr.tk.tk004

import rego.v1

# 1. Safely extract nodes from your input file
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

# 2. Helper Rule: Find integration processing stages in the graph
integration_nodes := [node | some node in nodes; node.type == "data_integration"]

# 3. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: FAIL if any integration node exists but is missing lineage or provenance properties
	some integration_node in integration_nodes
	integration_node.properties.lineage_available == false

	final_report := {
		"rule": "TK-004",
		"status": "FAIL",
		"legal_reference": "GDPR Articles 5(2) and 30",
		"reason": sprintf("Dataset lineage or provenance traceability information is missing on integration step '%s'.", [integration_node.id]),
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.lineage_available", [integration_node.id]),
					"observed": false,
					"expected": true,
					"condition": "Traceability metrics must be present to fulfill GDPR accountability and auditing frameworks."
				}
			],
			"derived_evidence": {
				"lineage_available": false,
				"provenance_recorded": false
			}
		},
		"remedy": sprintf("Configure your integration pipelines to record data flows, then set 'lineage_available: true' on node '%s'.", [integration_node.id])
	}
}

else := final_report if {
	# Path B: PASS if data integration steps exist and successfully verify tracking parameters
	count(integration_nodes) > 0
	some integration_node in integration_nodes
	integration_node.properties.lineage_available == true

	final_report := {
		"rule": "TK-004",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5(2) and 30",
		"reason": "Lineage and provenance traceability records are fully mapped and available for compliance auditing.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.lineage_available", [integration_node.id]),
					"observed": true,
					"expected": true,
					"condition": "Data lineage configurations are active and verifying pipeline flows."
				}
			],
			"derived_evidence": {
				"lineage_available": true,
				"auditable_nodes": count(integration_nodes)
			}
		},
		"remedy": null
	}
}

else := final_report if {
	# Path C: PASS automatically if no structural data integration transformations are occurring
	count(integration_nodes) == 0

	final_report := {
		"rule": "TK-004",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5(2) and 30",
		"reason": "No discrete multi-source data integration nodes are declared in this workflow blueprint. Lineage checks are bypassed.",
		"evidence": {
			"input_evidence": [],
			"derived_evidence": {
				"lineage_available": true
			}
		},
		"remedy": null
	}
}
