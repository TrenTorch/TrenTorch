"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
response_mask = _module.response_mask
sft_loss = _module.sft_loss


def test_1_mask_hand_computed():
    m = response_mask(np.array([2, 1]), np.array([4, 3]), 5)
    assert m.tolist() == [[False, False, True, True, False], [False, True, True, False, False]]


def test_2_mask_excludes_prompt_and_padding():
    m = response_mask(np.array([3]), np.array([6]), 8)
    assert m[0, :3].sum() == 0 and m[0, 6:].sum() == 0 and m[0, 3:6].all()


def test_3_uniform_logits_give_log_v():
    B, T, V = 2, 6, 5
    ids = np.random.RandomState(0).randint(0, V, size=(B, T))
    loss = sft_loss(np.zeros((B, T, V)), ids, np.array([2, 3]), np.array([5, 6]))
    assert np.isclose(loss, np.log(V))


def test_4_prompt_tokens_do_not_change_the_loss():
    rng = np.random.RandomState(1)
    B, T, V = 2, 6, 4
    logits = rng.randn(B, T, V)
    ids = rng.randint(0, V, size=(B, T))
    pl, sl = np.array([3, 2]), np.array([6, 5])
    base = sft_loss(logits, ids, pl, sl)
    changed = ids.copy()
    changed[0, :3] = (changed[0, :3] + 1) % V
    assert np.isclose(sft_loss(logits, changed, pl, sl), base)


def test_5_padding_logits_do_not_change_the_loss():
    rng = np.random.RandomState(2)
    B, T, V = 2, 6, 4
    logits = rng.randn(B, T, V)
    ids = rng.randint(0, V, size=(B, T))
    pl, sl = np.array([2, 2]), np.array([4, 6])
    base = sft_loss(logits, ids, pl, sl)
    other = logits.copy()
    other[0, 4:] = rng.randn(2, V) * 50
    assert np.isclose(sft_loss(other, ids, pl, sl), base)


def test_6_matches_explicit_loop_oracle_and_shift():
    rng = np.random.RandomState(3)
    B, T, V = 3, 7, 5
    logits = rng.randn(B, T, V)
    ids = rng.randint(0, V, size=(B, T))
    pl, sl = np.array([2, 3, 1]), np.array([7, 5, 4])
    total, n = 0.0, 0
    for b in range(B):
        for t in range(pl[b], sl[b]):
            z = logits[b, t - 1]
            lp = z - np.log(np.exp(z).sum())
            total -= lp[ids[b, t]]
            n += 1
    assert np.isclose(sft_loss(logits, ids, pl, sl), total / n)


def test_7_stable_for_huge_logits():
    logits = np.zeros((1, 4, 3))
    logits[0, :, 0] = 1e4
    ids = np.array([[0, 0, 0, 0]])
    assert np.isclose(sft_loss(logits, ids, np.array([1]), np.array([4])), 0.0, atol=1e-8)
