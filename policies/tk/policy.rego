#
# InspectR TK rule set v2 : manifest and aggregator
#
# evaluator.py reads `manifest` and queries each rule's `result` separately,
# so a broken rule becomes ERROR for that rule only and the other results
# are kept. `results` is kept for direct use with `opa eval`.
#
package inspectr

import rego.v1

rule_set_version := "tk-v2.0"

manifest := [
	{"id": "TK-R1", "query": "data.inspectr.tk.r1.result", "legal_reference": data.inspectr.tk.r1.legal_reference},
	{"id": "TK-R2", "query": "data.inspectr.tk.r2.result", "legal_reference": data.inspectr.tk.r2.legal_reference},
	{"id": "TK-R3", "query": "data.inspectr.tk.r3.result", "legal_reference": data.inspectr.tk.r3.legal_reference},
]

results := [
	data.inspectr.tk.r1.result,
	data.inspectr.tk.r2.result,
	data.inspectr.tk.r3.result,
]
