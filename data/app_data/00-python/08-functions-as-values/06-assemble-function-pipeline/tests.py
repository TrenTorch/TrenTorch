"""
pytest data/app_data/00-python/08-functions-as-values/06-assemble-function-pipeline/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
make_pipeline = _module.make_pipeline


def test_single_transformation():
    pipeline = make_pipeline(lambda x: x + 1)
    assert pipeline(4) == 5


def test_multiple_transformations_and_ordering():
    pipeline = make_pipeline(lambda x: x + 2, lambda x: x * 3)
    assert pipeline(4) == 18


def test_empty_pipeline():
    pipeline = make_pipeline()
    assert pipeline(42) == 42


def test_independent_pipeline_closures():
    double = make_pipeline(lambda x: x * 2)
    add_ten = make_pipeline(lambda x: x + 10)
    assert double(5) == 10
    assert add_ten(5) == 15


def test_lambda_transformations():
    pipeline = make_pipeline(lambda x: x - 1, lambda x: x * x)
    assert pipeline(5) == 16


def test_decorator_preserves_result():
    pipeline = make_pipeline(lambda x: x + 2, lambda x: x * 3)
    assert pipeline(4) == 18
    assert pipeline.calls == 1


def test_independent_decorator_state():
    p1 = make_pipeline(lambda x: x + 1)
    p2 = make_pipeline(lambda x: x + 1)
    p1(1)
    p1(1)
    p2(1)
    assert p1.calls == 2
    assert p2.calls == 1


def test_repeated_calls_retain_configuration():
    pipeline = make_pipeline(lambda x: x * 2)
    assert pipeline(1) == 2
    assert pipeline(5) == 10
    assert pipeline(10) == 20


def test_input_object_handling():
    pipeline = make_pipeline(lambda x: x + [4])
    original = [1, 2, 3]
    result = pipeline(original)
    assert result == [1, 2, 3, 4]
    assert original == [1, 2, 3]


def test_transformation_failure_propagation():
    def fail(x):
        raise ValueError("boom")

    pipeline = make_pipeline(fail)
    with pytest.raises(ValueError):
        pipeline(1)
