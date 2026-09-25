"""
pytest data/app_data/00-python/09-iteration-internals/01-iterables-vs-iterators/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/09-iteration-internals/{Path(__file__).resolve().parent.name}")
is_iterator = _module.is_iterator
get_iterator = _module.get_iterator
independent_iterators = _module.independent_iterators


def test_iterable_vs_iterator_distinction():
    values = [1, 2, 3]
    assert is_iterator(values) is False
    assert is_iterator(tuple(values)) is False
    assert is_iterator("abc") is False
    assert is_iterator(iter(values)) is True


def test_iter_used_correctly():
    result = get_iterator([10, 20])
    assert is_iterator(result) is True
    assert next(result) == 10
    assert next(result) == 20


def test_independent_iterator_state():
    a, b = independent_iterators([1, 2, 3])
    assert next(a) == 1
    assert next(a) == 2
    assert next(b) == 1


def test_empty_iterable():
    result = get_iterator([])
    assert is_iterator(result) is True
    import pytest

    with pytest.raises(StopIteration):
        next(result)


def test_iterator_remains_its_own_iterator():
    iterator = iter([1, 2, 3])
    assert iter(iterator) is iterator
