"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
propagate = _module.propagate

TWO_NODES = np.array([[0.0, 1.0], [1.0, 0.0]])
SEED = np.array([[1.0, 0.0], [0.0, 0.0]])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_two_node_chain_matches_closed_form():
    # F* = (1 / (1 + alpha)) [[1, 0], [alpha, 0]] for this graph.
    F = propagate(TWO_NODES, SEED, alpha=0.5, iters=300)
    assert np.isclose(F[0, 0], 2 / 3)
    assert np.isclose(F[1, 0], 1 / 3)


def test_zero_iterations_returns_seed_labels():
    F = propagate(TWO_NODES, SEED, alpha=0.5, iters=0)
    assert np.array_equal(F, SEED)


def test_one_iteration_matches_update_formula():
    # F1 = alpha * S Y0 + (1 - alpha) * Y0; S = W for unit degrees.
    # S Y0 = [[0, 0], [1, 0]], so F1 = 0.5 * [[0, 0], [1, 0]] + 0.5 * [[1, 0], [0, 0]].
    F = propagate(TWO_NODES, SEED, alpha=0.5, iters=1)
    assert np.allclose(F, [[0.5, 0.0], [0.5, 0.0]])


def test_output_shape_matches_seed_matrix():
    W = np.ones((4, 4)) - np.eye(4)
    Y0 = np.eye(4)[:, :2]
    assert propagate(W, Y0, 0.3, 50).shape == (4, 2)


def test_fully_connected_graph_gives_equal_scores_for_symmetric_seed():
    W = np.ones((3, 3)) - np.eye(3)
    Y0 = np.array([[1.0], [0.0], [0.0]])
    F = propagate(W, Y0, 0.5, 500)
    assert np.isclose(F[1, 0], F[2, 0])


def test_larger_alpha_spreads_label_further():
    W = np.ones((3, 3)) - np.eye(3)
    Y0 = np.array([[1.0], [0.0], [0.0]])
    weak = propagate(W, Y0, 0.1, 500)[1, 0]
    strong = propagate(W, Y0, 0.9, 500)[1, 0]
    assert strong > weak


def test_seeded_node_keeps_the_largest_score_of_its_class():
    W = np.ones((4, 4)) - np.eye(4)
    Y0 = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
    F = propagate(W, Y0, 0.5, 400)
    assert F[0, 0] > F[0, 1]


def test_asymmetric_graph_raises():
    W = np.array([[0.0, 1.0], [0.0, 0.0]])
    assert _raises_value_error(propagate, W, SEED, 0.5, 5)


def test_negative_edge_weight_raises():
    W = np.array([[0.0, -1.0], [-1.0, 0.0]])
    assert _raises_value_error(propagate, W, SEED, 0.5, 5)


def test_isolated_node_raises():
    W = np.zeros((2, 2))
    assert _raises_value_error(propagate, W, SEED, 0.5, 5)


def test_alpha_at_boundary_raises():
    assert _raises_value_error(propagate, TWO_NODES, SEED, 1.0, 5)
    assert _raises_value_error(propagate, TWO_NODES, SEED, 0.0, 5)


def test_negative_iterations_raise():
    assert _raises_value_error(propagate, TWO_NODES, SEED, 0.5, -1)


def test_row_count_mismatch_raises():
    assert _raises_value_error(propagate, TWO_NODES, np.ones((3, 1)), 0.5, 5)


def test_inputs_are_not_modified():
    W = TWO_NODES.copy()
    Y0 = SEED.copy()
    propagate(W, Y0, 0.5, 20)
    assert np.array_equal(W, TWO_NODES) and np.array_equal(Y0, SEED)
