#
# One test per decision-table row of TK-R1, TK-R2 and TK-R3.
# Run: opa test policies/tk -v
#
package inspectr.tk.rules_test

import data.inspectr.tk.r1
import data.inspectr.tk.r2
import data.inspectr.tk.r3
import rego.v1

bp(nodes) := {"pipeline": {"nodes": nodes}}

src(id, props) := {"id": id, "type": "data_source", "properties": props}

gate(id, props) := {"id": id, "type": "compliance_gate", "properties": props}

integ(id, props) := {"id": id, "type": "data_integration", "properties": props}

transfer := {"id": "share", "type": "data_transfer", "properties": {}}

sensitive := src("hs", {"contains_personal_data": true, "contains_special_category_data": true})

ordinary := src("reg", {"contains_personal_data": true, "contains_special_category_data": false})

non_personal := src("iot", {"contains_personal_data": false, "contains_special_category_data": false})

dpia_ok := gate("dpia", {"dpia_checkpoint_defined": true, "risk_assessment_checkpoint_defined": true})

check(res, status, row) if {
	res.status == status
	res.decision_row == row
}

# ---------------- TK-R1 ----------------

test_r1_row1_trigger_missing if {
	check(r1.result, "UNKNOWN", 1) with input as bp([src("hs", {}), dpia_ok])
}

test_r1_row1_trigger_wrong_type if {
	check(r1.result, "UNKNOWN", 1) with input as bp([src("hs", {"contains_special_category_data": "true"}), dpia_ok])
}

test_r1_row1_trigger_null if {
	check(r1.result, "UNKNOWN", 1) with input as bp([src("hs", {"contains_special_category_data": null}), dpia_ok])
}

test_r1_row1_no_sources if {
	check(r1.result, "UNKNOWN", 1) with input as bp([dpia_ok])
}

test_r1_row2_all_false if {
	check(r1.result, "NOT_APPLICABLE", 2) with input as bp([ordinary, non_personal])
}

test_r1_row3_no_gate if {
	check(r1.result, "FAIL", 3) with input as bp([sensitive])
}

test_r1_row4_dpia_false if {
	check(r1.result, "FAIL", 4) with input as bp([sensitive, gate("g", {"dpia_checkpoint_defined": false, "risk_assessment_checkpoint_defined": true})])
}

test_r1_row4_risk_false if {
	check(r1.result, "FAIL", 4) with input as bp([sensitive, gate("g", {"dpia_checkpoint_defined": true, "risk_assessment_checkpoint_defined": false})])
}

test_r1_row5_pass if {
	check(r1.result, "PASS", 5) with input as bp([sensitive, ordinary, dpia_ok])
}

# A true trigger on one source decides applicability even if another source is unclear.
test_r1_row5_true_beats_missing_elsewhere if {
	check(r1.result, "PASS", 5) with input as bp([sensitive, src("x", {}), dpia_ok])
}

# Gates without the control fields are ignored (the old TK-005 defect class).
test_r1_row5_unrelated_gate_ignored if {
	check(r1.result, "PASS", 5) with input as bp([sensitive, dpia_ok, gate("share_gate", {"purpose_compatibility_declared": true})])
}

test_r1_row6_control_missing if {
	check(r1.result, "UNKNOWN", 6) with input as bp([sensitive, gate("g", {"dpia_checkpoint_defined": true})])
}

test_r1_row6_gate_without_fields if {
	check(r1.result, "UNKNOWN", 6) with input as bp([sensitive, gate("g", {})])
}

# The removed-field case that used to wipe out every result (defect D1).
test_r1_row6_control_removed_from_v2_shape if {
	check(r1.result, "UNKNOWN", 6) with input as bp([sensitive, gate("dpia_check", {"risk_assessment_checkpoint_defined": true})])
}

# ---------------- TK-R2 ----------------

test_r2_row2_no_integration if {
	check(r2.result, "NOT_APPLICABLE", 2) with input as bp([sensitive])
}

test_r2_row3_false if {
	check(r2.result, "FAIL", 3) with input as bp([integ("i1", {"lineage_record_defined": true}), integ("i2", {"lineage_record_defined": false})])
}

test_r2_row4_missing if {
	check(r2.result, "UNKNOWN", 4) with input as bp([integ("i1", {})])
}

test_r2_row4_wrong_type if {
	check(r2.result, "UNKNOWN", 4) with input as bp([integ("i1", {"lineage_record_defined": "yes"})])
}

test_r2_row5_pass if {
	check(r2.result, "PASS", 5) with input as bp([integ("i1", {"lineage_record_defined": true}), integ("i2", {"lineage_record_defined": true})])
}

# ---------------- TK-R3 ----------------

purpose_gate(v) := gate("share_gate", {"purpose_compatibility_declared": v})

test_r3_row1_personal_flag_missing if {
	check(r3.result, "UNKNOWN", 1) with input as bp([src("x", {}), transfer, purpose_gate(true)])
}

test_r3_row1_no_sources if {
	check(r3.result, "UNKNOWN", 1) with input as bp([transfer, purpose_gate(true)])
}

test_r3_row2_no_transfer if {
	check(r3.result, "NOT_APPLICABLE", 2) with input as bp([sensitive, purpose_gate(true)])
}

test_r3_row2_no_personal_data if {
	check(r3.result, "NOT_APPLICABLE", 2) with input as bp([non_personal, transfer])
}

test_r3_row3_false if {
	check(r3.result, "FAIL", 3) with input as bp([ordinary, transfer, purpose_gate(false)])
}

test_r3_row4_no_gate_carries_field if {
	check(r3.result, "UNKNOWN", 4) with input as bp([ordinary, transfer, dpia_ok])
}

test_r3_row4_wrong_type if {
	check(r3.result, "UNKNOWN", 4) with input as bp([ordinary, transfer, purpose_gate("true")])
}

test_r3_row5_human if {
	check(r3.result, "HUMAN", 5) with input as bp([ordinary, transfer, purpose_gate(true)])
}

# The V2 demo defect: a DPIA gate without the purpose field no longer forces HUMAN by accident,
# and the result is HUMAN only because the sharing gate declares true.
test_r3_row5_dpia_gate_ignored if {
	check(r3.result, "HUMAN", 5) with input as bp([sensitive, transfer, dpia_ok, purpose_gate(true)])
}

# There is no PASS path in TK-R3.
test_r3_never_pass if {
	r3.result.status != "PASS" with input as bp([ordinary, transfer, purpose_gate(true)])
}
