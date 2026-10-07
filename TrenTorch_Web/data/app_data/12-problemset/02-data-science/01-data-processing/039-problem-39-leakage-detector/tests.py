"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_case_1():
    assert solve(['age', 'target_amount', 'income']) == ['target_amount']


def test_case_2():
    assert solve([]) == []


def test_case_3():
    assert solve(['Label_Class', 'FUTURE_sales', 'price']) == ['Label_Class', 'FUTURE_sales']


def test_case_4():
    assert solve(['post_click_rate', 'clicks']) == ['post_click_rate']


def test_case_5():
    assert solve(['age', 'income']) == []


def test_case_6():
    assert solve(['target', 'target', 'label']) == ['target', 'target', 'label']


def test_case_insensitive_matching():
    assert solve(["TARGET_value"]) == ["TARGET_value"]


def test_large_n_1e5():
    columns = [f"feature_{i}" for i in range(99999)] + ["target"]
    assert solve(columns) == ["target"]
