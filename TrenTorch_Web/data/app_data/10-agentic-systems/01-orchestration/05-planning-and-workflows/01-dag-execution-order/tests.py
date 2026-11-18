"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

execution_order = _module.execution_order


def test_1_linear_chain():
    assert execution_order({"c": ["b"], "b": ["a"], "a": []}) == ["a", "b", "c"]


def test_2_alphabetical_tie_break_among_ready_tasks():
    assert execution_order({"z": [], "m": [], "a": []}) == ["a", "m", "z"]


def test_3_diamond():
    tasks = {"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []}
    assert execution_order(tasks) == ["a", "b", "c", "d"]


def test_4_unknown_dependency_raises():
    with pytest.raises(ValueError):
        execution_order({"a": ["ghost"]})


def test_5_cycle_raises():
    with pytest.raises(ValueError):
        execution_order({"a": ["b"], "b": ["a"]})
    with pytest.raises(ValueError):
        execution_order({"a": ["a"]})


def test_6_empty_plan():
    assert execution_order({}) == []


def test_7_order_respects_all_dependencies_and_input_untouched():
    tasks = {"e": ["c", "d"], "d": ["b"], "c": ["a", "b"], "b": [], "a": []}
    snap = {k: list(v) for k, v in tasks.items()}
    order = execution_order(tasks)
    pos = {n: i for i, n in enumerate(order)}
    assert len(order) == 5 and all(pos[d] < pos[n] for n, ds in tasks.items() for d in ds)
    assert tasks == snap
