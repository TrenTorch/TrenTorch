"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
householder_vector = _module.householder_vector
householder_matrix = _module.householder_matrix
apply_householder = _module.apply_householder


def _random(shape, seed=0):
    return np.random.default_rng(seed).normal(size=shape)


# ---- 1-5: the mirror direction ----


def test_1_sends_a_vector_onto_the_first_axis():
    x = np.array([3.0, 4.0])
    h = householder_matrix(householder_vector(x))
    np.testing.assert_allclose(h @ x, [-5.0, 0.0], atol=1e-12)


def test_2_target_sign_is_opposite_to_the_first_entry():
    x = np.array([-3.0, 4.0])
    h = householder_matrix(householder_vector(x))
    np.testing.assert_allclose(h @ x, [5.0, 0.0], atol=1e-12)


def test_3_works_in_higher_dimensions_for_many_random_vectors():
    for seed in range(8):
        x = _random(6, seed)
        h = householder_matrix(householder_vector(x))
        result = h @ x
        np.testing.assert_allclose(result[1:], np.zeros(5), atol=1e-12)
        assert np.isclose(abs(result[0]), np.linalg.norm(x))
        assert np.isclose(result[0], -np.sign(x[0]) * np.linalg.norm(x))


def test_4_zero_first_entry_counts_as_positive():
    x = np.array([0.0, 2.0, 0.0])
    h = householder_matrix(householder_vector(x))
    np.testing.assert_allclose(h @ x, [-2.0, 0.0, 0.0], atol=1e-12)


def test_5_zero_vector_gives_the_zero_direction_and_the_identity():
    v = householder_vector(np.zeros(4))
    np.testing.assert_array_equal(v, np.zeros(4))
    np.testing.assert_allclose(householder_matrix(v), np.eye(4))


def test_6_no_cancellation_when_x_is_nearly_on_the_first_axis():
    x = np.array([1.0, 1e-9, 1e-9])
    v = householder_vector(x)
    assert np.isclose(v[0], 2.0)  # 1 + norm(x), not 1 - norm(x)
    h = householder_matrix(v)
    np.testing.assert_allclose(h @ x, [-np.linalg.norm(x), 0.0, 0.0], atol=1e-15)


def test_7_input_is_not_modified():
    x = np.array([1.0, 2.0, 3.0])
    original = x.copy()
    householder_vector(x)
    np.testing.assert_array_equal(x, original)


# ---- 8-12: the reflection matrix ----


def test_8_matrix_matches_a_hand_computed_case():
    # v = [1, 0]: reflects across the vertical axis, so x flips sign
    np.testing.assert_allclose(householder_matrix(np.array([1.0, 0.0])), [[-1.0, 0.0], [0.0, 1.0]])


def test_9_matrix_is_symmetric_orthogonal_and_an_involution():
    h = householder_matrix(_random(5, 1))
    np.testing.assert_allclose(h, h.T, atol=1e-12)
    np.testing.assert_allclose(h.T @ h, np.eye(5), atol=1e-12)
    np.testing.assert_allclose(h @ h, np.eye(5), atol=1e-12)


def test_10_determinant_is_minus_one():
    assert np.isclose(np.linalg.det(householder_matrix(_random(4, 2))), -1.0)


def test_11_preserves_lengths_and_the_mirror_direction_flips():
    v = _random(5, 3)
    h = householder_matrix(v)
    a = _random(5, 4)
    assert np.isclose(np.linalg.norm(h @ a), np.linalg.norm(a))
    np.testing.assert_allclose(h @ v, -v, atol=1e-12)


def test_12_scaling_the_direction_does_not_change_the_reflection():
    v = _random(4, 5)
    np.testing.assert_allclose(householder_matrix(v), householder_matrix(7.5 * v), atol=1e-12)


# ---- 13-17: applying the reflection ----


def test_13_apply_matches_the_explicit_matrix_on_a_vector():
    v, a = _random(6, 6), _random(6, 7)
    np.testing.assert_allclose(apply_householder(v, a), householder_matrix(v) @ a, atol=1e-12)


def test_14_apply_matches_the_explicit_matrix_on_a_matrix():
    v, a = _random(5, 8), _random(5 * 3, 9).reshape(5, 3)
    result = apply_householder(v, a)
    assert result.shape == (5, 3)
    np.testing.assert_allclose(result, householder_matrix(v) @ a, atol=1e-12)


def test_15_apply_with_a_zero_direction_returns_an_unchanged_copy():
    a = _random(4, 10)
    result = apply_householder(np.zeros(4), a)
    np.testing.assert_array_equal(result, a)
    assert result is not a


def test_16_apply_does_not_modify_its_inputs():
    v, a = _random(4, 11), _random(4 * 2, 12).reshape(4, 2)
    v_copy, a_copy = v.copy(), a.copy()
    apply_householder(v, a)
    np.testing.assert_array_equal(v, v_copy)
    np.testing.assert_array_equal(a, a_copy)


def test_17_zeroing_a_column_then_applying_the_same_mirror_to_other_columns():
    a = np.array([[4.0, 1.0], [3.0, 2.0]])
    v = householder_vector(a[:, 0])
    result = apply_householder(v, a)
    np.testing.assert_allclose(result[:, 0], [-5.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(result[:, 1], householder_matrix(v) @ a[:, 1], atol=1e-12)
