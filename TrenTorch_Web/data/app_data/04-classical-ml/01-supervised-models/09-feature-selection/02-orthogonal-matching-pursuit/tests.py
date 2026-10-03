"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
omp = _module.omp


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_identity_dictionary_recovers_the_sparse_target():
    D = np.eye(4)
    y = np.array([0.0, 3.0, 0.0, -1.0])
    assert np.allclose(omp(D, y, 2), [0.0, 3.0, 0.0, -1.0])


def test_largest_magnitude_atom_is_picked_first():
    # y = 2 * e3 - e1; with k = 1 only the larger coefficient is chosen.
    D = np.eye(5)
    y = np.array([-1.0, 0.0, 0.0, 2.0, 0.0])
    x = omp(D, y, 1)
    assert np.allclose(x, [0.0, 0.0, 0.0, 2.0, 0.0])


def test_ties_go_to_the_smallest_index():
    D = np.eye(3)
    y = np.array([1.0, 1.0, 0.0])
    assert np.allclose(omp(D, y, 1), [1.0, 0.0, 0.0])


def test_k_zero_returns_all_zeros():
    rng = np.random.default_rng(0)
    D = rng.normal(size=(6, 4))
    assert np.array_equal(omp(D, rng.normal(size=6), 0), np.zeros(4))


def test_recovers_a_two_sparse_signal_from_a_random_dictionary():
    rng = np.random.default_rng(1)
    D = rng.normal(size=(20, 40))
    x_true = np.zeros(40)
    x_true[5], x_true[17] = 1.5, -2.0
    y = D @ x_true
    assert np.allclose(omp(D, y, 2), x_true, atol=1e-8)


def test_output_has_at_most_k_nonzeros():
    rng = np.random.default_rng(2)
    D = rng.normal(size=(15, 30))
    y = rng.normal(size=15)
    assert np.count_nonzero(omp(D, y, 4)) <= 4


def test_residual_is_orthogonal_to_the_selected_columns():
    rng = np.random.default_rng(3)
    D = rng.normal(size=(12, 20))
    y = rng.normal(size=12)
    x = omp(D, y, 3)
    support = np.flatnonzero(x)
    residual = y - D @ x
    assert np.allclose(D[:, support].T @ residual, 0.0, atol=1e-10)


def test_error_does_not_increase_when_k_grows():
    rng = np.random.default_rng(4)
    D = rng.normal(size=(18, 25))
    y = rng.normal(size=18)
    errors = [np.linalg.norm(y - D @ omp(D, y, k)) for k in range(0, 6)]
    assert all(b <= a + 1e-12 for a, b in zip(errors, errors[1:]))


def test_output_length_is_the_number_of_atoms():
    rng = np.random.default_rng(5)
    D = rng.normal(size=(7, 9))
    assert omp(D, rng.normal(size=7), 2).shape == (9,)


def test_k_larger_than_number_of_atoms_raises():
    assert _raises_value_error(omp, np.zeros((4, 2)), np.zeros(4), 3)


def test_negative_k_raises():
    assert _raises_value_error(omp, np.zeros((4, 2)), np.zeros(4), -1)


def test_length_mismatch_raises():
    assert _raises_value_error(omp, np.zeros((4, 2)), np.zeros(3), 1)


def test_does_not_modify_inputs():
    rng = np.random.default_rng(6)
    D = rng.normal(size=(6, 5))
    y = rng.normal(size=6)
    D0, y0 = D.copy(), y.copy()
    omp(D, y, 2)
    assert np.array_equal(D, D0) and np.array_equal(y, y0)
