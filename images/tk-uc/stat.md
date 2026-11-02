## Executive Summary

**InspectR** is a proof of concept for **design-time compliance inspection of data-pipeline blueprints**. It addresses the TK/MUNDAT municipal data-sharing case by translating selected GDPR and organisational requirements into explicit, machine-checkable design controls.

InspectR combines a planned pipeline’s **data schema, processing manifest, and infrastructure metadata** into a unified JSON blueprint. The blueprint is evaluated directly by **Open Policy Agent (OPA)** using three **Rego** rules (rule set `tk-v2.0`). The system produces explainable rule-level results with evidence, reasoning, and remediation guidance:

- **PASS** — the obligation applies and the required design control is declared;
- **FAIL** — the obligation applies and a required control is declared absent;
- **UNKNOWN** — a fact the rule needs is undetermined (absent, null, or not a boolean);
- **HUMAN** — everything checkable is declared, but the decision is a legal judgement;
- **NOT_APPLICABLE** — the trigger facts are declared false, so the obligation does not apply;
- **ERROR** — InspectR could not evaluate the rule (a tool fault, not a finding).

The PoC includes metadata-catalogue and lineage references to support traceability, but it does not validate the catalogue contents, runtime behaviour, legal adequacy, or completed organisational processes. A successful result therefore indicates that a defined design-time checkpoint is present—not that the pipeline is legally compliant or operationally secure.

### Current status

The PoC is operational and validated for the TK/MUNDAT Sickleave scenario. On `data/tk_mundat_data_sharing_v2.json` its three active rules currently produce:

| Rule | Current result |
|---|---|
| TK-R1 — DPIA and risk-assessment checkpoint | PASS |
| TK-R2 — Lineage record for integrated data | PASS |
| TK-R3 — Purpose compatibility before sharing | HUMAN |

The current implementation successfully demonstrates **evidence-bound, explainable, repeatable design-time inspection**, while remaining intentionally limited in scope and not representing a complete GDPR compliance system.