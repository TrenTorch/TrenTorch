"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/04-elastic-net/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
elastic_net_coordinate_descent = _module.elastic_net_coordinate_descent

lasso_regression_coordinate_descent = load_solution(
    "01-classical-ml/03-regularized-linear-models/03-lasso-regression"
).lasso_regression_coordinate_descent


def test_elastic_net_with_l1_ratio_one_matches_pure_lasso():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(200, 5))
    true_w = np.array([2.0, 0.0, -1.0, 0.0, 3.0])
    y = x @ true_w + rng.normal(scale=0.2, size=200)

    elastic_weight, elastic_bias = elastic_net_coordinate_descent(x, y, alpha=0.3, l1_ratio=1.0, epochs=200)
    lasso_weight, lasso_bias = lasso_regression_coordinate_descent(x, y, alpha=0.3, epochs=200)

    assert np.allclose(elastic_weight, lasso_weight, atol=1e-6)
    assert np.allclose(elastic_bias, lasso_bias, atol=1e-6)


def test_elastic_net_matches_sklearn_elastic_net():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(300, 6))
    true_w = np.array([2.0, 0.0, 0.0, -1.0, 0.0, 3.0])
    y = x @ true_w + 3.0 + rng.normal(scale=0.3, size=300)
    weight, bias = elastic_net_coordinate_descent(x, y, alpha=0.3, l1_ratio=0.7, epochs=300)

    from sklearn.linear_model import ElasticNet

    reference = ElasticNet(alpha=0.3, l1_ratio=0.7, max_iter=10000).fit(x, y)
    assert np.allclose(weight.flatten(), reference.coef_, atol=1e-4)
    assert np.isclose(bias[0], reference.intercept_, atol=1e-4)


def test_elastic_net_still_produces_exact_zeros_for_irrelevant_features():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(300, 5))
    true_w = np.array([3.0, 0.0, 0.0, 0.0, -2.0])
    y = x @ true_w + rng.normal(scale=0.1, size=300)
    weight, _ = elastic_net_coordinate_descent(x, y, alpha=0.5, l1_ratio=0.8, epochs=200)
    assert np.isclose(weight[0, 1], 0.0, atol=1e-6)
    assert np.isclose(weight[0, 2], 0.0, atol=1e-6)
    assert np.isclose(weight[0, 3], 0.0, atol=1e-6)


def test_lower_l1_ratio_produces_less_sparsity():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(300, 6))
    true_w = np.zeros(6)
    true_w[[0, 3]] = [3.0, -2.0]
    y = x @ true_w + rng.normal(scale=0.2, size=300)

    mostly_lasso, _ = elastic_net_coordinate_descent(x, y, alpha=0.5, l1_ratio=0.99, epochs=300)
    mostly_ridge, _ = elastic_net_coordinate_descent(x, y, alpha=0.5, l1_ratio=0.01, epochs=300)

    lasso_zeros = np.sum(np.abs(mostly_lasso) < 1e-6)
    ridge_zeros = np.sum(np.abs(mostly_ridge) < 1e-6)
    assert lasso_zeros >= ridge_zeros


def test_elastic_net_includes_the_l2_denominator_term():
    # Directly targets a mutant that forgets the extra l2_penalty term
    # in the denominator (reducing to plain Lasso regardless of
    # l1_ratio): with l1_ratio=0.0 (pure Ridge behavior expected), the
    # result must differ meaningfully from the l1_ratio=1.0 (pure
    # Lasso) result on data with correlated features.
    rng = np.random.default_rng(4)
    base = rng.normal(size=300)
    x = np.column_stack([base, base + rng.normal(scale=0.01, size=300)])  # highly correlated
    y = 2.0 * base + rng.normal(scale=0.1, size=300)

    ridge_like, _ = elastic_net_coordinate_descent(x, y, alpha=0.5, l1_ratio=0.01, epochs=300)
    lasso_like, _ = elastic_net_coordinate_descent(x, y, alpha=0.5, l1_ratio=1.0, epochs=300)

    # Ridge-like elastic net should keep both correlated weights closer
    # together (both nonzero), while Lasso-like tends to favor one.
    ridge_like_both_nonzero = np.all(np.abs(ridge_like) > 1e-3)
    assert ridge_like_both_nonzero
