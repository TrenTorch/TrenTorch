"""
pytest data/app_data/12-research-papers/07-agentic-systems/09-mrkl/01-route-query/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mrkl-route-query")
route_query = _module.route_query


def test_1_routes_to_matching_keyword():
    assert route_query("What is 2+2?", [("2+2", "calc"), ("paris", "wiki")]) == "calc"


def test_2_no_keyword_match_returns_none():
    assert route_query("hello", [("calc", "c")]) is None


def test_3_matching_is_case_insensitive():
    assert route_query("PARIS is nice", [("paris", "wiki")]) == "wiki"


def test_4_first_matching_expert_wins():
    assert route_query("paris", [("par", "a"), ("paris", "b")]) == "a"


def test_5_empty_experts_return_none():
    assert route_query("anything", []) is None


def test_6_does_not_mutate_experts():
    e = [("x", "y")]
    route_query("x", e)
    assert e == [("x", "y")]

