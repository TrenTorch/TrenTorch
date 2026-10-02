"""
pytest tests.py
"""

import types

from _load import load_solution

_module = load_solution(__file__)
eager_double = _module.eager_double
lazy_double = _module.lazy_double
lazy_positive = _module.lazy_positive


def test_eager_result_type():
    result = eager_double([1, 2, 3])
    assert type(result) is list
    assert result == [2, 4, 6]


def test_lazy_result_type():
    result = lazy_double([1, 2, 3])
    assert isinstance(result, types.GeneratorType)


def test_execution_timing():
    processed = []

    def source():
        for x in [1, 2, 3]:
            processed.append(x)
            yield x

    result = lazy_double(source())
    assert processed == []
    next(result)
    assert processed == [1]


def test_large_input_behavior():
    result = lazy_double(range(10**9))
    assert next(result) == 0
    assert next(result) == 2


def test_correct_filtering_and_transformation():
    assert list(lazy_double([1, 2, 3])) == [2, 4, 6]
    assert list(lazy_positive([-2, 3, 0, 5])) == [3, 5]


def test_partial_consumption():
    processed = []

    def source():
        for x in [1, 2, 3, 4]:
            processed.append(x)
            yield x

    result = lazy_positive(source())
    next(result)
    assert processed == [1]
