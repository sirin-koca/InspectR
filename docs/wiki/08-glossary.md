# 8 · Glossary

[← Testing and tooling](07-testing-and-tooling.md) · [Wiki home](README.md)

Terms used across the code, the policies and these pages. The core definitions follow the Terminology table in the root `README.md` and the status model in `src/catalog.py`.

## Project and case

| Term | Meaning |
|---|---|
| **InspectR** | Design-time compliance inspection tool for data-pipeline blueprints. It is the MSc thesis artefact (Design Science Research) at the Department of Informatics, University of Oslo, built in collaboration with SINTEF within DataPACT. |
| **DataPACT** | The research project the work is part of. The Sickleave scenario is taken from DataPACT deliverable D5.1 §3.7. |
| **SINTEF** | Norwegian research institute and collaborator; several supervisors are from SINTEF. |
| **TK** | Trondheim Kommune, the municipality of Trondheim and the case owner. Also the prefix of the rule IDs (`TK-R1` …) and the policy directory `policies/tk/`. |
| **MUNDAT** | Trondheim Kommune's municipal data-sharing case used as the evaluation case. |
| **Sickleave scenario** | The MUNDAT scenario modelled in the V2 blueprint. A research dataset is built from health-services and citizen-registry sources, integrated, anonymised and shared with an external recipient. |
| **inLUMEN** | Pipeline design tool, including a Pipeline Copilot, used to generate the raw TK pipeline (`tk-uc/inlumen-tk-uc.json`) and its provenance exports. |
| **PoC** | Proof of concept. Iteration 1 of InspectR; its boundary is set out in `PoC.md`. |
| **RQ1 / RQ2 / RQ3** | Research questions: RQ1 evidence model (what a blueprint must contain for inspection, and how much tooling can derive), RQ2 architecture (reuse across use cases and blueprint formats), RQ3 evaluation (reliability, explainability and efficiency compared with manual expert review). |
| **AC1–AC8** | Acceptance criteria for the PoC, listed in `src/catalog.py` (`ACCEPTANCE`) and on the Validation page. |
| **D1–D5** | Defects found in the v1 rule set and fixed or addressed in `tk-v2.0`. See [Rego policies](04-rego-policies.md#defects-d1d5). |

## Policy and law

| Term | Meaning |
|---|---|
| **Policy-as-Code (PaC)** | Executable representation of policy conditions. Here: Rego evaluated by OPA. |
| **OPA** | Open Policy Agent, a general-purpose policy engine. InspectR runs the `opa` binary as a subprocess (`opa eval`). It is located through `OPA_PATH`, `PATH`, or `C:\Tools\OPA\opa.exe`. |
| **Rego** | OPA's declarative policy language. InspectR's rules are in `policies/tk/*.rego` and use `import rego.v1`. |
| **`opa eval` / `opa test`** | OPA commands to evaluate a query against input, and to run Rego unit tests. |
| **Manifest** | `data.inspectr.manifest` in `policies/tk/policy.rego`: the list of rules (`id`, `query`, `legal_reference`) that the evaluator runs one by one. |
| **Rule set** | The versioned set of rules. The current one is `tk-v2.0` (TK-R1, TK-R2, TK-R3); v1 had TK-001 … TK-006. |
| **GDPR** | General Data Protection Regulation (EU) 2016/679. All three current rules reference GDPR articles. |
| **DPIA** | Data Protection Impact Assessment (GDPR Art. 35). TK-R1 checks that a DPIA checkpoint and a risk-assessment checkpoint are declared when special-category data is processed. |
| **Special-category data** | Personal data under GDPR Art. 9, such as health data. Here it is declared by `contains_special_category_data`. |
| **Lineage** | Record of where integrated data came from. TK-R2 (GDPR Art. 5(2), Art. 30) checks `lineage_record_defined` on integration nodes. |
| **Purpose compatibility** | Whether further processing is compatible with the original purpose (GDPR Art. 5(1)(b), Art. 6(4)). TK-R3 checks that it has been declared and then always asks for human review. |
| **EU AI Act (AIA)** | Regulation (EU) 2024/1689. Target of the earliest prototype (`assets/aia_poc_rules.json`, `Logg.md`), not of the current rule set. |

## Blueprint and evidence

| Term | Meaning |
|---|---|
| **Blueprint** | Machine-readable description of a planned pipeline: `pipeline.nodes` (each with `id`, `type`, `properties`) and `pipeline.connections`. See [Data and blueprints](06-data-and-blueprints.md). |
| **Enriched blueprint** | A blueprint with compliance facts added by hand, such as `data/tk_mundat_data_sharing_v2.json`. |
| **Raw export** | A blueprint as the tooling exports it, without compliance facts (`tk-uc/inlumen-tk-uc.json`). |
| **Enrichment gap** | What has to be added to a raw export before it can be inspected; an RQ1 finding. |
| **Adapter** | Planned component that maps native exports to InspectR's evidence model (RQ2, AC1). Not implemented in iteration 1. |
| **Intermediate representation (IR)** | Normalised model between blueprint and rules. Deliberately left out of the PoC; the blueprint goes directly to OPA. |
| **Node type** | The `type` field of a node. The rules read `data_source`, `compliance_gate`, `data_integration` and `data_transfer`. |
| **Compliance gate** | A planned assessment or approval point (`type: compliance_gate`). Declaring it does not establish enforcement. |
| **Trigger** | The fact that makes a rule's obligation apply (e.g. special-category data for TK-R1). |
| **Obligation** | What the requirement demands once triggered. |
| **Control** | A safeguard in the design intended to meet the obligation (e.g. `dpia_checkpoint_defined`). |
| **Undetermined** | No usable evidence for a fact: absent, `null`, or not a JSON boolean (`lib.not_usable`). Always leads to `UNKNOWN`, never `PASS` or `NOT_APPLICABLE`. |
| **Evidence** | The blueprint observations and derived facts a result is based on. Each item has a JSONPath-like `selector`, an `observed` value and a role. |
| **Selector** | Path to the property that was read, e.g. `$.pipeline.nodes[?(@.id=='dpia_check')].properties.dpia_checkpoint_defined`. |
| **Decision row** | The row of a rule's decision table that produced the result (`decision_row`). It is reported in the result and checked by the Rego tests. |
| **Design time** | Before the pipeline is run. InspectR checks what the design declares, not how it behaves at runtime. |

## Results and statuses

| Term | Meaning |
|---|---|
| **Result** | One object per rule with `rule`, `status`, `legal_reference`, `reason`, `evidence`, `remedy` (plus `decision_row` from Rego). |
| **`PASS`** | The obligation applies and the blueprint declares every required control as true. A design-level result, not a certificate of legal compliance. |
| **`FAIL`** | The obligation applies and the blueprint declares a required control as false (for TK-R1, also when no compliance gate exists). |
| **`UNKNOWN`** | A fact the rule needs is undetermined: absent, null, or not a boolean. |
| **`HUMAN`** | Everything checkable is declared, but the final decision is a legal judgement (TK-R3 always ends here when declared). |
| **`NOT_APPLICABLE`** | The trigger facts are declared false, so the obligation does not apply. |
| **`ERROR`** | InspectR could not evaluate the rule (technical fault). It is not a finding about the blueprint, and other rules are still reported. |
| **`InputError`** | Raised by `src/evaluator.py` when the blueprint does not have the minimum shape; no rule is run. |
| **Scenario (S0–S6)** | Predefined variants of the blueprint with expected statuses (`src/scenarios.py`), used on the Inspect and Validation pages and in the tests. |

## Tools and UI

| Term | Meaning |
|---|---|
| **Streamlit** | Python web framework used for the UI (`streamlit run app.py`). |
| **Graphviz** | Graph language used to draw the architecture and pipeline diagrams (`st.graphviz_chart`). |
| **pytest** | Python test runner used for the integration tests (`pytest tests -v`). |
| **Mermaid** | Diagram syntax used in these wiki pages; GitHub renders it. |
