"""Contract tests for IQR Outlier Flagging."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/029-problem-29-iqr-outlier-flagging').solve

def test_examples():
    np.testing.assert_array_equal(solve([1.,2.,3.,10.]), [False,False,False,True])
    np.testing.assert_array_equal(solve([-100.,0.,1.,2.,3.]), [True,False,False,False,False])
def test_typical_values_not_flagged():
    np.testing.assert_array_equal(solve([1.,2.,3.,4.,5.]), [False]*5)
def test_flags_both_tails():
    result = solve([-50.,1.,2.,3.,4.,80.])
    assert result[0] and result[-1]
