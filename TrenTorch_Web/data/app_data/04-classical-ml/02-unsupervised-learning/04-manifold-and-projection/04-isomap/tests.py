"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

isomap = load_solution(__file__).isomap


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _line():
    t = np.array([0.0, 1.0, 2.5, 4.0, 6.0, 7.5])
    return np.column_stack([t, np.zeros_like(t)]), t


def _dist1d(z):
    return np.abs(z[:, None, 0] - z[None, :, 0])


def test_output_shape_is_n_by_components():
    X, _ = _line()
    assert isomap(X, 2, 2).shape == (6, 2)


def test_points_on_a_line_recover_their_spacing():
    X, t = _line()
    Z = isomap(X, 2, 1)
    assert np.allclose(_dist1d(Z), np.abs(t[:, None] - t[None, :]), atol=1e-8)


def test_curved_path_uses_arc_length_not_straight_chord():
    theta = np.linspace(0.0, np.pi, 30)
    X = np.column_stack([np.cos(theta), np.sin(theta)])
    Z = isomap(X, 2, 1)
    ends = np.linalg.norm(Z[0] - Z[-1])
    arc = np.pi
    assert abs(ends - arc) < 0.2


def test_centered_embedding():
    X, _ = _line()
    Z = isomap(X, 2, 1)
    assert np.allclose(Z.mean(axis=0), 0.0, atol=1e-9)


def test_disconnected_graph_raises():
    X = np.array([[0.0, 0.0], [0.1, 0.0], [100.0, 0.0], [100.1, 0.0]])
    assert _raises_value_error(isomap, X, 1, 1)


def test_n_neighbors_out_of_range_raises():
    X, _ = _line()
    assert _raises_value_error(isomap, X, 0, 1)
    assert _raises_value_error(isomap, X, 6, 1)


def test_components_out_of_range_raises():
    X, _ = _line()
    assert _raises_value_error(isomap, X, 2, 0)
    assert _raises_value_error(isomap, X, 2, 7)


def test_same_input_gives_same_embedding():
    X, _ = _line()
    assert np.array_equal(isomap(X, 2, 1), isomap(X, 2, 1))


def test_does_not_modify_the_data():
    X, _ = _line()
    before = X.copy()
    isomap(X, 2, 1)
    assert np.array_equal(X, before)
