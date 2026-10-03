"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

replan = _module.replan
PLAN = [
    {"id": "1", "tool": "search", "depends_on": []},
    {"id": "2", "tool": "fetch", "depends_on": ["1"]},
    {"id": "3", "tool": "summarize", "depends_on": ["2"]},
]


def test_1_failed_step_uses_the_fallback_and_finished_steps_disappear():
    out = replan(PLAN, {"1"}, "2", {"fetch": "fetch_cached"})
    assert [(s["id"], s["tool"]) for s in out] == [("2", "fetch_cached"), ("3", "summarize")]


def test_2_dependencies_on_completed_steps_are_dropped():
    out = replan(PLAN, {"1"}, "2", {"fetch": "alt"})
    assert out[0]["depends_on"] == [] and out[1]["depends_on"] == ["2"]


def test_3_missing_fallback_raises():
    with pytest.raises(ValueError):
        replan(PLAN, {"1"}, "2", {})


def test_4_only_the_failed_step_changes_its_tool():
    out = replan(PLAN, {"1"}, "2", {"fetch": "alt", "summarize": "other"})
    assert out[1]["tool"] == "summarize"


def test_5_original_order_is_preserved():
    plan = PLAN + [{"id": "4", "tool": "report", "depends_on": ["3"]}]
    out = replan(plan, {"1"}, "2", {"fetch": "alt"})
    assert [s["id"] for s in out] == ["2", "3", "4"]


def test_6_nothing_completed_keeps_every_step():
    out = replan(PLAN, set(), "1", {"search": "web"})
    assert len(out) == 3 and out[0]["tool"] == "web"


def test_7_input_plan_is_not_modified():
    snap = [dict(s, depends_on=list(s["depends_on"])) for s in PLAN]
    replan(PLAN, {"1"}, "2", {"fetch": "alt"})
    assert PLAN == snap
