"""Contract tests for KNN Classification."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/057-problem-57-knn-classification').solve

def test_examples():
    assert solve([[0.],[2.]], [0,1], [.2], 1) == 0
    assert solve([[0.],[2.],[4.]], [0,1,1], [3.], 3) == 1
def test_majority_vote():
    assert solve([[0.],[1.],[2.],[3.]], ["a","b","b","a"], [1.2], 3) == "b"
def test_tie_uses_sorted_label_order():
    assert solve([[0.],[2.]], [2,1], [1.], 2) == 1
