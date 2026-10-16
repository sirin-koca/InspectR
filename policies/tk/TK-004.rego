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

lineage_record_value(node) := object.get(
	object.get(node, "properties", {}),
	"lineage_record_defined",
	object.get(object.get(node, "properties", {}), "lineage_available", null)
)

# 3. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: FAIL if any integration node lacks a defined lineage record
	some integration_node in integration_nodes
	lineage_record_value(integration_node) == false

	final_report := {
		"rule": "TK-004",
		"status": "FAIL",
		"legal_reference": "GDPR Articles 5(2) and 30",
		"reason": sprintf("The integration design does not define a lineage record on step '%s'.", [integration_node.id]),
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.lineage_record_defined", [integration_node.id]),
					"observed": lineage_record_value(integration_node),
					"expected": true,
					"condition": "An integration design must identify a lineage record for traceable processing."
				}
			],
			"derived_evidence": {
				"lineage_record_defined": false,
				"provenance_recorded": false
			}
		},
		"remedy": sprintf("Define the catalogue-backed lineage record for integration node '%s' and set 'lineage_record_defined: true'.", [integration_node.id])
	}
}

else := final_report if {
	# Path B: PASS if data integration steps exist and successfully verify tracking parameters
	count(integration_nodes) > 0
	some integration_node in integration_nodes
	lineage_record_value(integration_node) == true

	final_report := {
		"rule": "TK-004",
		"status": "PASS",
		"legal_reference": "GDPR Articles 5(2) and 30",
		"reason": "The integration design identifies a lineage record for traceable processing.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.lineage_record_defined", [integration_node.id]),
					"observed": lineage_record_value(integration_node),
					"expected": true,
					"condition": "The planned integration includes a defined lineage record."
				}
			],
			"derived_evidence": {
				"lineage_record_defined": true,
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
				"lineage_record_defined": true
			}
		},
		"remedy": null
	}
}
