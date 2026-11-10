# 1 · Getting started

[← Wiki home](README.md) · Next: [Architecture →](02-architecture.md)

This page explains how to install InspectR, point it at an OPA binary, run both test suites and start the Streamlit app.

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.12 | Stated in the root `README.md`. The code uses `str \| None` type hints, so Python 3.10 or newer is the hard minimum. |
| Python packages | Listed in `requirements.txt` (see below). `pytest` is needed for the integration tests and is installed separately. |
| Open Policy Agent (OPA) ≥ 1.0 | A standalone binary, **not** a Python package. The Rego files use `import rego.v1`. Download from the [OPA releases](https://github.com/open-policy-agent/opa/releases). |

All commands run from the **repository root**. `src/evaluator.py` uses the relative path `policies/tk`, `src/scenarios.py` reads `data/…` and `tk-uc/…`, and `app.py` loads images from `images/`.

## 1. Install Python dependencies

`requirements.txt` contains:

```text
streamlit
plotly
pandas
opa
rego
```

The app itself only imports `streamlit`, `pandas` and `plotly` (plotly is used by the archived taxonomy page). OPA is called as an external binary through `subprocess`, so the `opa` and `rego` entries are not used at runtime. On some setups `pip install -r requirements.txt` fails with `No matching distribution found for opa`. If that happens, install the runtime packages directly:

```bash
python -m venv .venv
source .venv/bin/activate              # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt pytest
# if that fails because of the `opa` entry:
python -m pip install streamlit plotly pandas pytest
```

## 2. Make OPA available (`OPA_PATH`)

`src/evaluator.py` looks for OPA in this order (`_opa_executable()`):

1. the `OPA_PATH` environment variable, if it points at an existing file;
2. `opa` on `PATH` (`shutil.which("opa")`);
3. the original Windows path `C:\Tools\OPA\opa.exe`.

If none exists, evaluation raises a `RuntimeError` ("OPA executable not found…"), which the Inspect and Validation pages show as an error message.

```bash
# Linux / macOS
curl -L -o opa https://github.com/open-policy-agent/opa/releases/download/v1.4.2/opa_linux_amd64_static
chmod +x opa
export OPA_PATH="$PWD/opa"
```

```powershell
# Windows
$env:OPA_PATH = "C:\Tools\OPA\opa.exe"
```

Any OPA 1.x release should work; the version above is an example.

## 3. Run the Python integration tests

```bash
pytest tests -v
# or, without exporting the variable:
OPA_PATH=/path/to/opa pytest tests -v
```

Expected: **20 passed**. These tests run real OPA against real blueprints, so they need OPA from step 2. See [Testing and tooling](07-testing-and-tooling.md#python-integration-tests) for what each test covers.

## 4. Run the Rego unit tests

```bash
opa test policies/tk -v
```

Expected: **PASS: 29/29**. These tests live in `policies/tk/tests/rules_test.rego` and need only OPA, not Python. See [Testing and tooling](07-testing-and-tooling.md#rego-unit-tests).

## 5. Start the app

```bash
streamlit run app.py
```

Streamlit prints a local URL (by default `http://localhost:8501`). The app opens on **Overview**. To inspect a blueprint, go to **Inspect** and pick a built-in scenario (S0–S6) or upload a JSON file. **Validation** runs all scenarios through OPA and shows the scenario matrix. See [Streamlit app](05-streamlit-app.md).

## Evaluating a blueprint from the command line

The manifest package also exposes an aggregated `results` list, so a blueprint can be evaluated without Python:

```bash
opa eval --format=pretty --data policies/tk --stdin-input data.inspectr.results \
  < data/tk_mundat_data_sharing_v2.json
```

```powershell
Get-Content -Raw data\tk_mundat_data_sharing_v2.json |
  C:\Tools\OPA\opa.exe eval --format=pretty --data policies\tk --stdin-input data.inspectr.results
```

Note that this path skips the evaluator's input validation and per-rule error isolation (see [Architecture](02-architecture.md)). On the V2 blueprint the expected statuses are TK-R1 `PASS`, TK-R2 `PASS`, TK-R3 `HUMAN`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "OPA executable not found…" | None of the three OPA locations exists. | Set `OPA_PATH` or put `opa` on `PATH`. |
| `InspectR policy directory not found: policies/tk` | Working directory is not the repo root. | `cd` to the repository root. |
| `FileNotFoundError` for `data/…` or `images/…` | Same as above. | Same as above. |
| `InputError` when uploading a blueprint | Not a JSON object, no `pipeline.nodes` list, or a node without a string `id`. | Fix the blueprint shape (see [Data and blueprints](06-data-and-blueprints.md#blueprint-schema)). |
| `No matching distribution found for opa` | `opa` entry in `requirements.txt`. | Install `streamlit plotly pandas` directly (step 1). |
