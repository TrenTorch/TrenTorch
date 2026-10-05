"""Contract tests for KNN Classification."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    assert solve([[0.],[2.]], [0,1], [.2], 1) == 0
    assert solve([[0.],[2.],[4.]], [0,1,1], [3.], 3) == 1
def test_majority_vote():
    assert solve([[0.],[1.],[2.],[3.]], ["a","b","b","a"], [1.2], 3) == "b"
def test_tie_uses_sorted_label_order():
    assert solve([[0.],[2.]], [2,1], [1.], 2) == 1
