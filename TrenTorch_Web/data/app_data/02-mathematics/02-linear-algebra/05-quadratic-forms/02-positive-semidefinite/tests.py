"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
is_positive_semidefinite = _module.is_positive_semidefinite
gram_matrix = _module.gram_matrix
nearest_psd = _module.nearest_psd


def _random(shape, seed=0):
    return np.random.default_rng(seed).normal(size=shape)


# ---- 1-7: the test ----


def test_1_positive_definite_matrices_pass():
    assert is_positive_semidefinite(np.array([[2.0, 0.0], [0.0, 3.0]]))


def test_2_singular_psd_matrix_passes_but_is_not_positive_definite():
    a = np.array([[1.0, 1.0], [1.0, 1.0]])  # eigenvalues 0 and 2
    assert is_positive_semidefinite(a)
    assert np.linalg.eigvalsh(a)[0] < 1e-12


def test_3_zero_matrix_passes():
    assert is_positive_semidefinite(np.zeros((3, 3)))


def test_4_negative_eigenvalue_fails():
    assert not is_positive_semidefinite(np.array([[1.0, 0.0], [0.0, -1e-3]]))
    assert not is_positive_semidefinite(np.array([[0.0, 1.0], [1.0, 0.0]]))  # eigenvalues +1, -1


def test_5_rounding_sized_negative_eigenvalue_is_tolerated():
    assert is_positive_semidefinite(np.array([[1.0, 0.0], [0.0, -1e-12]]))
    assert not is_positive_semidefinite(np.array([[1.0, 0.0], [0.0, -1e-12]]), tol=0.0)


def test_6_non_symmetric_and_non_square_inputs_fail():
    assert not is_positive_semidefinite(np.array([[1.0, 2.0], [0.0, 1.0]]))
    assert not is_positive_semidefinite(np.ones((2, 3)))


def test_7_negative_semidefinite_fails():
    assert not is_positive_semidefinite(np.array([[-1.0, 0.0], [0.0, 0.0]]))


# ---- 8-11: Gram matrices ----


def test_8_gram_matrix_hand_computed():
    x = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 2.0]])
    expected = [[1.0, 1.0, 0.0], [1.0, 2.0, 2.0], [0.0, 2.0, 4.0]]
    np.testing.assert_allclose(gram_matrix(x), expected)


def test_9_gram_matrix_is_always_psd():
    for seed in range(6):
        g = gram_matrix(_random((5, 3), seed))
        assert is_positive_semidefinite(g)


def test_10_gram_matrix_of_dependent_rows_is_singular():
    g = gram_matrix(_random((6, 2), 1))  # 6 vectors in 2D
    assert np.linalg.matrix_rank(g) == 2
    assert is_positive_semidefinite(g)


def test_11_gram_matrix_is_symmetric_and_the_right_shape():
    g = gram_matrix(_random((4, 7), 2))
    assert g.shape == (4, 4)
    np.testing.assert_allclose(g, g.T)


# ---- 12-17: nearest PSD matrix ----


def test_12_psd_input_is_returned_unchanged():
    a = gram_matrix(_random((4, 4), 3))
    np.testing.assert_allclose(nearest_psd(a), a, atol=1e-10)


def test_13_result_is_psd_and_symmetric():
    a = _random((5, 5), 4)
    result = nearest_psd(a)
    np.testing.assert_allclose(result, result.T, atol=1e-12)
    assert is_positive_semidefinite(result)


def test_14_clips_a_negative_eigenvalue_to_zero_on_a_diagonal_matrix():
    result = nearest_psd(np.diag([3.0, -2.0, 1.0]))
    np.testing.assert_allclose(result, np.diag([3.0, 0.0, 1.0]), atol=1e-12)


def test_15_is_closer_to_the_input_than_other_psd_matrices():
    a = _random((4, 4), 5)
    sym = (a + a.T) / 2
    best = np.linalg.norm(sym - nearest_psd(a))
    for seed in range(20):
        other = gram_matrix(_random((4, 4), 100 + seed))
        assert best <= np.linalg.norm(sym - other) + 1e-12


def test_16_non_symmetric_input_is_symmetrized_first():
    a = np.array([[2.0, 1.0], [3.0, 2.0]])
    np.testing.assert_allclose(nearest_psd(a), nearest_psd((a + a.T) / 2), atol=1e-12)


def test_17_input_is_not_modified():
    a = _random((4, 4), 6)
    original = a.copy()
    nearest_psd(a)
    np.testing.assert_array_equal(a, original)
