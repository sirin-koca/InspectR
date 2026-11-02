import json
import os
import shutil
import subprocess
from pathlib import Path

from src.catalog import STATUSES


# =========================================================
# INSPECTR EVALUATOR (TK rule set v2)
# =========================================================

POLICY_PATH = Path("policies/tk")
MANIFEST_QUERY = "data.inspectr.manifest"

REQUIRED_FIELDS = {
    "rule",
    "status",
    "legal_reference",
    "reason",
    "evidence",
    "remedy",
}


class InputError(ValueError):
    """The blueprint as a whole cannot be read. No rule is evaluated."""


def _opa_executable() -> str:
    """OPA_PATH env var, then 'opa' on PATH, then the original Windows path."""
    candidates = [
        os.environ.get("OPA_PATH"),
        shutil.which("opa"),
        r"C:\Tools\OPA\opa.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "OPA executable not found. Install OPA, put 'opa' on PATH, "
        "or set the OPA_PATH environment variable."
    )


def _validate_input(blueprint) -> None:
    if not isinstance(blueprint, dict):
        raise InputError("Blueprint must be a JSON object.")
    pipeline = blueprint.get("pipeline")
    if not isinstance(pipeline, dict):
        raise InputError("Blueprint does not contain a valid 'pipeline' object.")
    nodes = pipeline.get("nodes")
    if not isinstance(nodes, list):
        raise InputError("Blueprint does not contain a valid 'pipeline.nodes' list.")
    for index, node in enumerate(nodes):
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise InputError(
                f"pipeline.nodes[{index}] must be an object with a string 'id'."
            )


def _opa_eval(opa: str, query: str, blueprint: dict):
    """Run one OPA query. Returns (value, None) or (None, error message).
    value is None with no error when the query is undefined."""
    try:
        process = subprocess.run(
            [opa, "eval", "--format=json", "--data", str(POLICY_PATH),
             "--stdin-input", query],
            input=json.dumps(blueprint),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, f"OPA could not be run: {exc}"

    if process.returncode != 0:
        return None, process.stderr.strip() or "Unknown OPA evaluation error."

    try:
        output = json.loads(process.stdout)
    except json.JSONDecodeError:
        return None, "OPA returned invalid JSON."

    result = output.get("result")
    if not result:  # undefined
        return None, None
    try:
        return result[0]["expressions"][0]["value"], None
    except (KeyError, IndexError, TypeError):
        return None, "OPA returned an unexpected result structure."


def _error_result(rule_id: str, legal_reference: str, message: str) -> dict:
    return {
        "rule": rule_id,
        "status": "ERROR",
        "legal_reference": legal_reference,
        "reason": f"InspectR could not evaluate this rule: {message} "
                  "This is a technical fault in InspectR, not a finding about the blueprint.",
        "evidence": {"input_evidence": [], "derived_evidence": {"error": message}},
        "remedy": "Report to the InspectR developer.",
    }


def _check_result(value, rule_id: str) -> str | None:
    """Returns an error message if the rule result is malformed."""
    if not isinstance(value, dict):
        return "the rule returned a value that is not a result object."
    missing = REQUIRED_FIELDS - value.keys()
    if missing:
        return "the rule result is missing fields: " + ", ".join(sorted(missing))
    if value["status"] not in STATUSES:
        return f"the rule returned an invalid status '{value['status']}'."
    if value["rule"] != rule_id:
        return f"the rule reported id '{value['rule']}' instead of '{rule_id}'."
    return None


def evaluate(blueprint: dict) -> list[dict]:
    """
    Evaluate a JSON pipeline blueprint against the InspectR TK rule set.

    Flow: blueprint JSON -> input validation -> OPA (one query per rule)
          -> result validation -> one result per rule.

    Raises InputError (a ValueError) if the blueprint is unreadable as a whole.
    Raises RuntimeError if OPA or the rule manifest is unavailable.
    Any fault inside a single rule becomes an ERROR result for that rule only.
    """
    _validate_input(blueprint)

    if not POLICY_PATH.exists():
        raise RuntimeError(f"InspectR policy directory not found: {POLICY_PATH}")

    try:
        opa = _opa_executable()
    except FileNotFoundError as exc:
        raise RuntimeError(str(exc)) from exc

    manifest, error = _opa_eval(opa, MANIFEST_QUERY, blueprint)
    if error or not isinstance(manifest, list) or not manifest:
        raise RuntimeError(
            f"InspectR rule manifest could not be loaded: {error or 'manifest undefined or empty'}"
        )

    results = []
    for entry in manifest:
        rule_id = entry.get("id", "UNKNOWN-RULE")
        legal_reference = entry.get("legal_reference", "")
        value, error = _opa_eval(opa, entry.get("query", ""), blueprint)

        if error:
            results.append(_error_result(rule_id, legal_reference, error))
            continue
        if value is None:
            results.append(_error_result(
                rule_id, legal_reference, "the rule produced no result (undefined)."))
            continue
        problem = _check_result(value, rule_id)
        if problem:
            results.append(_error_result(rule_id, legal_reference, problem))
            continue
        results.append(value)

    return results
