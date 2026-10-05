"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

perceptron_train = load_solution(__file__).perceptron_train


def _predict(X, w, b):
    return (X @ w + b > 0).astype(int)


def test_one_hand_computed_update():
    w, b = perceptron_train(np.array([[1.0, 2.0]]), np.array([1]), epochs=1)
    assert np.allclose(w, [1.0, 2.0])
    assert np.isclose(b, 1.0)


def test_learning_rate_scales_the_update():
    w, b = perceptron_train(np.array([[1.0, 2.0]]), np.array([1]), lr=0.5, epochs=1)
    assert np.allclose(w, [0.5, 1.0])
    assert np.isclose(b, 0.5)


def test_learns_and():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([0, 0, 0, 1])
    w, b = perceptron_train(X, y)
    assert _predict(X, w, b).tolist() == y.tolist()


def test_learns_or():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([0, 1, 1, 1])
    w, b = perceptron_train(X, y)
    assert _predict(X, w, b).tolist() == y.tolist()


def test_cannot_learn_xor():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([0, 1, 1, 0])
    w, b = perceptron_train(X, y, epochs=1000)
    assert (_predict(X, w, b) == y).mean() < 1.0


def test_separates_well_separated_blobs():
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(-3, 0.5, size=(30, 2)), rng.normal(3, 0.5, size=(30, 2))])
    y = np.array([0] * 30 + [1] * 30)
    w, b = perceptron_train(X, y, epochs=200)
    assert (_predict(X, w, b) == y).all()


def test_does_not_modify_inputs():
    X = np.array([[1.0, 2.0], [-1.0, -2.0]])
    y = np.array([1, 0])
    X0, y0 = X.copy(), y.copy()
    perceptron_train(X, y)
    assert np.array_equal(X, X0) and np.array_equal(y, y0)


def test_return_types():
    w, b = perceptron_train(np.array([[1.0, 2.0]]), np.array([1]))
    assert isinstance(w, np.ndarray) and isinstance(b, float)
