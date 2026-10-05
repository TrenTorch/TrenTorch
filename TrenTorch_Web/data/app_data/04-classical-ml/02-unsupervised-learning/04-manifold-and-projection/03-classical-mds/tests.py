"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

classical_mds = load_solution(__file__).classical_mds


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _points():
    return np.array([[0.0, 0.0], [3.0, 0.0], [0.0, 4.0], [3.0, 4.0], [1.5, 2.0]])


def _dist(P):
    return np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)


def test_planar_points_are_recovered_exactly_in_two_dimensions():
    D = _dist(_points())
    Z = classical_mds(D, 2)
    assert np.allclose(_dist(Z), D, atol=1e-8)


def test_output_shape_is_n_by_k():
    D = _dist(_points())
    assert classical_mds(D, 2).shape == (5, 2)


def test_embedding_is_centered():
    Z = classical_mds(_dist(_points()), 2)
    assert np.allclose(Z.mean(axis=0), 0.0, atol=1e-9)


def test_one_dimensional_line_embeds_in_one_axis():
    x = np.array([0.0, 1.0, 3.0, 6.0])
    D = np.abs(x[:, None] - x[None, :])
    Z = classical_mds(D, 1)
    assert np.allclose(_dist(Z), D, atol=1e-8)


def test_translation_invariant_distances_give_same_embedding_distances():
    D = _dist(_points())
    assert np.allclose(_dist(classical_mds(D, 2)), _dist(classical_mds(D, 2)))


def test_nonsquare_matrix_raises():
    assert _raises_value_error(classical_mds, np.ones((3, 4)), 2)


def test_asymmetric_matrix_raises():
    D = np.array([[0.0, 1.0], [2.0, 0.0]])
    assert _raises_value_error(classical_mds, D, 1)


def test_nonzero_diagonal_raises():
    D = np.array([[1.0, 1.0], [1.0, 1.0]])
    assert _raises_value_error(classical_mds, D, 1)


def test_k_out_of_range_raises():
    D = _dist(_points())
    assert _raises_value_error(classical_mds, D, 0)
    assert _raises_value_error(classical_mds, D, 6)


def test_same_input_gives_same_embedding():
    D = _dist(_points())
    assert np.array_equal(classical_mds(D, 2), classical_mds(D, 2))


def test_does_not_modify_the_distances():
    D = _dist(_points())
    before = D.copy()
    classical_mds(D, 2)
    assert np.array_equal(D, before)
