"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_case_1():
    assert solve([['a', 'b', 'a', 'b', 'c']]) == (('a', 'b'), 2)


def test_case_2():
    assert solve([['a', 'a', 'a']]) == (('a', 'a'), 2)


def test_case_3():
    assert solve([['a', 'b'], ['a', 'b'], ['c', 'd']]) == (('a', 'b'), 2)


def test_case_4():
    assert solve([['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c']]) == (('a', 'b'), 3)


def test_single_token_sequence_has_no_pairs():
    with pytest.raises(IndexError):
        solve([["x"]])


def test_large_n_1e5():
    corpus = [["a", "b"] * 50000]
    assert solve(corpus) == (("a", "b"), 50000)
