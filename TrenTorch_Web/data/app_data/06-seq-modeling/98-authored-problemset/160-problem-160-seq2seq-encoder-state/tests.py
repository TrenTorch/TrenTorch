"""Contract tests for this authored problem."""
import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

solve = load_solution('06-seq-modeling/98-authored-problemset/160-problem-160-seq2seq-encoder-state').solve

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
    _assert_equal(solve([[1.0], [2.0]], [0.0], [[1.0]], [[0.5]], [0.0]), [0.98304110])

def test_visible_example_2():
    _assert_equal(solve([[0.0], [0.0]], [1.0], [[1.0]], [[0.0]], [0.0]), [0.0])
