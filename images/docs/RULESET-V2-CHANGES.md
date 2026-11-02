# InspectR TK Rule Set v2: What Was Fixed and Why

Rule set version: `tk-v2.0` (replaces TK-001 to TK-006). Date: 2 November 2026.

## Summary

The six TK rules were reduced to three rules and moved from three verdict statuses (PASS, FAIL, HUMAN) to six (adding UNKNOWN, NOT_APPLICABLE and ERROR). Every rule is now a complete decision table, so every possible input reaches exactly one status. Five defects were fixed. All of them could hide findings or produce a confident wrong verdict. Each rule now covers one kind of evidence:

| New rule | Replaces | Evidence class | Statuses it can produce |
|---|---|---|---|
| TK-R1 DPIA and risk-assessment checkpoint | TK-001, TK-002 | Manually declared | PASS, FAIL, UNKNOWN, NOT_APPLICABLE |
| TK-R2 Lineage record for integrated data | TK-004 | Derivable in future from inLUMEN runs | PASS, FAIL, UNKNOWN, NOT_APPLICABLE |
| TK-R3 Purpose compatibility before sharing | TK-005 | Human judgement | HUMAN, FAIL, UNKNOWN, NOT_APPLICABLE |

ERROR can come from any rule, but it is a fault in InspectR, not a verdict about the blueprint.

Reducing the rules was a research-quality decision. With three rules, each status can be tested exhaustively, and each rule stands for one evidence class. The thesis can then show what InspectR can do with declared, derivable and judgement-based evidence without repeating the same logic six times. TK-001 and TK-002 had the same trigger and differed only in the field they checked. TK-006 depended on hard-coded node IDs and mostly re-checked fields the other rules already check. TK-003 (data-sharing agreement) was dropped to keep the scope small. It can return as TK-R4 using the same structure as TK-R1.

## Status model

| Status | Meaning | Who acts |
|---|---|---|
| PASS | The obligation applies and the blueprint declares every required control as `true` | Nobody (design level only) |
| FAIL | The obligation applies and the blueprint declares a required control as `false` | Designer: add the control |
| UNKNOWN | A fact the rule needs is missing, `null` or not a boolean | Designer or inLUMEN: supply the fact |
| HUMAN | Everything checkable is declared, but the final decision is a legal judgement | Legal or domain expert |
| NOT_APPLICABLE | The trigger facts are present and `false`, so the obligation does not apply | Nobody |
| ERROR | InspectR failed for this rule (OPA error, conflicting or undefined result, malformed result) | InspectR developer |

A missing trigger is always UNKNOWN, never NOT_APPLICABLE or PASS. "Not told there is sensitive data" is not "there is no sensitive data". A PASS means "the design declares the control", never "the pipeline is compliant".

An unreadable blueprint (not a JSON object, no `pipeline.nodes` list, or a node without a string `id`) gets no status at all. `evaluator.py` rejects it with an input error before any rule runs.

## Defects fixed

| ID | Defect (rules v1) | Effect | Fix (rules v2) |
|---|---|---|---|
| D1 | If a control field was missing, no branch of the rule matched and the rule was undefined. `policy.rego` built one array from all six rules, so the whole array became undefined. | Removing `dpia_checkpoint_defined` from V2 returned no results for any rule, and the app showed an error. One missing field hid every finding. | Each rule has an explicit UNKNOWN row for missing or invalid controls and a `default` ERROR result. `evaluator.py` queries each rule separately, so a broken rule becomes ERROR for that rule only. |
| D2 | A missing trigger fell into the "not required" branch (`not dpia_is_legally_required`), which returned PASS. | Removing `contains_special_category_data` from both V2 sources gave TK-001 and TK-002 PASS ("does not handle special category data"). This is a false PASS, the most dangerous error in a compliance tool. | Rows 1 and 2 of TK-R1 and TK-R3 separate "trigger missing or invalid" (UNKNOWN) from "trigger declared false" (NOT_APPLICABLE). |
| D3 | TK-005 returned HUMAN as soon as any compliance gate lacked `purpose_compatibility_declared`. | V2 returned HUMAN because `dpia_check` lacks the field, even though `sharing_assessment` declares `true`. The verdict was right by accident. | TK-R3 ignores gates that do not carry the field. On V2 it now returns HUMAN because the sharing gate declares `true` (decision row 5). |
| D4 | The "not applicable" branches recorded evidence that is not in the blueprint, such as `purpose_compatibility_declared: true` (TK-005 with no gates) and `lineage_record_defined: true` (TK-004 with no integration node). These branches also reported PASS. | The raw inLUMEN export got five PASS results that rested on nothing. | These cases return NOT_APPLICABLE or UNKNOWN. Derived evidence lists only what was examined (node IDs, nodes with false or unusable values). TK-R3 has no PASS path at all. |
| D5 | `evaluator.py` called OPA at the fixed path `C:\Tools\OPA\opa.exe`. | InspectR ran only on one Windows machine. Docker, CI and SINTEF machines could not run it. | The OPA path comes from the `OPA_PATH` environment variable, then `opa` on PATH, then the old Windows path. |

Smaller changes:

