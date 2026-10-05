"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
logit_lens = _module.logit_lens
target_rank_by_layer = _module.target_rank_by_layer


def test_1_hand_computed_single_layer():
    resid = np.array([[3.0, 4.0]])  # rms = sqrt((9+16)/2)
    W_U = np.eye(2)
    out = logit_lens(resid, W_U, np.ones(2), eps=0.0)
    rms = np.sqrt(12.5)
    assert np.allclose(out, [[3 / rms, 4 / rms]])


def test_2_gain_scales_the_features():
    resid = np.array([[1.0, 1.0]])
    out = logit_lens(resid, np.eye(2), np.array([2.0, 0.5]), eps=0.0)
    assert np.allclose(out, [[2.0, 0.5]])


def test_3_scale_of_the_stream_does_not_matter():
    rng = np.random.RandomState(0)
    resid = rng.randn(4, 6)
    W_U = rng.randn(6, 9)
    g = rng.rand(6) + 0.5
    assert np.allclose(logit_lens(resid, W_U, g, 1e-12), logit_lens(resid * 17.0, W_U, g, 1e-12), atol=1e-6)


def test_4_shapes():
    out = logit_lens(np.ones((5, 4)), np.ones((4, 7)), np.ones(4))
    assert out.shape == (5, 7)


def test_5_rank_hand_computed():
    logits = np.array([[0.1, 0.9, 0.5], [0.9, 0.1, 0.5], [0.1, 0.5, 0.9]])
    assert target_rank_by_layer(logits, 0).tolist() == [2, 0, 2]
    assert target_rank_by_layer(logits, 2).tolist() == [1, 1, 0]


def test_6_rank_ignores_logit_scale():
    logits = np.random.RandomState(1).randn(3, 8)
    assert np.array_equal(target_rank_by_layer(logits, 4), target_rank_by_layer(logits * 100, 4))


def test_7_inputs_untouched_and_matches_loop_oracle():
    rng = np.random.RandomState(2)
    resid, W_U, g = rng.randn(3, 5), rng.randn(5, 6), rng.rand(5)
    snaps = [resid.copy(), W_U.copy()]
    out = logit_lens(resid, W_U, g)
    for l in range(3):
        x = resid[l]
        expected = (x / np.sqrt((x ** 2).mean() + 1e-6) * g) @ W_U
        assert np.allclose(out[l], expected)
    assert np.array_equal(resid, snaps[0]) and np.array_equal(W_U, snaps[1])
