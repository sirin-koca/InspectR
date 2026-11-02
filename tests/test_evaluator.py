"""Evaluator tests: real blueprints, input errors and per-rule ERROR isolation.
Run from the repo root: OPA_PATH=/path/to/opa pytest tests -v
"""
import copy
import json
import shutil
from pathlib import Path

import pytest

from src import evaluator
from src.evaluator import InputError, evaluate

ROOT = Path(__file__).resolve().parents[1]
V2 = json.loads((ROOT / "data/tk_mundat_data_sharing_v2.json").read_text(encoding="utf-8"))
RAW = json.loads((ROOT / "tk-uc/inlumen-tk-uc.json").read_text(encoding="utf-8"))


def statuses(results):
    return {r["rule"]: r["status"] for r in results}


def node(bp, node_id):
    return next(n for n in bp["pipeline"]["nodes"] if n["id"] == node_id)


def test_v2_baseline():
    assert statuses(evaluate(V2)) == {"TK-R1": "PASS", "TK-R2": "PASS", "TK-R3": "HUMAN"}


def test_raw_inlumen_export_gives_no_vacuous_pass():
    s = statuses(evaluate(RAW))
    assert s["TK-R1"] == "UNKNOWN"
    assert "PASS" not in s.values()


def test_control_false_is_fail():
    bp = copy.deepcopy(V2)
    node(bp, "dpia_check")["properties"]["dpia_checkpoint_defined"] = False
    assert statuses(evaluate(bp))["TK-R1"] == "FAIL"


def test_removed_control_no_longer_wipes_results():  # defect D1
    bp = copy.deepcopy(V2)
    del node(bp, "dpia_check")["properties"]["dpia_checkpoint_defined"]
    assert statuses(evaluate(bp)) == {"TK-R1": "UNKNOWN", "TK-R2": "PASS", "TK-R3": "HUMAN"}


def test_removed_trigger_is_unknown_not_pass():  # defect D2
    bp = copy.deepcopy(V2)
    del node(bp, "health_services")["properties"]["contains_special_category_data"]
    del node(bp, "citizen_registry")["properties"]["contains_special_category_data"]
    assert statuses(evaluate(bp))["TK-R1"] == "UNKNOWN"


@pytest.mark.parametrize("bad", [[], {"pipeline": []}, {"pipeline": {}}, {"pipeline": {"nodes": [{"type": "x"}]}}])
def test_unreadable_blueprint_is_input_error(bad):
    with pytest.raises(InputError):
        evaluate(bad)


def test_broken_rule_is_error_for_that_rule_only(tmp_path, monkeypatch):
    policies = tmp_path / "tk"
    shutil.copytree(ROOT / "policies/tk", policies, ignore=shutil.ignore_patterns("tests"))
    # Inject a conflict: TK-R2 now produces two different results -> OPA runtime error.
    (policies / "broken.rego").write_text(
        "package inspectr.tk.r2\nimport rego.v1\nresult := {\"rule\": \"TK-R2\"} if true\n",
        encoding="utf-8",
    )
    (policies / "TK-R2.rego").write_text(
        (policies / "TK-R2.rego").read_text(encoding="utf-8").replace("default result :=", "default result_disabled :="),
        encoding="utf-8",
    )
    monkeypatch.setattr(evaluator, "POLICY_PATH", policies)
    s = statuses(evaluate(V2))
    assert s == {"TK-R1": "PASS", "TK-R2": "ERROR", "TK-R3": "HUMAN"}


def test_missing_opa_is_runtime_error(monkeypatch):
    monkeypatch.setattr(evaluator, "_opa_executable", lambda: (_ for _ in ()).throw(FileNotFoundError("no opa")))
    with pytest.raises(RuntimeError):
        evaluate(V2)


def test_catalog_matches_rego_manifest():
    """The UI catalog must describe exactly the rules OPA runs."""
    from src.catalog import RULES, STATUSES
    manifest, error = evaluator._opa_eval(evaluator._opa_executable(), evaluator.MANIFEST_QUERY, V2)
    assert error is None
    assert [m["id"] for m in manifest] == [r["id"] for r in RULES]
    assert [m["legal_reference"] for m in manifest] == [r["legal_reference"] for r in RULES]
    for rule in RULES:
        assert set(rule["outcomes"]) <= set(STATUSES)


def test_taxonomy_matches_catalog():
    from src.catalog import RULES
    taxonomy = json.loads((ROOT / "data/inspectr_taxonomy.json").read_text(encoding="utf-8"))
    assert [c["rule_id"] for c in taxonomy["children"]] == [r["id"] for r in RULES]


@pytest.mark.parametrize("scenario", [s[0] for s in __import__("src.scenarios", fromlist=["SCENARIOS"]).SCENARIOS])
def test_demo_scenarios_match_expected(scenario):
    """The scenarios shown on the Inspect and Validation pages."""
    from src.scenarios import SCENARIOS, build
    expected = next(s[4] for s in SCENARIOS if s[0] == scenario)
    assert statuses(evaluate(build(scenario))) == expected
