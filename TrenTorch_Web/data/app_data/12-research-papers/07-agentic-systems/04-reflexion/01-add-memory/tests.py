"""
pytest data/app_data/12-research-papers/07-agentic-systems/04-reflexion/01-add-memory/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-reflexion-add-memory")
add_reflection = _module.add_reflection


def test_1_appends_to_an_empty_memory():
    assert add_reflection([], "r1", 3) == ["r1"]


def test_2_keeps_only_the_most_recent_items():
    assert add_reflection(["a", "b"], "c", 2) == ["b", "c"]


def test_3_zero_capacity_keeps_nothing():
    assert add_reflection(["a"], "b", 0) == []


def test_4_does_not_mutate_the_original_memory():
    m = ["a"]
    add_reflection(m, "b", 5)
    assert m == ["a"]


def test_5_below_capacity_keeps_everything():
    assert add_reflection(["a"], "b", 10) == ["a", "b"]


def test_6_returns_a_list():
    assert isinstance(add_reflection([], "x", 1), list)

