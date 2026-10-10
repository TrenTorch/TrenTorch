"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_case_1():
    assert solve(['cat', 'dog'], {'cat': 1, 'dog': 2, 'fish': 3}, -1) == [1, 2]


def test_case_2():
    assert solve([], {'cat': 1, 'dog': 2, 'fish': 3}, -1) == []


def test_case_3():
    assert solve(['cat', 'bird'], {'cat': 1, 'dog': 2, 'fish': 3}, -1) == [1, -1]


def test_case_4():
    assert solve(['bird', 'bird'], {'cat': 1, 'dog': 2, 'fish': 3}, 0) == [0, 0]


def test_case_5():
    assert solve(['cat', 'cat', 'cat'], {'cat': 1, 'dog': 2, 'fish': 3}, -1) == [1, 1, 1]


def test_case_6():
    assert solve(['cat', 'dog', 'fish'], {}, 0) == [0, 0, 0]


def test_large_n_1e5():
    vocab = {"a": 1}
    tokens = ["a"] * 50000 + ["unknown"] * 50000
    out = solve(tokens, vocab, -1)
    assert out[:50000] == [1] * 50000
    assert out[50000:] == [-1] * 50000
