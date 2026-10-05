"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
train_linear_probe = _module.train_linear_probe
probe_accuracy = _module.probe_accuracy


def _data(seed=0, n=200):
    rng = np.random.RandomState(seed)
    y = (np.arange(n) % 2).astype(int)
    X = rng.randn(n, 5) * 0.5
    X[:, 2] += np.where(y == 1, 2.0, -2.0)
    return X, y


def test_1_separable_data_is_learned():
    X, y = _data()
    w, b = train_linear_probe(X, y, steps=400, lr=0.5, l2=0.0)
    assert probe_accuracy(X, y, w, b) > 0.98


def test_2_probe_finds_the_informative_dimension():
    X, y = _data(1)
    w, _ = train_linear_probe(X, y, steps=400, lr=0.5, l2=0.01)
    assert int(np.argmax(np.abs(w))) == 2 and w[2] > 0


def test_3_one_step_hand_computed():
    X = np.array([[1.0], [-1.0]])
    y = np.array([1, 0])
    w, b = train_linear_probe(X, y, steps=1, lr=1.0, l2=0.0)
    # p = 0.5 each; r = [-0.5, 0.5]; grad_w = (1*-0.5 + -1*0.5)/2 = -0.5 ; grad_b = 0
    assert np.allclose(w, [0.5]) and np.isclose(b, 0.0)


def test_4_l2_shrinks_the_weights():
    X, y = _data(2)
    w0, _ = train_linear_probe(X, y, steps=300, lr=0.5, l2=0.0)
    w1, _ = train_linear_probe(X, y, steps=300, lr=0.5, l2=1.0)
    assert np.linalg.norm(w1) < np.linalg.norm(w0)


def test_5_accuracy_hand_computed():
    X = np.array([[1.0], [2.0], [-1.0], [-3.0]])
    y = np.array([1, 0, 0, 0])
    assert np.isclose(probe_accuracy(X, y, np.array([1.0]), 0.0), 0.75)


def test_6_random_labels_are_not_learnable_beyond_chance_on_heldout_data():
    rng = np.random.RandomState(3)
    X_tr, X_te = rng.randn(60, 4), rng.randn(400, 4)
    y_tr, y_te = rng.randint(0, 2, 60), rng.randint(0, 2, 400)
    w, b = train_linear_probe(X_tr, y_tr, steps=300, lr=0.3, l2=0.1)
    assert abs(probe_accuracy(X_te, y_te, w, b) - 0.5) < 0.12


def test_7_inputs_untouched_and_stable_for_large_features():
    X, y = _data(4)
    X = X * 1e3
    s = X.copy()
    w, b = train_linear_probe(X, y, steps=20, lr=1e-3, l2=0.0)
    assert np.all(np.isfinite(w)) and np.isfinite(b)
    assert np.array_equal(X, s)
