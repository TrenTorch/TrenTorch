"""Contract tests for Stratified Split."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/031-problem-31-stratified-split').solve

def test_examples():
    train, test = solve([0,0,0,0,1,1,1,1], .5, seed=0)
    assert len(train) == len(test) == 4
    assert sorted(np.r_[train, test].tolist()) == list(range(8))
    train2, test2 = solve([0]*5+[1]*5, .4, seed=2)
    assert len(test2) == 4 and len(train2) == 6
    assert len(set(test2) & set(train2)) == 0
def test_reproducible_and_stratified():
    y = [0]*10 + [1]*10
    train, test = solve(y, .3, seed=9)
    train_again, test_again = solve(y, .3, seed=9)
    np.testing.assert_array_equal(test, test_again)
    assert sum(y[i] == 0 for i in test) == 3
    assert sum(y[i] == 1 for i in test) == 3
def test_split_contains_each_index_once():
    train, test = solve([0,1,0,1,0,1], .33, seed=4)
    assert sorted(np.r_[train, test].tolist()) == list(range(6))
