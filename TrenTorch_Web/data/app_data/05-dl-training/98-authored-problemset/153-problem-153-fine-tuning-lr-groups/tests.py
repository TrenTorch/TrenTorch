"""Contract tests for this authored problem."""
import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('05-dl-training/98-authored-problemset/153-problem-153-fine-tuning-lr-groups').solve

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

def test_visible_example_1():
    _assert_equal(solve(["backbone"], ["head"], 0.1, 0.1), [{"params": ["backbone"], "lr": 0.01}, {"params": ["head"], "lr": 0.1}])

def test_visible_example_2():
    _assert_equal(solve([], ["head"], 0.01, 0.2), [{"params": [], "lr": 0.002}, {"params": ["head"], "lr": 0.01}])
