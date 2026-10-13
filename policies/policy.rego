package inspectr

# InspectR PoC Policy-as-Code for the Trondheim Kommune MUNDAT use case.
# These rules check structural and declared design-time evidence in the
# pipeline blueprint. They do not determine legal compliance.

import rego.v1

nodes := object.get(
    object.get(input, "pipeline", {}),
    "nodes",
    []
)

required_stages := {
    "tk_request_intake",
    "validate_request",
    "retrieve_relevant_data",
    "process_data_for_compliance",
    "run_compliance_checks",
    "prepare_sharing_decision",
    "tk_decision_output"
}

node_labels := {node.label | some node in nodes}
missing_stages := required_stages - node_labels

connections := object.get(
    object.get(input, "pipeline", {}),
    "connections",
    []
)

node_labels_by_id := {node.id: node.label | some node in nodes}

actual_edges := {
    sprintf("%s>%s", [
        node_labels_by_id[edge.from.node],
        node_labels_by_id[edge.to.node]
    ]) |
    some edge in connections
}

expected_edges := {
    "tk_request_intake>validate_request",
    "validate_request>retrieve_relevant_data",
    "retrieve_relevant_data>process_data_for_compliance",
    "process_data_for_compliance>run_compliance_checks",
    "run_compliance_checks>prepare_sharing_decision",
    "prepare_sharing_decision>tk_decision_output"
}

flow_valid if {
    count(nodes) == count(required_stages)
    count(missing_stages) == 0
    actual_edges == expected_edges
}

article_structure := {
    "rule": "TK-STRUCT-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT pipeline structure",
    "reason": "The blueprint does not contain the required TK compliance-flow stages and connections.",
    "evidence": {
        "input_evidence": [
            {
                "selector": "pipeline.nodes[*].label",
                "observed": [node.label | some node in nodes],
                "expected": [stage | stage := required_stages[_]],
                "condition": "All required TK stages are present."
            },
            {
                "selector": "pipeline.connections[*].from/to",
                "observed": actual_edges,
                "expected": expected_edges,
                "condition": "The six expected stage connections are present."
            }
        ],
        "derived_evidence": {
            "missing_stages": missing_stages,
            "flow_valid": false
        }
    },
    "remedy": "Add the missing TK stages and connect them in the documented intake-to-output order."
} if {
    count(missing_stages) > 0
} else := {
    "rule": "TK-STRUCT-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT pipeline structure",
    "reason": "The blueprint contains the required stages, but not in the documented order.",
    "evidence": {
        "input_evidence": [
            {
                "selector": "pipeline.nodes[*].label",
                "observed": [node.label | some node in nodes],
                "expected": [stage | stage := required_stages[_]],
                "condition": "All required TK stages are present."
            },
            {
                "selector": "pipeline.connections[*].from/to",
                "observed": actual_edges,
                "expected": expected_edges,
                "condition": "The six expected stage connections are present."
            }
        ],
        "derived_evidence": {
            "missing_stages": [],
            "flow_valid": false
        }
    },
    "remedy": "Connect the TK stages in the documented intake-to-output order."
} if {
    count(missing_stages) == 0
    not flow_valid
} else := {
    "rule": "TK-STRUCT-01",
    "status": "OK",
    "legal_reference": "MUNDAT pipeline structure",
    "reason": "The blueprint contains the seven documented TK compliance-flow stages and connections.",
    "evidence": {
        "input_evidence": [
            {
                "selector": "pipeline.nodes[*].label",
                "observed": [node.label | some node in nodes],
                "expected": [stage | stage := required_stages[_]],
                "condition": "All required TK stages are present."
            },
            {
                "selector": "pipeline.connections[*].from/to",
                "observed": actual_edges,
                "expected": expected_edges,
                "condition": "The six expected stage connections are present."
            }
        ],
        "derived_evidence": {
            "stages_checked": count(nodes),
            "flow_valid": true
        }
    },
    "remedy": null
} if {
    count(missing_stages) == 0
    flow_valid
}

logging_failures contains node.label if {
    some node in nodes
    object.get(object.get(node, "compliance_extensions", {}), "has_logging", false) != true
}

logging_evidence contains {
    "node_id": node.id,
    "node_label": node.label,
    "selector": sprintf("pipeline.nodes[id=%s].compliance_extensions.has_logging", [node.id]),
    "observed": object.get(object.get(node, "compliance_extensions", {}), "has_logging", null),
    "expected": true,
    "condition": "Every pipeline stage declares logging capability."
} if {
    some node in nodes
}

article_traceability := {
    "rule": "TK-TRACE-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT logging and traceability requirement",
    "reason": "One or more pipeline stages do not declare logging capability.",
    "evidence": {
        "input_evidence": logging_evidence,
        "derived_evidence": {
            "nodes_without_logging": logging_failures
        }
    },
    "remedy": "Declare logging capability for every pipeline stage and retain traceability of the request, data access, checks, and decision."
} if {
    count(logging_failures) > 0
} else := {
    "rule": "TK-TRACE-01",
    "status": "OK",
    "legal_reference": "MUNDAT logging and traceability requirement",
    "reason": "All pipeline stages declare design-time logging capability.",
    "evidence": {
        "input_evidence": logging_evidence,
        "derived_evidence": {
            "nodes_checked": count(nodes)
        }
    },
    "remedy": null
}

data_source_nodes contains node if {
    some node in nodes
    node.kind == "source"
}

