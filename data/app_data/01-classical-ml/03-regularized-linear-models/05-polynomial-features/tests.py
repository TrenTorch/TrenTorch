"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/05-polynomial-features/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
polynomial_features_multivariate = _module.polynomial_features_multivariate


def test_degree_zero_produces_a_single_column_of_ones():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = polynomial_features_multivariate(x, degree=0)
    assert result.shape == (2, 1)
    assert np.allclose(result, 1.0)


def test_degree_one_returns_bias_plus_raw_features():
    x = np.array([[2.0, 3.0]])
    result = polynomial_features_multivariate(x, degree=1)
    assert np.allclose(result, [[1.0, 2.0, 3.0]])


def test_matches_known_oracle_values_for_degree_two():
    # generated once, offline, via sklearn.preprocessing.PolynomialFeatures
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = polynomial_features_multivariate(x, degree=2)
    expected = np.array(
        [
            [1.0, 1.0, 2.0, 1.0, 2.0, 4.0],
            [1.0, 3.0, 4.0, 9.0, 12.0, 16.0],
        ]
    )
    assert np.allclose(result, expected)


def test_matches_sklearn_polynomial_features_exactly():
    from sklearn.preprocessing import PolynomialFeatures

    rng = np.random.default_rng(0)
    x = rng.normal(size=(10, 3))
    for degree in [1, 2, 3]:
        result = polynomial_features_multivariate(x, degree)
        reference = PolynomialFeatures(degree=degree, include_bias=True).fit_transform(x)
        assert np.allclose(result, reference, atol=1e-10)


def test_output_column_count_matches_combinatorial_formula():
    # For k features and degree d, the number of monomials is
    # C(k+d, d), a direct check the right SET of terms was generated.
    from math import comb

    x = np.zeros((5, 3))
    for degree in [0, 1, 2, 3]:
        result = polynomial_features_multivariate(x, degree)
        expected_columns = comb(3 + degree, degree)
        assert result.shape[1] == expected_columns


def test_includes_interaction_terms_not_just_pure_powers():
    # The defining difference from the single-variable version: a
    # degree-2 expansion of 2 features must include the x0*x1 cross
    # term, not just x0^2 and x1^2.
    x = np.array([[2.0, 5.0]])
    result = polynomial_features_multivariate(x, degree=2)
    # columns: [1, x0, x1, x0^2, x0*x1, x1^2] = [1, 2, 5, 4, 10, 25]
    assert np.isclose(result[0, 4], 10.0)  # the x0*x1 interaction term


def test_polynomial_features_does_not_omit_cross_terms():
    # Directly targets a mutant that generates only pure powers per
    # feature (treating each feature independently, ignoring cross
    # terms entirely): the resulting column count would be smaller
    # than the correct combinatorial count.
    from math import comb

    x = np.zeros((4, 2))
    result = polynomial_features_multivariate(x, degree=2)
    correct_count = comb(2 + 2, 2)  # = 6: [1, x0, x1, x0^2, x0*x1, x1^2]
    assert result.shape[1] == correct_count
    assert result.shape[1] > 1 + 2 + 2  # more than just bias + pure powers (5) confirms cross terms exist
