"""
pytest data/app_data/00-python/07-functions/07-assemble-pipeline/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/07-functions/{Path(__file__).resolve().parent.name}")
run_pipeline = _module.run_pipeline


def double(x):
    return x * 2


def increment(x):
    return x + 1


def test_transformation_order():
    assert run_pipeline([1, 2, 3], double, increment) == [3, 5, 7]
    assert run_pipeline([1, 2, 3], increment, double) == [4, 6, 8]


def test_no_transformations():
    values = [1, 2, 3]
    result = run_pipeline(values)
    assert result == [1, 2, 3]
    assert result is not values


def test_default_configuration():
    assert run_pipeline([1, 1, 2]) == [1, 1, 2]


def test_keyword_configuration():
    assert run_pipeline([1, 1, 2], unique=True) == [1, 2]
    assert run_pipeline([1, 1, 2], unique=False) == [1, 1, 2]
    assert run_pipeline([1, 2, 3, 4], double, limit=2) == [2, 4]
    assert run_pipeline([1, 2, 3], double, limit=0) == []


def test_duplicate_handling_preserves_first_seen_order():
    assert run_pipeline([3, 1, 3, 2, 1], unique=True) == [3, 1, 2]


def test_limit_handling_stops_exactly():
    result = run_pipeline([1, 2, 3, 4, 5], limit=3)
    assert result == [1, 2, 3]


def test_combined_configuration():
    result = run_pipeline([1, 1, 2, 2, 3], unique=True, limit=2)
    assert result == [1, 2]


def test_unknown_options_raise_type_error():
    with pytest.raises(TypeError):
        run_pipeline([1, 2], typo=True)


def test_input_immutability():
    values = [1, 2, 3]
    run_pipeline(values, double)
    assert values == [1, 2, 3]


def test_fresh_local_state_across_calls():
    assert run_pipeline([1, 1], unique=True) == [1]
    assert run_pipeline([2, 2], unique=True) == [2]


def test_variable_transformation_count():
    assert run_pipeline([1, 2], double, increment, double) == [
        double(increment(double(1))),
        double(increment(double(2))),
    ]


def test_function_argument_forwarding():
    calls = []

    def record(x):
        calls.append(x)
        return x + 1

    run_pipeline([5], record)
    assert calls == [5]
