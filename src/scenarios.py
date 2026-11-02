"""
Built-in demonstration scenarios.

Each scenario is the enriched V2 blueprint with one controlled change (or the
raw inLUMEN export). Together they exercise every non-ERROR status, and the
expected results make the demonstration a live regression check.
"""

import copy
import json
from pathlib import Path

V2_PATH = Path("data/tk_mundat_data_sharing_v2.json")
RAW_PATH = Path("tk-uc/inlumen-tk-uc.json")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _node(blueprint: dict, node_id: str) -> dict:
    return next(n for n in blueprint["pipeline"]["nodes"] if n["id"] == node_id)


def _v2() -> dict:
    return _load(V2_PATH)


def _control_false() -> dict:
    bp = _v2()
    _node(bp, "dpia_check")["properties"]["dpia_checkpoint_defined"] = False
    return bp


def _control_removed() -> dict:
    bp = _v2()
    del _node(bp, "dpia_check")["properties"]["dpia_checkpoint_defined"]
    return bp


def _trigger_removed() -> dict:
    bp = _v2()
    for node_id in ("health_services", "citizen_registry"):
        del _node(bp, node_id)["properties"]["contains_special_category_data"]
    return bp


def _no_sensitive_data() -> dict:
    bp = _v2()
    _node(bp, "health_services")["properties"]["contains_special_category_data"] = False
    return bp


def _purpose_not_assessed() -> dict:
    bp = _v2()
    _node(bp, "sharing_assessment")["properties"]["purpose_compatibility_declared"] = False
    return bp


def _raw_export() -> dict:
    return _load(RAW_PATH)


# (key, label, change made, builder, expected statuses)
SCENARIOS = [
    ("v2", "S0 · Enriched blueprint (V2)", "None. The manually enriched TK/MUNDAT blueprint.",
     _v2, {"TK-R1": "PASS", "TK-R2": "PASS", "TK-R3": "HUMAN"}),
    ("control_false", "S1 · DPIA checkpoint declared false", "dpia_check.dpia_checkpoint_defined: true → false",
     _control_false, {"TK-R1": "FAIL", "TK-R2": "PASS", "TK-R3": "HUMAN"}),
    ("control_removed", "S2 · DPIA checkpoint field removed", "dpia_check.dpia_checkpoint_defined deleted",
     _control_removed, {"TK-R1": "UNKNOWN", "TK-R2": "PASS", "TK-R3": "HUMAN"}),
    ("trigger_removed", "S3 · Special-category flag removed", "contains_special_category_data deleted on both sources",
     _trigger_removed, {"TK-R1": "UNKNOWN", "TK-R2": "PASS", "TK-R3": "HUMAN"}),
    ("no_sensitive", "S4 · No special-category data", "health_services.contains_special_category_data: true → false",
     _no_sensitive_data, {"TK-R1": "NOT_APPLICABLE", "TK-R2": "PASS", "TK-R3": "HUMAN"}),
    ("purpose_false", "S5 · Purpose compatibility declared false", "sharing_assessment.purpose_compatibility_declared: true → false",
     _purpose_not_assessed, {"TK-R1": "PASS", "TK-R2": "PASS", "TK-R3": "FAIL"}),
    ("raw", "S6 · Raw inLUMEN export (not enriched)", "None. The original inLUMEN export without compliance metadata.",
     _raw_export, {"TK-R1": "UNKNOWN", "TK-R2": "NOT_APPLICABLE", "TK-R3": "NOT_APPLICABLE"}),
]


def build(key: str) -> dict:
    for k, _label, _change, builder, _expected in SCENARIOS:
        if k == key:
            return copy.deepcopy(builder())
    raise KeyError(key)
