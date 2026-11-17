"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
validate_plan = _module.validate_plan
TOOLS = {"search": {"required": ["query"], "optional": ["limit"]}, "email": {"required": ["to", "body"], "optional": []}}


def step(i, tool, args=None, deps=()):
    return {"id": i, "tool": tool, "args": args or {}, "depends_on": list(deps)}


def test_1_valid_plan_has_no_errors():
    plan = [step("1", "search", {"query": "x"}), step("2", "email", {"to": "a", "body": "b"}, ["1"])]
    assert validate_plan(plan, TOOLS) == []


def test_2_unknown_tool_skips_argument_checks():
    assert validate_plan([step("1", "teleport", {"x": 1})], TOOLS) == ["step 1: unknown tool 'teleport'"]


def test_3_missing_and_unexpected_arguments_are_sorted():
    errs = validate_plan([step("1", "email", {"cc": "z", "bcc": "y"})], TOOLS)
    assert errs == [
        "step 1: missing argument 'body'", "step 1: missing argument 'to'",
        "step 1: unexpected argument 'bcc'", "step 1: unexpected argument 'cc'",
    ]


def test_4_dependency_must_be_an_earlier_step():
    plan = [step("1", "search", {"query": "x"}, ["2"]), step("2", "search", {"query": "y"}, ["1", "9"])]
    assert validate_plan(plan, TOOLS) == ["step 1: invalid dependency '2'", "step 2: invalid dependency '9'"]


def test_5_self_dependency_is_invalid():
    assert validate_plan([step("1", "search", {"query": "x"}, ["1"])], TOOLS) == ["step 1: invalid dependency '1'"]


def test_6_optional_arguments_are_allowed():
    assert validate_plan([step("1", "search", {"query": "x", "limit": 3})], TOOLS) == []


def test_7_errors_follow_plan_order_and_input_untouched():
    plan = [step("a", "x"), step("b", "email", {"to": "t", "body": "b"}, ["zzz"])]
    snap = [dict(s) for s in plan]
    errs = validate_plan(plan, TOOLS)
    assert errs == ["step a: unknown tool 'x'", "step b: invalid dependency 'zzz'"] and plan == snap
