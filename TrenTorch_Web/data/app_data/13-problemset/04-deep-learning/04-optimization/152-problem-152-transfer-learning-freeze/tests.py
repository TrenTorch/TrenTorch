"""Contract tests for this authored problem."""
import numpy as np
import pytest

from _load import load_solution

solve = load_solution(__file__).solve

def _assert_equal(actual, expected):
    if isinstance(actual, np.ndarray):
        np.testing.assert_allclose(actual, np.asarray(expected), atol=1e-6, rtol=1e-6)
    elif isinstance(actual, tuple):
        assert isinstance(expected, tuple) and len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _assert_equal(left, right)
    elif isinstance(actual, list):
        assert isinstance(expected, (list, tuple)) and len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _assert_equal(left, right)
    elif isinstance(actual, dict):
        assert isinstance(expected, dict) and actual.keys() == expected.keys()
        for key in actual:
            _assert_equal(actual[key], expected[key])
    elif isinstance(actual, (float, np.floating)) or isinstance(expected, float):
        assert actual == pytest.approx(expected, rel=1e-6, abs=1e-6)
    else:
        assert actual == expected

from types import SimpleNamespace

def test_example_1_freezes_backbone_and_trains_head():
    backbone = [SimpleNamespace(requires_grad=True)]
    head = [SimpleNamespace(requires_grad=False)]
    returned_backbone, returned_head = solve(backbone, head)
    assert returned_backbone == backbone and returned_head == head
    assert [parameter.requires_grad for parameter in backbone] == [False]
    assert [parameter.requires_grad for parameter in head] == [True]

def test_example_2_updates_every_parameter_flag():
    backbone = [SimpleNamespace(requires_grad=True), SimpleNamespace(requires_grad=True)]
    head = [SimpleNamespace(requires_grad=False)]
    solve(backbone, head)
    assert [parameter.requires_grad for parameter in backbone] == [False, False]
    assert [parameter.requires_grad for parameter in head] == [True]
