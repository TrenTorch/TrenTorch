"""
pytest data/app_data/12-research-papers/07-agentic-systems/09-mrkl/03-dispatch/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mrkl-dispatch")
dispatch = _module.dispatch


def test_1_matching_route_is_called():
    out = dispatch("add 1", [("add", lambda q: "routed")], lambda q: "fallback")
    assert out == "routed"


def test_2_no_match_uses_the_fallback():
    assert dispatch("hi", [("calc", lambda q: "c")], lambda q: "fallback") == "fallback"


def test_3_route_receives_the_original_query():
    seen = []
    dispatch("Paris", [("paris", lambda q: seen.append(q) or "ok")], lambda q: "f")
    assert seen == ["Paris"]


def test_4_first_matching_route_wins():
    out = dispatch("abc", [("a", lambda q: "first"), ("b", lambda q: "second")], lambda q: "f")
    assert out == "first"


def test_5_empty_routes_use_fallback():
    assert dispatch("x", [], lambda q: "f") == "f"


def test_6_fallback_receives_the_query():
    assert dispatch("zzz", [], lambda q: q.upper()) == "ZZZ"

