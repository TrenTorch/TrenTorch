"""Contract tests for Welch t Statistic."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/034-problem-34-welch-t-statistic').solve

def test_examples():
    assert solve([1.,2.,3.], [2.,3.,4.]) == pytest.approx(-1.224744871391589)
    assert solve([2.,4.,6.], [1.,2.,3.]) == pytest.approx(1.5491933384829668)
def test_unequal_variances():
    value = solve([1.,2.,3.,4.], [2.,4.,6.,8.])
    assert np.isfinite(value) and value < 0
    assert solve([2.,4.,6.,8.], [1.,2.,3.,4.]) == pytest.approx(-value)
def test_identical_samples():
    assert solve([1.,3.,5.], [1.,3.,5.]) == pytest.approx(0.)
