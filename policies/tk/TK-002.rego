#
# TK-002 : risk-assessment checkpoint
#
# GDPR Articles 9 and 35
#
# Checks whether special category personal data is involved
# and requires a risk-assessment checkpoint in the design.
#
# Design-time rationale:
# Sensitive data processing introduces additional obligations
# and requires documented risk evaluation prior to implementation.
#
# Outcome:
# FAIL when special-category data is present and no risk-assessment checkpoint is defined.
#
package inspectr.tk.tk002

import rego.v1

# 1. Safely parse nodes array from your compliance blueprint JSON
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

# 2. Helper Rule: Find all data sources that process special category data
special_category_sources := [src | some src in nodes; src.type == "data_source"; src.properties.contains_special_category_data == true]

# 3. Helper Rule: Find any compliance gates in the pipeline
compliance_gates := [gate | some gate in nodes; gate.type == "compliance_gate"]

risk_checkpoint_value(gate) := object.get(
	object.get(gate, "properties", {}),
	"risk_assessment_checkpoint_defined",
	object.get(object.get(gate, "properties", {}), "risk_assessment_completed", null)
)

# 4. SINGLE COMPLETE RULE DEFINITION: Dynamic evaluation path routing
article := final_report if {
	# Path A: FAIL if special-category data exists but a gate lacks a risk-assessment checkpoint
	count(special_category_sources) > 0
	some gate in compliance_gates
	risk_checkpoint_value(gate) == false

	# Track down the specific offending source node for the UI evidence log
	some offending_source in special_category_sources

	final_report := {
		"rule": "TK-002",
		"status": "FAIL",
		"legal_reference": "GDPR Articles 9 and 35",
		"reason": sprintf("The design includes special-category data from source '%s' without a risk-assessment checkpoint.", [offending_source.id]),
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.contains_special_category_data", [offending_source.id]),
					"observed": true,
					"expected": true,
					"condition": "Source node introduces sensitive special category data into the workflow lifecycle."
				},
				{
					"selector": sprintf("pipeline.nodes[%s].properties.risk_assessment_checkpoint_defined", [gate.id]),
					"observed": risk_checkpoint_value(gate),
					"expected": true,
					"condition": "A planned risk-assessment checkpoint must accompany sensitive-data processing."
				}
			],
			"derived_evidence": {
				"special_category_data_present": true,
				"risk_assessment_checkpoint_defined": false
			}
		},
		"remedy": sprintf("Add a risk-assessment checkpoint for the '%s' workflow and set 'risk_assessment_checkpoint_defined: true' on the compliance gate.", [offending_source.id])
	}
}

else := final_report if {
	# Path B: PASS if special-category data exists and a gate defines a risk-assessment checkpoint
	count(special_category_sources) > 0
	some gate in compliance_gates
	risk_checkpoint_value(gate) == true

	some main_source in special_category_sources

	final_report := {
		"rule": "TK-002",
		"status": "PASS",
		"legal_reference": "GDPR Articles 9 and 35",
		"reason": "The blueprint includes a risk-assessment checkpoint for the declared sensitive-data processing.",
		"evidence": {
			"input_evidence": [
				{
					"selector": sprintf("pipeline.nodes[%s].properties.risk_assessment_checkpoint_defined", [gate.id]),
					"observed": risk_checkpoint_value(gate),
					"expected": true,
					"condition": "The planned pipeline includes a risk-assessment checkpoint for sensitive data."
				}
			],
			"derived_evidence": {
				"special_category_data_present": true,
				"risk_assessment_checkpoint_defined": true,
				"validated_source_id": main_source.id
			}
		},
		"remedy": null
	}
}

else := final_report if {
	# Path C: PASS automatically if no special category data is processed at all
	count(special_category_sources) == 0

	final_report := {
		"rule": "TK-002",
		"status": "PASS",
		"legal_reference": "GDPR Articles 9 and 35",
		"reason": "Data processing context does not handle sensitive special category data profiles. Risk assessment not mandated by this rule.",
		"evidence": {
			"input_evidence": [],
			"derived_evidence": {
				"special_category_data_present": false,
				"risk_assessment_checkpoint_defined": false
			}
		},
		"remedy": null
	}
}