- Dropped the undocumented fallback fields `dpia_completed`, `risk_assessment_completed`, `data_sharing_agreement_exists`, `lineage_available` and `purpose_compatible`. No blueprint in `data/` uses them, and two names for one fact makes the evidence ambiguous.
- Dropped `contains_personal_data` from the TK-R1 trigger. Special-category data is personal data by definition.
- Only real JSON booleans count as evidence. `"true"`, `1` and `null` give UNKNOWN.
- Each result has two new fields: `title`, and `decision_row`, which links the verdict to a row of the rule's decision table.
- The evaluation page shows all six statuses, and evidence values are displayed as text so that mixed types (boolean, string, list) render correctly.

## Measured behaviour, before and after

The old rule set was the repo's HEAD. Every row was run through OPA 1.22.0.

| Input | v1 (6 rules) | v2 (3 rules) |
|---|---|---|
| V2 blueprint as is | 5 × PASS, TK-005 HUMAN (accidental, D3) | R1 PASS, R2 PASS, R3 HUMAN |
| V2 with `dpia_checkpoint_defined: false` | TK-001 FAIL, TK-006 FAIL | R1 FAIL, R2 PASS, R3 HUMAN |
| V2 with `dpia_checkpoint_defined` removed | No results at all (D1) | R1 UNKNOWN, R2 PASS, R3 HUMAN |
| V2 with `contains_special_category_data` removed | TK-001 and TK-002 PASS (false PASS, D2) | R1 UNKNOWN, R2 PASS, R3 HUMAN |
| Raw inLUMEN export (`tk-uc/inlumen-tk-uc.json`) | 5 × PASS, TK-006 FAIL (vacuous, D4) | R1 UNKNOWN, R2 NOT_APPLICABLE, R3 NOT_APPLICABLE |

On the raw inLUMEN export, R2 and R3 return NOT_APPLICABLE because inLUMEN exports `kind` rather than `type`, so InspectR finds no `data_integration` or `data_transfer` node. That is a correct reading of the input but not of the pipeline. The planned adapter (RQ2) is the fix.

## Interpretations taken (to confirm with supervisors)

1. TK-R1 row 3: a design with special-category data and no compliance gate is FAIL (a missing gate is a missing control), not UNKNOWN.
2. TK-R1 and TK-R3: one source declaring the trigger `true` makes the obligation apply, even if another source's flag is missing.
3. TK-R1: PASS needs one gate that declares both checkpoints `true`. Gates that carry neither field are ignored.

## Verification

- `opa test policies/tk -v`: 29 tests, one or more per decision-table row, all passing. The only uncovered lines are the ERROR defaults, which should be unreachable.
- `OPA_PATH=<path to opa> pytest tests -v`: 13 tests covering the catalogue and taxonomy consistency checks plus V2, the raw export, D1 and D2 regressions, input errors, a missing OPA binary and an injected broken rule. The broken rule gives TK-R2 ERROR while TK-R1 and TK-R3 are kept.

## Files

| File | Change |
|---|---|
| `policies/tk/TK-001.rego` … `TK-006.rego` | Removed |
| `policies/tk/lib.rego` | New: shared helpers for absent, invalid and boolean facts and evidence entries |
| `policies/tk/TK-R1.rego`, `TK-R2.rego`, `TK-R3.rego` | New: three rules as decision tables |
| `policies/tk/policy.rego` | Manifest for the evaluator, plus the combined `results` list |
| `policies/tk/tests/rules_test.rego` | New: Rego unit tests |
| `src/evaluator.py` | Per-rule evaluation, ERROR handling, input errors, portable OPA path |
| `pages/evaluation.py` | Six statuses, rule titles, text rendering of evidence |
| `tests/test_evaluator.py`, `tests/conftest.py` | New: evaluator tests |

## App and documentation consistency

Every page and document that described the six v1 rules or the three v1 statuses was updated. To stop the UI drifting from the Rego rules again, rule and status descriptions now live in one file, `src/catalog.py`, which the pages read. Two tests guard it: the catalogue must list the same rule IDs and legal references as the Rego manifest, and the taxonomy data must list the same rule IDs as the catalogue.

| File | Change |
|---|---|
| `src/catalog.py` | New: rule set, status model and dropped rules, used by the pages |
| `pages/pac.py` | Rule mapping and result semantics generated from the catalogue; dropped rules listed |
| `pages/evidence.py` | Per-rule traceability (trigger, control, selectors, every status, boundary) from the catalogue |
| `pages/tk_uc.py` | Three rules, six statuses; `metadata_catalog` node added to the pipeline table |
| `pages/main.py`, `pages/architecture.py`, `pages/research.py` | Status model text replaces the tri-state text |
| `pages/datapipeline.py` | Diagram label shows all statuses; the teaching example uses UNKNOWN for undetermined evidence instead of HUMAN |
| `pages/taxonomy.py`, `data/inspectr_taxonomy.json` | Taxonomy rebuilt for TK-R1 to TK-R3 |
| `pages/evaluation.py` | Status icons read from the catalogue |
| `README.md` | Evaluator, rule table, TK-R2 traceability example, status meanings, limitations, OPA lookup, tests, repository structure, terminology (trigger, obligation, control, undetermined) |
| `PoC.md`, `tk-uc/stat.md`, `.github/copilot-instructions.md` | Six statuses, three rules, new conventions for adding a rule |

Not changed: the architecture images in `images/` (they may still show PASS / FAIL / HUMAN), `README-backup-*.md`, and the Logg.

All ten pages load without errors in a Streamlit test run.
