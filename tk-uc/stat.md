## Executive Summary

**InspectR** is a proof of concept for **design-time compliance inspection of data-pipeline blueprints**. It addresses the TK/MUNDAT municipal data-sharing case by translating selected GDPR and organisational requirements into explicit, machine-checkable design controls.

InspectR combines a planned pipeline’s **data schema, processing manifest, and infrastructure metadata** into a unified JSON blueprint. The blueprint is evaluated directly by **Open Policy Agent (OPA)** using six **Rego** rules. The system produces explainable rule-level results with evidence, reasoning, and remediation guidance:

- **PASS** — the required design control is declared, or the rule is not triggered;
- **FAIL** — an applicable required control is explicitly missing or disabled;
- **HUMAN** — the available blueprint evidence is insufficient for an automated conclusion.

The PoC includes metadata-catalogue and lineage references to support traceability, but it does not validate the catalogue contents, runtime behaviour, legal adequacy, or completed organisational processes. A successful result therefore indicates that a defined design-time checkpoint is present—not that the pipeline is legally compliant or operationally secure.

### Current status

The PoC is operational and validated for the TK/MUNDAT Sickleave scenario. Its six active rules currently produce:

| Rule | Current result |
|---|---|
| TK-001 — DPIA checkpoint | PASS |
| TK-002 — Risk-assessment checkpoint | PASS |
| TK-003 — Data-sharing agreement checkpoint | PASS |
| TK-004 — Lineage record | PASS |
| TK-005 — Purpose compatibility | HUMAN |
| TK-006 — Sharing safeguards | PASS |

The current implementation successfully demonstrates **evidence-bound, explainable, repeatable design-time inspection**, while remaining intentionally limited in scope and not representing a complete GDPR compliance system.