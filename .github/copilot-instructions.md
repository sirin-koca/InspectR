# InspectR Repository Guidelines

## Project Overview

InspectR is a research proof of concept for design-time compliance inspection of
static data-pipeline blueprints. The current executable use case is the
TK/MUNDAT pipeline and a selected set of GDPR-oriented operational rules. It is
not a complete legal compliance assessment and does not inspect runtime
execution.

## Build, Run, and Validation

Use the repository's Windows virtual environment when available:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

OPA is an external prerequisite for live evaluation. The evaluator currently
invokes `C:\Tools\OPA\opa.exe`, so install OPA at that path (or update the
evaluator deliberately and consistently) before running the Evaluation page.
Run Streamlit from the repository root because policy and asset paths are
relative to the current working directory.

There is no configured pytest/unittest suite, build script, or linter in this
repository. Use targeted smoke checks instead:

```powershell
python -m py_compile app.py src\evaluator.py pages\evaluation.py
C:\Tools\OPA\opa.exe eval --format=json --data policies\tk --stdin-input data.inspectr.results < data\inlumen-tk-uc.json
```

The second command is the single-policy evaluation equivalent of a focused
test; substitute another blueprint under `data\` to check a different input.

## Architecture

- [`app.py`](../app.py) configures the Streamlit application, global CSS,
  session state, and the `st.Page` navigation list.
- `pages\` contains the UI pages. [`pages/evaluation.py`](../pages/evaluation.py)
  uploads two JSON blueprints, hashes uploads to invalidate stale results,
  invokes the evaluator independently for each file, and renders evidence and
  rule-by-rule comparisons.
- [`src/evaluator.py`](../src/evaluator.py) is the Python/OPA boundary. It
  validates the minimum blueprint shape, runs OPA against the TK policy
  directory, parses `data.inspectr.results`, and validates the returned result
  contract before Streamlit displays anything.
- [`policies/tk/policy.rego`](../policies/tk/policy.rego) is the active policy
  aggregator. It returns the six rule reports from `TK-001.rego` through
  `TK-006.rego`; policy decisions belong in Rego rather than being hard-coded
  in Python or page code.
- [`data/`](../data/) contains example inLUMEN-style blueprints and taxonomy
  data. [`tk-uc/`](../tk-uc/) contains source/use-case material, while
  [`assets/`](../assets/) contains supplementary catalogs that are not the
  runtime policy input.

The runtime deliberately passes the uploaded blueprint directly to OPA; there
is no intermediate representation or graph transformation in this PoC. The
overall flow is:

```text
uploaded JSON -> Streamlit session state -> Python shape validation
-> OPA/Rego evaluation -> validated PASS/FAIL/HUMAN reports -> evidence UI
```

## Code and Policy Conventions

- Preserve the result contract expected by `src\evaluator.py`:
  `rule`, `status`, `legal_reference`, `reason`, `evidence`, and `remedy`.
  Status values are exactly `PASS`, `FAIL`, or `HUMAN`.
- Keep evidence explainable. Input evidence should identify the blueprint
  selector and observed/expected values; derived evidence should describe
  conclusions calculated by Rego. Remedies may be human-readable or structured
  when the policy requires an actionable change.
- Add or change compliance logic in the relevant `policies\tk\TK-00X.rego`
  module and register it in `policies\tk\policy.rego`. Keep Python focused on
  orchestration, validation, and presentation.
- Rego modules use `import rego.v1`, package names under
  `inspectr.tk.tkNNN`, and an `article` report consumed by the aggregator.
  Preserve the existing rule IDs and `RULE_ORDER` in the evaluation page when
  adding rules or changing their order.
- Streamlit pages communicate through `st.session_state`; avoid relying on
  module-level mutable state for uploaded blueprints or evaluation results.
  When an upload changes, clear results associated with that upload.
- Use the existing page registration in `app.py` for user-facing pages. Keep
  explanatory/research content separate from executable policy behavior.
- Treat missing or ambiguous blueprint evidence conservatively: distinguish
  automated failure from a result that requires human review, rather than
  silently treating missing evidence as success.
- Keep policy and asset paths compatible with execution from the repository
  root. If path handling is changed, update both the runtime code and the
  documented commands.

See [`README.md`](../README.md) and [`PoC.md`](../PoC.md) for the research
scope, TK scenarios, and limitations.
