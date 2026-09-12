"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/02-dot-product-norms/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}"
)
dot_product = _module.dot_product
l1_norm = _module.l1_norm
l2_norm = _module.l2_norm
linf_norm = _module.linf_norm


def test_dot_product_matches_hand_computation():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
    assert np.isclose(dot_product(a, b), 32.0)


def test_dot_product_of_orthogonal_vectors_is_zero():
    assert np.isclose(dot_product(np.array([1.0, 0.0]), np.array([0.0, 1.0])), 0.0)


def test_dot_product_returns_a_plain_scalar():
    result = dot_product(np.array([1.0, 2.0]), np.array([3.0, 4.0]))
    assert np.isscalar(result) or isinstance(result, float)


def test_l1_norm_matches_hand_computation():
    x = np.array([3.0, -4.0, 0.0])
    assert np.isclose(l1_norm(x), 7.0)


def test_l2_norm_matches_hand_computation():
    # classic 3-4-5 triangle
    x = np.array([3.0, 4.0])
    assert np.isclose(l2_norm(x), 5.0)


def test_l2_norm_equals_sqrt_of_self_dot_product():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    assert np.isclose(l2_norm(x), np.sqrt(dot_product(x, x)))


def test_linf_norm_matches_hand_computation():
    x = np.array([3.0, -7.0, 5.0])
    assert np.isclose(linf_norm(x), 7.0)


def test_norms_are_never_negative():
    rng = np.random.default_rng(1)
    x = rng.normal(size=8)
    assert l1_norm(x) >= 0.0
    assert l2_norm(x) >= 0.0
    assert linf_norm(x) >= 0.0


def test_l1_l2_linf_ordering_on_a_spread_out_vector():
    # A well-known norm inequality: ||x||_inf <= ||x||_2 <= ||x||_1 for
    # any vector (with equality only in degenerate cases). Directly
    # catches a mutant that swaps two of the three norm implementations.
    x = np.array([3.0, 4.0, 0.0])
    assert linf_norm(x) <= l2_norm(x) <= l1_norm(x)


def test_l2_norm_not_confused_with_l1_norm():
    # Directly targets a mutant that implements l2_norm as a plain sum
    # of absolute values (i.e. copies l1_norm's body). For x=[3, 4],
    # l1 gives 7, l2 gives 5 -- clearly different.
    x = np.array([3.0, 4.0])
    assert np.isclose(l2_norm(x), 5.0)
    assert not np.isclose(l2_norm(x), 7.0)
