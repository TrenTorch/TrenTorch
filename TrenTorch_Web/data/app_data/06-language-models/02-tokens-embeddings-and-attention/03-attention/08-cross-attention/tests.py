"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
cross_attention = _module.cross_attention


def _setup(seed=0, Tq=3, Tk=5, d=4, dh=3):
    rng = np.random.RandomState(seed)
    return rng.randn(Tq, d), rng.randn(Tk, d), rng.randn(d, dh), rng.randn(d, dh), rng.randn(d, dh)


def test_1_shapes_follow_the_decoder_length():
    x, e, Wq, Wk, Wv = _setup()
    out, w = cross_attention(x, e, Wq, Wk, Wv, np.ones(5))
    assert out.shape == (3, 3) and w.shape == (3, 5)


def test_2_rows_sum_to_one():
    x, e, Wq, Wk, Wv = _setup(1)
    _, w = cross_attention(x, e, Wq, Wk, Wv, np.ones(5))
    assert np.allclose(w.sum(axis=1), 1.0)


def test_3_padded_encoder_positions_get_zero_weight():
    x, e, Wq, Wk, Wv = _setup(2)
    mask = np.array([1, 1, 1, 0, 0])
    _, w = cross_attention(x, e, Wq, Wk, Wv, mask)
    assert np.all(w[:, 3:] == 0.0) and np.allclose(w.sum(axis=1), 1.0)


def test_4_padding_contents_do_not_change_the_output():
    x, e, Wq, Wk, Wv = _setup(3)
    mask = np.array([1, 1, 1, 0, 0])
    a, _ = cross_attention(x, e, Wq, Wk, Wv, mask)
    e2 = e.copy()
    e2[3:] = 1e3
    b, _ = cross_attention(x, e2, Wq, Wk, Wv, mask)
    assert np.allclose(a, b)


def test_5_equal_keys_give_uniform_weights_over_real_positions():
    x, _, Wq, Wk, Wv = _setup(4)
    e = np.tile(np.random.RandomState(0).randn(1, 4), (5, 1))
    _, w = cross_attention(x, e, Wq, Wk, Wv, np.array([1, 1, 1, 1, 0]))
    assert np.allclose(w[:, :4], 0.25)


def test_6_single_real_position_copies_its_value():
    x, e, Wq, Wk, Wv = _setup(5)
    out, _ = cross_attention(x, e, Wq, Wk, Wv, np.array([0, 0, 1, 0, 0]))
    assert np.allclose(out, np.tile(e[2] @ Wv, (3, 1)))


def test_7_matches_loop_oracle_and_inputs_untouched():
    x, e, Wq, Wk, Wv = _setup(6)
    snap = e.copy()
    mask = np.array([1, 0, 1, 1, 0])
    out, _ = cross_attention(x, e, Wq, Wk, Wv, mask)
    for i in range(3):
        s = np.array([(x[i] @ Wq) @ (e[j] @ Wk) / np.sqrt(3) for j in range(5)])
        s[mask == 0] = -np.inf
        p = np.exp(s - s.max())
        p /= p.sum()
        assert np.allclose(out[i], sum(p[j] * (e[j] @ Wv) for j in range(5)))
    assert np.array_equal(e, snap)
