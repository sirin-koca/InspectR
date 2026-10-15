package inspectr.tk.tk006

import rego.v1

nodes := object.get(
	object.get(input, "pipeline", {}),
	"nodes",
	[]
)

node_by_id := {node.id: node | some node in nodes; node.id != null}

dpia_properties := object.get(
	object.get(node_by_id, "dpia_check", {}),
	"properties",
	{}
)

sharing_properties := object.get(
	object.get(node_by_id, "sharing_assessment", {}),
	"properties",
	{}
)

transfer_properties := object.get(
	object.get(node_by_id, "share_dataset", {}),
	"properties",
	{}
)

input_evidence := [
	{
		"selector": "pipeline.nodes[id==\"dpia_check\"].properties.dpia_completed",
		"observed": object.get(dpia_properties, "dpia_completed", null),
		"expected": true,
		"condition": "The DPIA must be completed before the sharing workflow proceeds."
	},
	{
		"selector": "pipeline.nodes[id==\"dpia_check\"].properties.risk_assessment_completed",
		"observed": object.get(dpia_properties, "risk_assessment_completed", null),
		"expected": true,
		"condition": "The risk assessment must be completed for the sharing workflow."
	},
	{
		"selector": "pipeline.nodes[id==\"sharing_assessment\"].properties.data_sharing_agreement_exists",
		"observed": object.get(sharing_properties, "data_sharing_agreement_exists", null),
		"expected": true,
		"condition": "A verified data-sharing agreement must exist before transfer."
	},
	{
		"selector": "pipeline.nodes[id==\"sharing_assessment\"].properties.recipient_approved",
		"observed": object.get(sharing_properties, "recipient_approved", null),
		"expected": true,
		"condition": "The intended recipient must be explicitly approved."
	},
	{
		"selector": "pipeline.nodes[id==\"share_dataset\"].properties.encrypted_in_transit",
		"observed": object.get(transfer_properties, "encrypted_in_transit", null),
		"expected": true,
		"condition": "The dataset must be encrypted while it is transferred."
	}
]

failed_controls := [
	control["selector"] |
	some control in input_evidence
	control["observed"] != control["expected"]
]

all_controls_present := count(failed_controls) == 0

derived_evidence := {
	"security_controls_complete": all_controls_present,
	"verified_control_count": count(input_evidence) - count(failed_controls),
	"required_control_count": count(input_evidence),
	"failed_controls": failed_controls
}

article := {
	"rule": "TK-006",
	"status": "FAIL",
	"legal_reference": "GDPR Articles 25 and 32",
	"reason": "One or more required sharing safeguards are missing, false, or incomplete.",
	"evidence": {
		"input_evidence": input_evidence,
		"derived_evidence": derived_evidence
	},
	"remedy": "Correct every control reported with an observed value other than true, then re-evaluate the blueprint."
} if {
	not all_controls_present

} else := {
	"rule": "TK-006",
	"status": "PASS",
	"legal_reference": "GDPR Articles 25 and 32",
	"reason": "All required sharing safeguards are explicitly documented in the blueprint.",
	"evidence": {
		"input_evidence": input_evidence,
		"derived_evidence": derived_evidence
	},
	"remedy": null
} if {
	all_controls_present
}