"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
bigram_net_loss = _module.bigram_net_loss
bigram_net_gradient = _module.bigram_net_gradient
train_bigram_net = _module.train_bigram_net

XS = np.array([0, 0, 0, 1, 1, 2])
YS = np.array([1, 1, 2, 0, 2, 0])


def test_1_zero_weights_give_log_v():
    assert np.isclose(bigram_net_loss(np.zeros((3, 3)), XS, YS), np.log(3))


def test_2_gradient_matches_finite_differences():
    rng = np.random.RandomState(0)
    W = rng.randn(3, 3)
    g = bigram_net_gradient(W, XS, YS)
    eps = 1e-6
    for i in range(3):
        for j in range(3):
            Wp, Wm = W.copy(), W.copy()
            Wp[i, j] += eps
            Wm[i, j] -= eps
            numeric = (bigram_net_loss(Wp, XS, YS) - bigram_net_loss(Wm, XS, YS)) / (2 * eps)
            assert np.isclose(g[i, j], numeric, atol=1e-6)


def test_3_gradient_hand_computed_at_zero():
    # all rows uniform (1/3). Row 2 has the single pair (2 -> 0):
    # grad row = (1/3 - [1,0,0]) / 6 pairs
    g = bigram_net_gradient(np.zeros((3, 3)), XS, YS)
    assert np.allclose(g[2], np.array([1 / 3 - 1, 1 / 3, 1 / 3]) / 6)


def test_4_repeated_input_rows_accumulate():
    xs = np.array([0, 0, 0, 0])
    ys = np.array([1, 1, 1, 1])
    g = bigram_net_gradient(np.zeros((2, 2)), xs, ys)
    assert np.allclose(g[0], [0.5, -0.5])
    assert np.allclose(g[1], 0.0)


def test_5_training_lowers_the_loss():
    W0 = np.zeros((3, 3))
    W = train_bigram_net(XS, YS, 3, steps=50, lr=1.0)
    assert bigram_net_loss(W, XS, YS) < bigram_net_loss(W0, XS, YS)


def test_6_training_approaches_the_count_estimate():
    W = train_bigram_net(XS, YS, 3, steps=4000, lr=2.0)
    e = np.exp(W - W.max(axis=1, keepdims=True))
    p = e / e.sum(axis=1, keepdims=True)
    mle = np.array([[0, 2 / 3, 1 / 3], [0.5, 0, 0.5], [1, 0, 0]])
    assert np.allclose(p, mle, atol=0.05)


def test_7_unseen_rows_stay_uniform_and_inputs_untouched():
    xs, ys = np.array([0, 0, 1]), np.array([1, 2, 0])
    snap = (xs.copy(), ys.copy())
    W = train_bigram_net(xs, ys, 4, steps=100, lr=1.0)
    assert np.allclose(W[2], 0.0) and np.allclose(W[3], 0.0)
    assert np.array_equal(xs, snap[0]) and np.array_equal(ys, snap[1])
