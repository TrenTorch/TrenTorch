"""Contract tests for Winsorize Values."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([0.,1.,2.,3.,100.], .2, .8), [.8,1.,2.,3.,22.4])
    np.testing.assert_allclose(solve([1.,2.,3.,4.,5.], 0., 1.), [1.,2.,3.,4.,5.])
def test_clips_both_tails():
    result = solve([-100.,0.,1.,2.,3.,100.], .25, .75)
    assert result[0] == pytest.approx(np.quantile([-100.,0.,1.,2.,3.,100.], .25))
    assert result[-1] == pytest.approx(np.quantile([-100.,0.,1.,2.,3.,100.], .75))
def test_interior_values_unchanged():
    np.testing.assert_allclose(solve([0.,1.,2.,3.,4.], .2, .8), [.8,1.,2.,3.,3.2])
