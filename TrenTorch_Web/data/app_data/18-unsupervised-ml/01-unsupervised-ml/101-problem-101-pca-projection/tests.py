"""Focused examples and boundary cases for this problem."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution('18-unsupervised-ml/01-unsupervised-ml/101-problem-101-pca-projection')
solve = _module.solve

def _assert_equal(actual, expected):
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _assert_equal(left, right)
    elif isinstance(actual, dict) and isinstance(expected, dict):
        assert actual == expected
    elif isinstance(actual, (int, float, bool, np.number)) and isinstance(expected, (int, float, bool, np.number)):
        np.testing.assert_allclose(actual, expected, rtol=1e-6, atol=1e-6)
    else:
        np.testing.assert_allclose(np.asarray(actual), np.asarray(expected), rtol=1e-6, atol=1e-6)

def test_case_01():
    _assert_equal(solve([[1,2],[3,4]], [[1,0],[0,1]], 1), [[1], [3]])

def test_case_02():
    _assert_equal(solve([[-1,2]], [[0,1],[1,0]], 2), [[2, -1]])

def test_case_03():
    _assert_equal(solve([[0,0],[2,0]], [[1,0],[0,1]], 2), [[0, 0], [2, 0]])

def test_case_04():
    _assert_equal(solve([[1,0]], [[1,0],[0,1]], 0), [[]])

