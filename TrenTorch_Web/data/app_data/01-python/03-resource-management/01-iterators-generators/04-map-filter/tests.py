"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
squared = _module.squared
keep_positive = _module.keep_positive
transform_and_filter = _module.transform_and_filter


def test_correct_map_transformation():
    assert list(squared([1, 2, 3])) == [1, 4, 9]


def test_correct_filtering():
    assert list(keep_positive([-2, 0, 3, 5])) == [3, 5]


def test_lazy_behavior():
    calls = []

    def source():
        for x in [1, 2, 3]:
            calls.append(x)
            yield x

    result = squared(source())
    assert calls == []
    next(result)
    assert calls == [1]


def test_composition_order():
    result = transform_and_filter([1, 2, 3], lambda x: x * 2, lambda x: x > 2)
    assert list(result) == [4, 6]


def test_input_ordering():
    assert list(squared([3, 1, 2])) == [9, 1, 4]


def test_iterator_consumption():
    result = squared([1, 2, 3])
    assert list(result) == [1, 4, 9]
    assert list(result) == []
