"""Contract tests for K-Fold Indices."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    folds = solve(6,3)
    assert len(folds) == 3
    np.testing.assert_array_equal(folds[0][0], [2,3,4,5])
    np.testing.assert_array_equal(folds[0][1], [0,1])
    assert [len(test) for _,test in solve(5,2)] == [3,2]
def test_every_index_appears_once_as_test():
    folds = solve(10,4)
    tests = np.concatenate([test for _,test in folds])
    np.testing.assert_array_equal(np.sort(tests), np.arange(10))
def test_train_and_test_are_disjoint():
    for train, test in solve(7,3):
        assert not (set(train) & set(test))
        assert sorted(np.r_[train,test].tolist()) == list(range(7))
