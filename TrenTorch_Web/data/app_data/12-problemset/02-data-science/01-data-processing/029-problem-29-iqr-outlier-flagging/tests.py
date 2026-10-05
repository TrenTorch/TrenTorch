"""Contract tests for IQR Outlier Flagging."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_array_equal(solve([1.,2.,3.,10.]), [False,False,False,True])
    np.testing.assert_array_equal(solve([-100.,0.,1.,2.,3.]), [True,False,False,False,False])
def test_typical_values_not_flagged():
    np.testing.assert_array_equal(solve([1.,2.,3.,4.,5.]), [False]*5)
def test_flags_both_tails():
    result = solve([-50.,1.,2.,3.,4.,80.])
    assert result[0] and result[-1]
