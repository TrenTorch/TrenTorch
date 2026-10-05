"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
additive_attention = _module.additive_attention


def _params(seed=0, dq=3, dk=4, h=5, T=6):
    rng = np.random.RandomState(seed)
    return rng.randn(dq), rng.randn(T, dk), rng.randn(dq, h), rng.randn(dk, h), rng.randn(h)


def test_1_weights_form_a_distribution_and_shapes():
    q_, K, Wq, Wk, v = _params()
    ctx, w = additive_attention(q_, K, Wq, Wk, v)
    assert ctx.shape == (4,) and w.shape == (6,)
    assert np.isclose(w.sum(), 1.0) and (w > 0).all()


def test_2_zero_v_gives_uniform_attention_and_mean_context():
    q_, K, Wq, Wk, _ = _params(1)
    ctx, w = additive_attention(q_, K, Wq, Wk, np.zeros(5))
    assert np.allclose(w, 1 / 6) and np.allclose(ctx, K.mean(axis=0))


def test_3_hand_computed_two_keys():
    K = np.array([[1.0], [3.0]])
    ctx, w = additive_attention(np.array([0.0]), K, np.zeros((1, 1)), np.eye(1), np.array([1.0]))
    s = np.tanh(np.array([1.0, 3.0]))
    expected = np.exp(s) / np.exp(s).sum()
    assert np.allclose(w, expected) and np.isclose(ctx[0], expected @ [1.0, 3.0])


def test_4_context_lies_in_the_convex_hull_of_keys():
    q_, K, Wq, Wk, v = _params(2)
    ctx, _ = additive_attention(q_, K, Wq, Wk, v)
    assert (ctx <= K.max(axis=0) + 1e-9).all() and (ctx >= K.min(axis=0) - 1e-9).all()


def test_5_stable_for_huge_scores():
    q_, K, Wq, Wk, v = _params(3)
    ctx, w = additive_attention(q_, K, Wq, Wk, v * 1e6)
    assert np.all(np.isfinite(ctx)) and np.isclose(w.sum(), 1.0)


def test_6_permuting_keys_permutes_weights_and_keeps_context():
    q_, K, Wq, Wk, v = _params(4)
    perm = np.random.RandomState(0).permutation(6)
    ctx, w = additive_attention(q_, K, Wq, Wk, v)
    ctx2, w2 = additive_attention(q_, K[perm], Wq, Wk, v)
    assert np.allclose(ctx, ctx2) and np.allclose(w[perm], w2)


def test_7_matches_loop_oracle_and_inputs_untouched():
    q_, K, Wq, Wk, v = _params(5)
    snap = K.copy()
    ctx, w = additive_attention(q_, K, Wq, Wk, v)
    e = np.array([v @ np.tanh(q_ @ Wq + K[t] @ Wk) for t in range(6)])
    ref = np.exp(e - e.max())
    ref /= ref.sum()
    assert np.allclose(w, ref) and np.allclose(ctx, (ref[:, None] * K).sum(axis=0))
    assert np.array_equal(K, snap)
