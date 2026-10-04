"""Contract tests for Cosine Similarity."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('02-math-and-statistics/01-maths-stats-for-ml/003-problem-3-cosine-similarity').solve

def test_examples():
    assert solve([1., 0.], [0., 1.]) == pytest.approx(0.)
    assert solve([1., 2.], [2., 4.]) == pytest.approx(1.)
def test_opposite_and_orthogonal_vectors():
    assert solve([1., 2.], [-1., -2.]) == pytest.approx(-1.)
    assert solve([1., 0.], [0., 3.]) == pytest.approx(0.)
def test_zero_vector_returns_zero():
    assert solve([0., 0.], [4., 5.]) == 0.
