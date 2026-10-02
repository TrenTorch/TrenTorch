"""
pytest tests.py
"""

import types

from _load import load_solution

_module = load_solution(__file__)
generate_range = _module.generate_range
generate_squares = _module.generate_squares
generate_until = _module.generate_until


def test_generator_object():
    result = generate_range(0, 3)
    assert isinstance(result, types.GeneratorType)


def test_lazy_execution():
    seen = []

    def tracked():
        for x in [1, 2, 3]:
            seen.append(x)
            yield x

    gen = generate_squares(tracked())
    assert seen == []
    next(gen)
    assert seen == [1]


def test_correct_sequence():
    assert list(generate_range(2, 5)) == [2, 3, 4]
    assert list(generate_range(5, 2)) == []
    assert list(generate_squares([1, 2, 3])) == [1, 4, 9]


def test_partial_consumption():
    gen = generate_range(0, 1000000)
    assert next(gen) == 0
    assert next(gen) == 1


def test_early_stopping():
    assert list(generate_until([2, 4, 6, 8, 10], 6)) == [2, 4, 6]


def test_empty_input_or_range():
    assert list(generate_range(3, 3)) == []
    assert list(generate_squares([])) == []
    assert list(generate_until([], 5)) == []


def test_memory_behavior_large_range():
    gen = generate_range(0, 10**9)
    assert next(gen) == 0
    assert next(gen) == 1
