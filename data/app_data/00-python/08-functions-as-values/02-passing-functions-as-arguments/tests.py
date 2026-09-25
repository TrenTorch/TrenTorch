"""
pytest data/app_data/00-python/08-functions-as-values/02-passing-functions-as-arguments/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
apply_once = _module.apply_once
apply_twice = _module.apply_twice
apply_n_times = _module.apply_n_times
transform_all = _module.transform_all


def test_function_receives_correct_value():
    assert apply_once(abs, -8) == 8
    assert apply_once(str, 42) == "42"


def test_sequential_application():
    def add_one(x):
        return x + 1

    assert apply_twice(add_one, 5) == 7


def test_zero_and_negative_counts():
    assert apply_n_times(lambda x: x * 2, 3, 0) == 3
    assert apply_n_times(lambda x: x * 2, 3, -5) == 3


def test_apply_n_times_multiple():
    def double(x):
        return x * 2

    assert apply_n_times(double, 3, 3) == 24


def test_order_preservation():
    assert transform_all([1, -2, 3], abs) == [1, 2, 3]


def test_input_list_unchanged():
    values = [1, -2, 3]
    transform_all(values, abs)
    assert values == [1, -2, 3]


def test_different_supplied_functions():
    assert transform_all(["a", "bb"], len) == [1, 2]
    assert apply_once(len, "hello") == 5
