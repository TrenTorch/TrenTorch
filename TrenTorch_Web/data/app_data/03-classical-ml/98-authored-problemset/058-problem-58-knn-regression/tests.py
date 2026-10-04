"""Contract tests for KNN Regression."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('03-classical-ml/98-authored-problemset/058-problem-58-knn-regression').solve

def test_examples():
    assert solve([[0.],[2.]], [0.,10.], [.2], 1) == pytest.approx(0.)
    assert solve([[0.],[2.],[4.]], [0.,10.,20.], [3.], 2) == pytest.approx(15.)
def test_average_of_selected_neighbors():
    assert solve([[0.],[2.],[10.]], [2.,4.,100.], [.9], 2) == pytest.approx(3.)
def test_k_equal_training_count():
    assert solve([[0.],[2.],[4.]], [1.,3.,8.], [2.], 3) == pytest.approx(4.)
