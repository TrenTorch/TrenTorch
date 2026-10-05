"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
cooccurrence_matrix = _module.cooccurrence_matrix
glove_weight = _module.glove_weight
glove_loss = _module.glove_loss


def test_1_cooccurrence_hand_computed():
    X = cooccurrence_matrix([0, 1, 2], 3, 2)
    expected = np.array([[0, 1, 0.5], [1, 0, 1], [0.5, 1, 0]])
    assert np.allclose(X, expected)


def test_2_cooccurrence_is_symmetric_and_counts_repeats():
    X = cooccurrence_matrix([0, 1, 0, 1], 2, 1)
    assert np.allclose(X, X.T) and np.isclose(X[0, 1], 3.0)


def test_3_weight_function():
    w = glove_weight(np.array([0.0, 50.0, 100.0, 400.0]), 100.0, 0.75)
    assert np.allclose(w, [0.0, 0.5 ** 0.75, 1.0, 1.0])


def test_4_perfect_fit_has_zero_loss():
    X = np.array([[0, 4.0], [4.0, 0]])
    W = np.array([[1.0, 0.0], [0.0, 1.0]])
    Wt = np.array([[0.0, np.log(4.0)], [np.log(4.0), 0.0]])
    assert np.isclose(glove_loss(W, Wt, np.zeros(2), np.zeros(2), X, 100.0, 0.75), 0.0)


def test_5_hand_computed_single_pair():
    X = np.array([[0.0, 2.0], [0.0, 0.0]])
    W = np.array([[1.0, 1.0], [0.0, 0.0]])
    Wt = np.array([[0.0, 0.0], [1.0, 2.0]])
    # pred = 3 + b ; target ln 2 ; f = (2/10)^0.5
    loss = glove_loss(W, Wt, np.zeros(2), np.zeros(2), X, 10.0, 0.5)
    assert np.isclose(loss, (0.2 ** 0.5) * (3 - np.log(2)) ** 2)


def test_6_zero_cooccurrence_pairs_are_ignored():
    X = np.array([[0.0, 3.0], [0.0, 0.0]])
    rng = np.random.RandomState(0)
    W, Wt = rng.randn(2, 2), rng.randn(2, 2)
    b, bt = rng.randn(2), rng.randn(2)
    a = glove_loss(W, Wt, b, bt, X, 100.0, 0.75)
    Wt2 = Wt.copy()
    Wt2[0] += 100.0  # only affects pairs (i, 0), whose X is zero
    assert np.isclose(a, glove_loss(W, Wt2, b, bt, X, 100.0, 0.75))


def test_7_inputs_untouched():
    X = np.array([[0.0, 2.0], [2.0, 0.0]])
    W, Wt = np.ones((2, 2)), np.ones((2, 2))
    sx = X.copy()
    glove_loss(W, Wt, np.zeros(2), np.zeros(2), X, 10.0, 0.75)
    assert np.array_equal(X, sx)
