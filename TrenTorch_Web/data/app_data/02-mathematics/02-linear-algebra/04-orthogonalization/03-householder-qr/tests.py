"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
householder_qr = _module.householder_qr
back_substitution = _module.back_substitution
least_squares_qr = _module.least_squares_qr


def _random(m, n, seed=0):
    return np.random.default_rng(seed).normal(size=(m, n))


# ---- 1-8: the factorization ----


def test_1_reconstructs_the_matrix():
    a = _random(6, 4, 1)
    q, r = householder_qr(a)
    np.testing.assert_allclose(q @ r, a, atol=1e-12)


def test_2_q_is_orthogonal():
    q, _ = householder_qr(_random(5, 3, 2))
    np.testing.assert_allclose(q.T @ q, np.eye(5), atol=1e-12)
    np.testing.assert_allclose(q @ q.T, np.eye(5), atol=1e-12)


def test_3_r_is_upper_triangular_with_exact_zeros():
    _, r = householder_qr(_random(6, 4, 3))
    assert r.shape == (6, 4)
    assert np.all(np.tril(r, -1) == 0.0)


def test_4_shapes_for_square_tall_and_single_column_inputs():
    for m, n in [(3, 3), (7, 2), (4, 1), (1, 1)]:
        a = _random(m, n, m + n)
        q, r = householder_qr(a)
        assert q.shape == (m, m) and r.shape == (m, n)
        np.testing.assert_allclose(q @ r, a, atol=1e-12)


def test_5_matches_numpy_qr_up_to_signs():
    a = _random(6, 3, 4)
    _, r = householder_qr(a)
    _, r_numpy = np.linalg.qr(a, mode="complete")
    np.testing.assert_allclose(np.abs(r), np.abs(r_numpy), atol=1e-10)


def test_6_hand_computed_two_by_two_case():
    a = np.array([[3.0, 1.0], [4.0, 2.0]])
    q, r = householder_qr(a)
    assert np.isclose(abs(r[0, 0]), 5.0)
    np.testing.assert_allclose(q @ r, a, atol=1e-12)


def test_7_handles_a_zero_column_without_dividing_by_zero():
    a = np.array([[1.0, 0.0, 2.0], [2.0, 0.0, 1.0], [2.0, 0.0, 3.0]])
    q, r = householder_qr(a)
    assert np.all(np.isfinite(q)) and np.all(np.isfinite(r))
    np.testing.assert_allclose(q @ r, a, atol=1e-12)


def test_8_already_triangular_input_is_still_factored_correctly():
    a = np.array([[2.0, 1.0], [0.0, 3.0], [0.0, 0.0]])
    q, r = householder_qr(a)
    np.testing.assert_allclose(q @ r, a, atol=1e-12)
    np.testing.assert_allclose(q.T @ q, np.eye(3), atol=1e-12)


def test_9_input_is_not_modified():
    a = _random(5, 3, 5)
    original = a.copy()
    householder_qr(a)
    np.testing.assert_array_equal(a, original)


# ---- 10-12: back substitution ----


def test_10_back_substitution_hand_computed():
    r = np.array([[2.0, 1.0], [0.0, 4.0]])
    # 4 x1 = 8 -> x1 = 2; 2 x0 + 2 = 5 -> x0 = 1.5
    np.testing.assert_allclose(back_substitution(r, np.array([5.0, 8.0])), [1.5, 2.0])


def test_11_back_substitution_solves_random_triangular_systems():
    r = np.triu(_random(5, 5, 6)) + 5 * np.eye(5)
    x = np.arange(1.0, 6.0)
    np.testing.assert_allclose(back_substitution(r, r @ x), x, atol=1e-10)


def test_12_back_substitution_one_by_one():
    np.testing.assert_allclose(back_substitution(np.array([[4.0]]), np.array([2.0])), [0.5])


# ---- 13-17: least squares ----


def test_13_recovers_the_solution_of_a_consistent_system():
    a = _random(8, 3, 7)
    x_true = np.array([1.0, -2.0, 0.5])
    np.testing.assert_allclose(least_squares_qr(a, a @ x_true), x_true, atol=1e-10)


def test_14_matches_numpy_lstsq_on_noisy_data():
    rng = np.random.default_rng(8)
    a = rng.normal(size=(30, 4))
    b = a @ np.array([2.0, 0.0, -1.0, 3.0]) + 0.5 * rng.normal(size=30)
    expected = np.linalg.lstsq(a, b, rcond=None)[0]
    np.testing.assert_allclose(least_squares_qr(a, b), expected, atol=1e-10)


def test_15_fits_a_line_to_hand_computed_data():
    t = np.array([0.0, 1.0, 2.0, 3.0])
    a = np.column_stack([np.ones(4), t])
    b = np.array([1.0, 3.0, 5.0, 7.0])  # exactly 1 + 2 t
    np.testing.assert_allclose(least_squares_qr(a, b), [1.0, 2.0], atol=1e-10)


def test_16_residual_is_orthogonal_to_the_columns():
    rng = np.random.default_rng(9)
    a = rng.normal(size=(20, 3))
    b = rng.normal(size=20)
    x = least_squares_qr(a, b)
    np.testing.assert_allclose(a.T @ (a @ x - b), np.zeros(3), atol=1e-10)


def test_17_stays_accurate_where_the_normal_equations_struggle():
    # Nearly dependent columns make A^T A badly conditioned
    t = np.linspace(0, 1, 40)
    a = np.column_stack([np.ones(40), t, t**2, t**3, t**4, t**5, t**6, t**7])
    x_true = np.ones(8)
    got = least_squares_qr(a, a @ x_true)
    np.testing.assert_allclose(got, x_true, atol=1e-5)
