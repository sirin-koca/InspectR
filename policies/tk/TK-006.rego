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

dpia_checkpoint_value := object.get(dpia_properties, "dpia_checkpoint_defined", object.get(dpia_properties, "dpia_completed", null))
risk_checkpoint_value := object.get(dpia_properties, "risk_assessment_checkpoint_defined", object.get(dpia_properties, "risk_assessment_completed", null))
agreement_checkpoint_value := object.get(sharing_properties, "data_sharing_agreement_checkpoint_defined", object.get(sharing_properties, "data_sharing_agreement_exists", null))
recipient_checkpoint_value := object.get(sharing_properties, "recipient_approval_checkpoint_defined", object.get(sharing_properties, "recipient_approved", null))
encryption_configuration_value := object.get(transfer_properties, "encryption_in_transit_configured", object.get(transfer_properties, "encrypted_in_transit", null))

input_evidence := [
	{
		"selector": "pipeline.nodes[id==\"dpia_check\"].properties.dpia_checkpoint_defined",
		"observed": dpia_checkpoint_value,
		"expected": true,
		"condition": "The planned sharing workflow must define a DPIA checkpoint."
	},
	{
		"selector": "pipeline.nodes[id==\"dpia_check\"].properties.risk_assessment_checkpoint_defined",
		"observed": risk_checkpoint_value,
		"expected": true,
		"condition": "The planned sharing workflow must define a risk-assessment checkpoint."
	},
	{
		"selector": "pipeline.nodes[id==\"sharing_assessment\"].properties.data_sharing_agreement_checkpoint_defined",
		"observed": agreement_checkpoint_value,
		"expected": true,
		"condition": "The planned transfer must define a data-sharing agreement checkpoint."
	},
	{
		"selector": "pipeline.nodes[id==\"sharing_assessment\"].properties.recipient_approval_checkpoint_defined",
		"observed": recipient_checkpoint_value,
		"expected": true,
		"condition": "The planned transfer must define a recipient-approval checkpoint."
	},
	{
		"selector": "pipeline.nodes[id==\"share_dataset\"].properties.encryption_in_transit_configured",
		"observed": encryption_configuration_value,
		"expected": true,
		"condition": "The planned transfer must define encryption in transit."
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
	"defined_control_count": count(input_evidence) - count(failed_controls),
	"required_control_count": count(input_evidence),
	"failed_controls": failed_controls
}

article := {
	"rule": "TK-006",
	"status": "FAIL",
	"legal_reference": "GDPR Articles 25 and 32",
	"reason": "One or more required sharing checkpoints are missing or not defined in the design.",
	"evidence": {
		"input_evidence": input_evidence,
		"derived_evidence": derived_evidence
	},
	"remedy": "Define every checkpoint reported with an observed value other than true, then re-evaluate the blueprint."
} if {
	not all_controls_present

} else := {
	"rule": "TK-006",
	"status": "PASS",
	"legal_reference": "GDPR Articles 25 and 32",
	"reason": "All required sharing checkpoints are defined in the blueprint.",
	"evidence": {
		"input_evidence": input_evidence,
		"derived_evidence": derived_evidence
	},
	"remedy": null
} if {
	all_controls_present
}