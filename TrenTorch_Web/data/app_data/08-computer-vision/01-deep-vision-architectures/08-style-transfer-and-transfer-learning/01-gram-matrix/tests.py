"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
gram_matrix = _module.gram_matrix


def test_1_hand_computed():
    f = np.array([[[1.0, 2.0]], [[3.0, 4.0]]])  # C=2, H=1, W=2
    # F = [[1,2],[3,4]] ; F F^T = [[5,11],[11,25]] ; / (2*1*2)
    assert np.allclose(gram_matrix(f), np.array([[5, 11], [11, 25]]) / 4)


def test_2_symmetric_and_positive_semidefinite():
    g = gram_matrix(np.random.RandomState(0).randn(4, 5, 5))
    assert np.allclose(g, g.T) and np.linalg.eigvalsh(g).min() > -1e-12


def test_3_shape():
    assert gram_matrix(np.zeros((6, 3, 4))).shape == (6, 6)


def test_4_invariant_to_permuting_positions():
    f = np.random.RandomState(1).randn(3, 4, 4)
    flat = f.reshape(3, -1)
    perm = np.random.RandomState(2).permutation(16)
    assert np.allclose(gram_matrix(f), gram_matrix(flat[:, perm].reshape(3, 4, 4)))


def test_5_translating_a_pattern_does_not_change_it():
    f = np.zeros((2, 6, 6))
    f[0, 1:3, 1:3] = 1.0
    f[1, 1:3, 1:3] = 2.0
    shifted = np.roll(f, (2, 3), axis=(1, 2))
    assert np.allclose(gram_matrix(f), gram_matrix(shifted))


def test_6_normalization_makes_size_comparable():
    f = np.ones((2, 3, 3))
    big = np.ones((2, 6, 6))
    assert np.allclose(gram_matrix(f), gram_matrix(big))


def test_7_input_untouched():
    f = np.random.RandomState(3).randn(2, 3, 3)
    snap = f.copy()
    gram_matrix(f)
    assert np.array_equal(f, snap)
