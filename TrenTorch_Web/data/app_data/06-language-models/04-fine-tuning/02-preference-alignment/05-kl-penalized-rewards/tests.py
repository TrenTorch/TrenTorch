"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
kl_penalized_rewards = _module.kl_penalized_rewards
mean_kl = _module.mean_kl


def test_1_hand_computed_rewards():
    lp = np.array([[-1.0, -2.0, -3.0]])
    lr = np.array([[-1.5, -2.0, -2.0]])
    out = kl_penalized_rewards(lp, lr, np.array([10.0]), np.array([3]), beta=0.5)
    # penalties: -0.5*0.5, 0, -0.5*(-1) ; reward on the last token
    assert np.allclose(out, [[-0.25, 0.0, 0.5 + 10.0]])


def test_2_padding_is_exactly_zero_and_reward_lands_on_last_valid_token():
    lp = np.array([[-1.0, -1.0, -9.0, -9.0], [-1.0, -1.0, -1.0, -1.0]])
    lr = np.zeros((2, 4))
    out = kl_penalized_rewards(lp, lr, np.array([5.0, 7.0]), np.array([2, 4]), beta=1.0)
    assert np.all(out[0, 2:] == 0.0)
    assert np.isclose(out[0, 1], 1.0 + 5.0) and np.isclose(out[1, 3], 1.0 + 7.0)


def test_3_identical_models_give_only_the_final_reward():
    lp = np.random.RandomState(0).randn(3, 5)
    out = kl_penalized_rewards(lp, lp, np.array([1.0, 2.0, 3.0]), np.array([5, 3, 1]), beta=0.3)
    expected = np.zeros((3, 5))
    expected[0, 4], expected[1, 2], expected[2, 0] = 1.0, 2.0, 3.0
    assert np.allclose(out, expected)


def test_4_mean_kl_hand_computed_with_padding_ignored():
    lp = np.array([[-1.0, -2.0, 99.0]])
    lr = np.array([[-2.0, -3.0, -99.0]])
    assert np.isclose(mean_kl(lp, lr, np.array([2])), 1.0)


def test_5_mean_kl_is_zero_for_identical_models_and_positive_under_sampling():
    rng = np.random.RandomState(0)
    p = np.array([0.7, 0.2, 0.1])
    q_ = np.array([0.4, 0.4, 0.2])
    draws = rng.choice(3, size=20000, p=p)
    lp, lr = np.log(p[draws])[None, :], np.log(q_[draws])[None, :]
    est = mean_kl(lp, lr, np.array([20000]))
    true = float((p * np.log(p / q_)).sum())
    assert abs(est - true) < 0.02
    assert np.isclose(mean_kl(lp, lp, np.array([20000])), 0.0)


def test_6_larger_beta_scales_the_penalty_linearly():
    lp = np.array([[-1.0, -1.0]])
    lr = np.array([[-2.0, -3.0]])
    a = kl_penalized_rewards(lp, lr, np.array([0.0]), np.array([2]), 0.1)
    b = kl_penalized_rewards(lp, lr, np.array([0.0]), np.array([2]), 0.2)
    assert np.allclose(b, 2 * a)


def test_7_inputs_not_modified():
    lp, lr = np.random.RandomState(1).randn(2, 3), np.random.RandomState(2).randn(2, 3)
    s1, s2 = lp.copy(), lr.copy()
    fr = np.array([1.0, 2.0])
    kl_penalized_rewards(lp, lr, fr, np.array([3, 2]), 0.1)
    mean_kl(lp, lr, np.array([3, 2]))
    assert np.array_equal(lp, s1) and np.array_equal(lr, s2) and np.array_equal(fr, [1.0, 2.0])
