"""Contract tests for Normalize a Vector."""
import numpy as np
import pytest
from _load import load_solution
solve = load_solution(__file__).solve

def test_examples():
    np.testing.assert_allclose(solve([3., 4.]), [.6, .8])
    np.testing.assert_allclose(solve([-5., 0.]), [-1., 0.])
def test_unit_length_and_direction():
    result = solve([1., 2., 2.])
    assert np.linalg.norm(result) == pytest.approx(1.)
    np.testing.assert_allclose(result, np.array([1., 2., 2.]) / 3.)
def test_zero_vector_contract():
    with pytest.raises(ValueError):
        solve([0., 0.])
