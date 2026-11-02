#
# InspectR shared helpers (TK rule set v2)
#
# Every rule reads blueprint facts through these helpers so that
# "absent", "null" and "wrong type" are handled the same way everywhere.
#
package inspectr.lib

import rego.v1

# Marker shown as the observed value when a field is not in the blueprint.
absent := "<absent>"

# All nodes of the blueprint. Input structure is validated in evaluator.py,
# so an empty list here only occurs for a blueprint with no nodes.
nodes := object.get(object.get(input, "pipeline", {}), "nodes", [])

nodes_of_type(t) := [n | some n in nodes; n.type == t]

props(node) := object.get(node, "properties", {})

# Observed value of a property, or the absent marker.
observed(node, field) := object.get(props(node), field, absent)

has_field(node, field) if {
	object.get(props(node), field, absent) != absent
}

# A fact is usable only if it is a real JSON boolean.
# Missing, null, "true", 1 etc. are not usable evidence.
is_true(node, field) if props(node)[field] == true

is_false(node, field) if props(node)[field] == false

not_usable(node, field) if not is_boolean(object.get(props(node), field, absent))

selector(node, field) := sprintf("pipeline.nodes[id==\"%s\"].properties.%s", [node.id, field])

evidence(node, field, expected, condition) := {
	"selector": selector(node, field),
	"observed": observed(node, field),
	"expected": expected,
	"condition": condition,
}
