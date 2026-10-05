"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
skipgram_pairs = _module.skipgram_pairs
sgns_loss = _module.sgns_loss


def test_1_pairs_hand_computed():
    assert skipgram_pairs([10, 20, 30], 1) == [(10, 20), (20, 10), (20, 30), (30, 20)]


def test_2_window_two_and_edges():
    pairs = skipgram_pairs([1, 2, 3, 4], 2)
    assert (1, 3) in pairs and (1, 4) not in pairs and len(pairs) == 10


def test_3_empty_and_single_token():
    assert skipgram_pairs([], 2) == [] and skipgram_pairs([5], 2) == []


def test_4_zero_vectors_give_one_plus_k_times_ln2():
    W = np.zeros((6, 3))
    loss = sgns_loss(W, W, np.array([0, 1]), np.array([2, 3]), np.array([[4, 5, 4], [1, 2, 3]]))
    assert np.isclose(loss, 4 * np.log(2))


def test_5_hand_computed_single_example():
    W_in = np.array([[1.0, 0.0], [0.0, 0.0]])
    W_out = np.array([[0.0, 0.0], [2.0, 0.0]])
    # center 0 (v=[1,0]); context 1: u.v = 2 ; one negative 0: u.v = 0
    loss = sgns_loss(W_in, W_out, np.array([0]), np.array([1]), np.array([[0]]))
    assert np.isclose(loss, np.log(1 + np.exp(-2.0)) + np.log(2))


def test_6_aligned_context_lowers_the_loss():
    rng = np.random.RandomState(0)
    W_in, W_out = rng.randn(5, 4), rng.randn(5, 4)
    c, o, neg = np.array([0]), np.array([1]), np.array([[2, 3]])
    base = sgns_loss(W_in, W_out, c, o, neg)
    W_out2 = W_out.copy()
    W_out2[1] = W_in[0] * 3
    assert sgns_loss(W_in, W_out2, c, o, neg) < base


def test_7_matches_loop_oracle_and_inputs_untouched():
    rng = np.random.RandomState(1)
    W_in, W_out = rng.randn(8, 3), rng.randn(8, 3)
    snap = W_in.copy()
    c, o, neg = rng.randint(0, 8, 5), rng.randint(0, 8, 5), rng.randint(0, 8, (5, 4))
    sig = lambda x: 1 / (1 + np.exp(-x))
    ref = np.mean([-np.log(sig(W_out[o[b]] @ W_in[c[b]])) - sum(np.log(sig(-W_out[k] @ W_in[c[b]])) for k in neg[b]) for b in range(5)])
    assert np.isclose(sgns_loss(W_in, W_out, c, o, neg), ref) and np.array_equal(W_in, snap)
