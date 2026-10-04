"""Contract tests for deterministic index-based K-fold splitting."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402
solve = load_solution('03-classical-ml/98-authored-problemset/064-problem-64-stratified-k-fold').solve

def _assert_splits(actual, expected):
    assert len(actual) == len(expected)
    for (train, valid), (want_train, want_valid) in zip(actual, expected):
        np.testing.assert_array_equal(train, want_train)
        np.testing.assert_array_equal(valid, want_valid)

def test_01_case():
    r=solve(5, 3)
    _assert_splits(r, [([2, 3, 4], [0, 1]), ([0, 1, 4], [2, 3]), ([0, 1, 2, 3], [4])])

def test_02_case():
    _assert_splits(solve(4, 2), [([2, 3], [0, 1]), ([0, 1], [2, 3])])

def test_03_case():
    _assert_splits(solve(3, 1), [([], [0, 1, 2])])

def test_04_case():
    _assert_splits(solve(1, 1), [([], [0])])

def test_05_case():
    _assert_splits(solve(0, 2), [([], []), ([], [])])

def test_06_case():
    _assert_splits(solve(1, 3), [([], [0]), ([0], []), ([0], [])])

def test_07_case():
    r=solve(7, 3)
    assert len(r) == 3
    np.testing.assert_array_equal(np.concatenate([valid for _, valid in r]), np.arange(7))

def test_08_case():
    sizes=[len(valid) for _, valid in solve(8, 3)]
    assert max(sizes)-min(sizes) <= 1

def test_09_case():
    r=solve(9, 4)
    for train, valid in r:
        assert not set(train.tolist()) & set(valid.tolist())

def test_10_case():
    r=solve(6, 3)
    for train, valid in r:
        np.testing.assert_array_equal(np.sort(np.concatenate([train, valid])), np.arange(6))

def test_11_case():
    a=solve(10, 4); b=solve(10, 4)
    for (ta, va), (tb, vb) in zip(a, b):
        np.testing.assert_array_equal(ta, tb); np.testing.assert_array_equal(va, vb)

def test_12_case():
    assert all(np.issubdtype(v.dtype, np.integer) and np.issubdtype(t.dtype, np.integer) for t, v in solve(5, 2))

def test_13_case():
    r=solve(11, 5)
    assert sum(len(valid) for _, valid in r) == 11
    assert [len(v) for _, v in r] == [3, 2, 2, 2, 2]

