"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sae_forward = _module.sae_forward
sae_loss = _module.sae_loss


def test_1_hand_computed_forward():
    x = np.array([[1.0, 2.0]])
    W_enc = np.array([[1.0, -1.0, 0.0], [0.0, 1.0, 1.0]])
    b_enc = np.array([0.0, 0.0, -5.0])
    W_dec = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    b_dec = np.zeros(2)
    x_hat, f = sae_forward(x, W_enc, b_enc, W_dec, b_dec)
    # pre = [1, 1, -3] -> relu [1, 1, 0]; x_hat = [1, 1]
    assert np.allclose(f, [[1.0, 1.0, 0.0]]) and np.allclose(x_hat, [[1.0, 1.0]])


def test_2_features_are_non_negative_and_shapes_match():
    rng = np.random.RandomState(0)
    x = rng.randn(5, 4)
    x_hat, f = sae_forward(x, rng.randn(4, 12), rng.randn(12), rng.randn(12, 4), rng.randn(4))
    assert f.shape == (5, 12) and x_hat.shape == (5, 4) and (f >= 0).all()


def test_3_decoder_bias_centres_the_input():
    x = np.array([[3.0, 3.0]])
    W_enc, W_dec = np.eye(2), np.eye(2)
    x_hat, f = sae_forward(x, W_enc, np.zeros(2), W_dec, b_dec=np.array([3.0, 3.0]))
    assert np.allclose(f, 0.0) and np.allclose(x_hat, [[3.0, 3.0]])


def test_4_perfect_reconstruction_leaves_only_the_sparsity_term():
    x = np.array([[1.0, 0.0], [0.0, 2.0]])
    f = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 1.0]])
    assert np.isclose(sae_loss(x, x.copy(), f, 0.5), 0.5 * (1.0 + 3.0) / 2)


def test_5_loss_hand_computed():
    x = np.array([[1.0, 1.0]])
    x_hat = np.array([[0.0, 3.0]])
    f = np.array([[2.0, 0.0, 1.0]])
    assert np.isclose(sae_loss(x, x_hat, f, 0.1), (1 + 4) + 0.1 * 3.0)


def test_6_sparsity_coefficient_scales_the_penalty_only():
    x = np.ones((2, 2))
    f = np.array([[1.0, 1.0], [2.0, 0.0]])
    a, b = sae_loss(x, x, f, 0.0), sae_loss(x, x, f, 2.0)
    assert np.isclose(a, 0.0) and np.isclose(b, 2.0 * 2.0)


def test_7_inputs_not_modified():
    rng = np.random.RandomState(1)
    x = rng.randn(3, 4)
    W_enc, W_dec = rng.randn(4, 8), rng.randn(8, 4)
    snaps = [x.copy(), W_enc.copy(), W_dec.copy()]
    x_hat, f = sae_forward(x, W_enc, np.zeros(8), W_dec, np.zeros(4))
    sae_loss(x, x_hat, f, 0.1)
    assert np.array_equal(x, snaps[0]) and np.array_equal(W_enc, snaps[1]) and np.array_equal(W_dec, snaps[2])
