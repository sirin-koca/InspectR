import json
import subprocess
from pathlib import Path


# =========================================================
# INSPECTR EVALUATOR
# =========================================================

POLICY_PATH = Path("policies/tk")
OPA_QUERY = "data.inspectr.results"


def evaluate(blueprint: dict) -> list[dict]:
    """
    Evaluate an inLUMEN JSON pipeline blueprint against
    the InspectR Rego Policy-as-Code ruleset.

    Flow:
        Blueprint JSON
            -> OPA
            -> policy.rego
            -> InspectR results

    No Intermediate Representation (IR) is used.
    """

    # -----------------------------------------------------
    # VALIDATE INPUT
    # -----------------------------------------------------

    if not isinstance(blueprint, dict):
        raise ValueError(
            "Blueprint must be a JSON object."
        )

    pipeline = blueprint.get("pipeline")

    if not isinstance(pipeline, dict):
        raise ValueError(
            "Blueprint does not contain a valid 'pipeline' object."
        )

    nodes = pipeline.get("nodes")

    if not isinstance(nodes, list):
        raise ValueError(
            "Blueprint does not contain a valid 'pipeline.nodes' list."
        )

    # -----------------------------------------------------
    # CHECK POLICY FILE
    # -----------------------------------------------------

    if not POLICY_PATH.exists():
        raise FileNotFoundError(
            f"InspectR policy file not found: {POLICY_PATH}"
        )

    # -----------------------------------------------------
    # RUN OPA / REGO
    # -----------------------------------------------------

    try:
        process = subprocess.run(
            [
                r"C:\Tools\OPA\opa.exe",
                "eval",
                "--format=json",
                "--data",
                str(POLICY_PATH),
                "--stdin-input",
                OPA_QUERY,
            ],
            input=json.dumps(blueprint),
            text=True,
            capture_output=True,
            check=False,
        )

    except FileNotFoundError as exc:
        raise RuntimeError(
            "OPA executable was not found. "
            "Install OPA and make sure 'opa' is available on PATH."
        ) from exc

    # -----------------------------------------------------
    # HANDLE OPA ERROR
    # -----------------------------------------------------

    if process.returncode != 0:
        error_message = process.stderr.strip()

        if not error_message:
            error_message = "Unknown OPA evaluation error."

        raise RuntimeError(
            f"OPA policy evaluation failed: {error_message}"
        )

    # -----------------------------------------------------
    # PARSE OPA RESPONSE
    # -----------------------------------------------------

    try:
        opa_output = json.loads(process.stdout)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "OPA returned invalid JSON."
        ) from exc

    try:
        results = (
            opa_output["result"][0]
            ["expressions"][0]
            ["value"]
        )

    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            "OPA returned an unexpected evaluation result."
        ) from exc

    # -----------------------------------------------------
    # VALIDATE INSPECTR RESULTS
    # -----------------------------------------------------

    if not isinstance(results, list):
        raise RuntimeError(
            "InspectR expected the Rego policy to return a list of results."
        )

    required_fields = {
        "rule",
        "status",
        "legal_reference",
        "reason",
        "evidence",
        "remedy",
    }

    for result in results:

        if not isinstance(result, dict):
            raise RuntimeError(
                "Invalid result returned by the Rego policy."
            )

        missing_fields = required_fields - result.keys()

        if missing_fields:
            raise RuntimeError(
                "Rego result is missing required fields: "
                + ", ".join(sorted(missing_fields))
            )

        if result["status"] not in {"PASS", "FAIL", "HUMAN"}:
            raise RuntimeError(
                f"Invalid InspectR status: {result['status']}"
            )

    # -----------------------------------------------------
    # RETURN RESULTS TO STREAMLIT
    # -----------------------------------------------------

    return results