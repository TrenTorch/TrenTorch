"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
percentiles = _module.percentiles
iqr = _module.iqr
zscores = _module.zscores
pearson = _module.pearson
covariance_matrix = _module.covariance_matrix


def test_percentiles_use_linear_interpolation():
    np.testing.assert_allclose(percentiles(np.array([1, 2, 3, 4]), [25, 50, 75]), [1.75, 2.5, 3.25])


def test_percentiles_of_0_and_100_are_the_extremes():
    a = np.array([7.0, 1.0, 9.0, 3.0])
    np.testing.assert_allclose(percentiles(a, [0, 100]), [1.0, 9.0])


def test_percentiles_match_numpy_on_random_data():
    a = np.random.default_rng(0).normal(size=101)
    qs = [1, 10, 33.3, 50, 90, 99]
    np.testing.assert_allclose(percentiles(a, qs), np.percentile(a, qs))


def test_iqr_of_a_simple_sample():
    assert iqr(np.array([1, 2, 3, 4])) == 1.5


def test_iqr_ignores_one_extreme_value():
    base = np.arange(1.0, 101.0)
    assert abs(iqr(np.append(base, 1e6)) - iqr(base)) < 1.0


def test_zscores_have_mean_zero_and_unit_std():
    z = zscores(np.random.default_rng(1).normal(5, 3, size=50))
    np.testing.assert_allclose([z.mean(), z.std()], [0.0, 1.0], atol=1e-12)


def test_zscores_known_values():
    np.testing.assert_allclose(zscores(np.array([2.0, 4.0, 6.0])), [-1.224744871391589, 0.0, 1.224744871391589])


def test_zscores_of_a_constant_array_are_zero_not_nan():
    out = zscores(np.array([5.0, 5.0, 5.0]))
    np.testing.assert_array_equal(out, [0.0, 0.0, 0.0])


def test_pearson_perfect_and_opposite_relationships():
    x = np.arange(10.0)
    np.testing.assert_allclose(pearson(x, 3 * x + 2), 1.0)
    np.testing.assert_allclose(pearson(x, -x), -1.0)


def test_pearson_matches_corrcoef():
    rng = np.random.default_rng(2)
    x = rng.normal(size=60)
    y = 0.5 * x + rng.normal(size=60)
    np.testing.assert_allclose(pearson(x, y), np.corrcoef(x, y)[0, 1])


def test_pearson_returns_a_python_float():
    assert type(pearson(np.array([1.0, 2.0, 4.0]), np.array([2.0, 1.0, 5.0]))) is float


def test_covariance_matrix_matches_numpy_cov():
    x = np.random.default_rng(3).normal(size=(40, 4))
    np.testing.assert_allclose(covariance_matrix(x), np.cov(x, rowvar=False))


def test_covariance_diagonal_is_the_sample_variance_and_it_is_symmetric():
    x = np.random.default_rng(4).normal(size=(30, 3))
    c = covariance_matrix(x)
    np.testing.assert_allclose(np.diag(c), x.var(axis=0, ddof=1))
    np.testing.assert_allclose(c, c.T)


def test_covariance_does_not_change_the_input():
    x = np.random.default_rng(5).normal(size=(10, 2))
    before = x.copy()
    covariance_matrix(x)
    np.testing.assert_array_equal(x, before)
