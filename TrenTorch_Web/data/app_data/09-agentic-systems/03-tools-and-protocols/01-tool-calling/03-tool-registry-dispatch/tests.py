"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

ToolRegistry = _module.ToolRegistry


def make():
    r = ToolRegistry()
    r.register("add", lambda a, b: a + b, "adds two numbers")
    r.register("boom", lambda: 1 / 0, "always fails")
    return r


def test_1_successful_call():
    assert make().call("add", {"a": 2, "b": 3}) == {"ok": True, "result": 5}


def test_2_unknown_tool_is_an_error_result():
    assert make().call("fly", {}) == {"ok": False, "error": "unknown tool: fly"}


def test_3_exceptions_become_error_results():
    out = make().call("boom", {})
    assert out == {"ok": False, "error": "tool error: division by zero"}


def test_4_wrong_arguments_do_not_crash():
    out = make().call("add", {"a": 1, "c": 2})
    assert out["ok"] is False and out["error"].startswith("tool error:")


def test_5_listing_is_sorted_with_descriptions():
    assert make().list_tools() == [{"name": "add", "description": "adds two numbers"}, {"name": "boom", "description": "always fails"}]


def test_6_duplicate_registration_raises():
    r = make()
    with pytest.raises(ValueError):
        r.register("add", lambda: 0)


def test_7_registries_are_independent():
    a, b = make(), ToolRegistry()
    assert b.list_tools() == [] and b.call("add", {"a": 1, "b": 1})["ok"] is False and a.call("add", {"a": 1, "b": 1})["ok"]
