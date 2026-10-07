"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected, rtol=1e-6, atol=1e-8):
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for k in expected:
            _close(actual[k], expected[k], rtol, atol)
        return
    if isinstance(expected, (tuple, list)) and not (len(expected) and isinstance(expected[0], (int, float, np.number)) and not isinstance(expected, tuple)):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _close(a, e, rtol, atol)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    assert a.shape == e.shape, (a.shape, e.shape)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, rtol=rtol, atol=atol, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_basic_merge():
    _close(solve(['l', 'o', 'w', 'e', 'r'], 'l', 'o', 'lo'), ['lo', 'w', 'e', 'r'])


def test_02_repeated_pair():
    _close(solve(['a', 'b', 'a', 'b', 'c'], 'a', 'b', 'ab'), ['ab', 'ab', 'c'])


def test_03_overlapping_pair_merges_left_first():
    _close(solve(['a', 'a', 'a'], 'a', 'a', 'aa'), ['aa', 'a'])


def test_04_pair_absent_leaves_tokens():
    _close(solve(['x', 'y'], 'a', 'b', 'ab'), ['x', 'y'])


def test_05_empty_sequence():
    _close(solve([], 'a', 'b', 'ab'), [])


def test_06_pair_at_end():
    _close(solve(['q', 'a', 'b'], 'a', 'b', 'ab'), ['q', 'ab'])


def test_07_multi_character_tokens():
    _close(solve(['ab', 'c', 'ab', 'c'], 'ab', 'c', 'abc'), ['abc', 'abc'])


def test_08_single_token():
    _close(solve(['a'], 'a', 'b', 'ab'), ['a'])


def test_09_four_equal_tokens():
    _close(solve(['a', 'a', 'a', 'a'], 'a', 'a', 'aa'), ['aa', 'aa'])


def test_10_order_matters():
    _close(solve(['b', 'a'], 'a', 'b', 'ab'), ['b', 'a'])


def test_11_non_adjacent_not_merged():
    _close(solve(['a', 'c', 'b'], 'a', 'b', 'ab'), ['a', 'c', 'b'])


def test_12_merged_symbol_is_caller_supplied():
    _close(solve(['t', 'h', 'e', 't', 'h'], 't', 'h', '<th>'), ['<th>', 'e', '<th>'])