source_evidence contains {
    "node_id": node.id,
    "node_label": node.label,
    "fields": [
        {
            "selector": sprintf("pipeline.nodes[id=%s].compliance_extensions.source_id", [node.id]),
            "observed": object.get(object.get(node, "compliance_extensions", {}), "source_id", null),
            "expected": "non-empty string",
            "condition": "The source is identified."
        },
        {
            "selector": sprintf("pipeline.nodes[id=%s].compliance_extensions.approved_source", [node.id]),
            "observed": object.get(object.get(node, "compliance_extensions", {}), "approved_source", null),
            "expected": true,
            "condition": "The source is marked approved."
        }
    ]
} if {
    some node in data_source_nodes
}

invalid_sources contains node.label if {
    some node in data_source_nodes
    ext := object.get(node, "compliance_extensions", {})
    object.get(ext, "source_id", "") == ""
}

invalid_sources contains node.label if {
    some node in data_source_nodes
    ext := object.get(node, "compliance_extensions", {})
    object.get(ext, "approved_source", false) != true
}

article_data_provenance := {
    "rule": "TK-DATA-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT data-source and provenance requirement",
    "reason": "A pipeline data source lacks a source identifier or is not marked as approved.",
    "evidence": {
        "input_evidence": source_evidence,
        "derived_evidence": {
            "invalid_sources": invalid_sources
        }
    },
    "remedy": "Declare the source identifier and approval status for each data-source node."
} if {
    count(invalid_sources) > 0
} else := {
    "rule": "TK-DATA-01",
    "status": "OK",
    "legal_reference": "MUNDAT data-source and provenance requirement",
    "reason": "Pipeline data sources provide declared provenance and approval evidence.",
    "evidence": {
        "input_evidence": source_evidence,
        "derived_evidence": {
            "data_sources_checked": count(data_source_nodes)
        }
    },
    "remedy": null
}

risk_check_nodes contains node.label if {
    some node in nodes
    node.label == "run_compliance_checks"
}

risk_check_evidence := [
    {
        "node_id": node.id,
        "node_label": node.label,
        "selector": sprintf("pipeline.nodes[id=%s].label", [node.id]),
        "observed": node.label,
        "expected": "run_compliance_checks",
        "condition": "A dedicated compliance and risk-assessment stage exists."
    } |
    some node in nodes
    node.label == "run_compliance_checks"
]

article_risk := {
    "rule": "TK-RISK-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT DPIA and risk-assessment requirement",
    "reason": "The blueprint does not contain a dedicated compliance and risk-assessment stage.",
    "evidence": {
        "input_evidence": risk_check_evidence,
        "derived_evidence": {
            "risk_check_stage_present": false
        }
    },
    "remedy": "Add a stage that performs the documented compliance, DPIA, and risk checks."
} if {
    count(risk_check_nodes) == 0
} else := {
    "rule": "TK-RISK-01",
    "status": "OK",
    "legal_reference": "MUNDAT DPIA and risk-assessment requirement",
    "reason": "The blueprint contains a dedicated compliance and risk-assessment stage.",
    "evidence": {
        "input_evidence": risk_check_evidence,
        "derived_evidence": {
            "risk_check_stage_present": true
        }
    },
    "remedy": null
}

decision_nodes contains node if {
    some node in nodes
    node.label == "prepare_sharing_decision"
}

missing_human_review contains node.label if {
    some node in decision_nodes
    ext := object.get(node, "compliance_extensions", {})
    object.get(ext, "human_oversight", null) == null
}

human_review_evidence := [
    {
        "node_id": node.id,
        "node_label": node.label,
        "selector": sprintf("pipeline.nodes[id=%s].compliance_extensions.human_oversight", [node.id]),
        "observed": object.get(object.get(node, "compliance_extensions", {}), "human_oversight", null),
        "expected": true,
        "condition": "The sharing decision stage declares human review."
    } |
    some node in decision_nodes
]

disabled_human_review contains node.label if {
    some node in decision_nodes
    ext := object.get(node, "compliance_extensions", {})
    object.get(ext, "human_oversight", null) == false
}

article_human_review := {
    "rule": "TK-HUMAN-01",
    "status": "FAIL",
    "legal_reference": "MUNDAT sharing-decision review requirement",
    "reason": "The sharing decision stage explicitly disables human review.",
    "evidence": {
        "input_evidence": human_review_evidence,
        "derived_evidence": {
            "components_without_human_review": disabled_human_review
        }
    },
    "remedy": "Provide a human approval or override step before sharing data."
} if {
    count(disabled_human_review) > 0
} else := {
    "rule": "TK-HUMAN-01",
    "status": "HUMAN",
    "legal_reference": "MUNDAT sharing-decision review requirement",
    "reason": "The blueprint contains a sharing decision stage but does not provide explicit human-review evidence.",
    "evidence": {
        "input_evidence": human_review_evidence,
        "derived_evidence": {
            "components_requiring_review": missing_human_review
        }
    },
    "remedy": "Declare human review or an override checkpoint before sharing data."
} if {
    count(disabled_human_review) == 0
    count(missing_human_review) > 0
} else := {
    "rule": "TK-HUMAN-01",
    "status": "OK",
    "legal_reference": "MUNDAT sharing-decision review requirement",
    "reason": "The sharing decision stage explicitly represents human review evidence.",
    "evidence": {
        "input_evidence": human_review_evidence,
        "derived_evidence": {
            "decision_stages_checked": count(decision_nodes)
        }
    },
    "remedy": null
} if {
    count(disabled_human_review) == 0
    count(missing_human_review) == 0
}

results := [
    article_structure,
    article_data_provenance,
    article_traceability,
    article_risk,
    article_human_review
]
