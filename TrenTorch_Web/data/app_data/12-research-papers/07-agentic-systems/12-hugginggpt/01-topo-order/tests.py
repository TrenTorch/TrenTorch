"""
pytest data/app_data/12-research-papers/07-agentic-systems/12-hugginggpt/01-topo-order/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-hugginggpt-topo-order")
topo_order = _module.topo_order


def test_1_dependencies_come_first():
    order = topo_order({"b": ["a"], "a": []})
    assert order.index("a") < order.index("b")


def test_2_independent_tasks_are_sorted_by_id():
    assert topo_order({"x": [], "y": []}) == ["x", "y"]


def test_3_chain_is_ordered():
    assert topo_order({"c": ["b"], "b": ["a"], "a": []}) == ["a", "b", "c"]


def test_4_cycle_returns_none():
    assert topo_order({"a": ["b"], "b": ["a"]}) is None


def test_5_empty_plan_is_empty_order():
    assert topo_order({}) == []


def test_6_does_not_mutate_tasks():
    tasks = {"b": ["a"], "a": []}
    topo_order(tasks)
    assert tasks == {"b": ["a"], "a": []}

