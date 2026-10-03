"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
dpo_implicit_reward = _module.dpo_implicit_reward
dpo_loss = _module.dpo_loss


def test_1_policy_equal_to_reference_gives_ln2():
    x = np.array([-10.0, -20.0])
    y = np.array([-12.0, -15.0])
    assert np.isclose(dpo_loss(x, y, x, y, beta=0.1), np.log(2))


def test_2_implicit_reward_hand_computed():
    assert np.allclose(dpo_implicit_reward(np.array([-8.0, -5.0]), np.array([-10.0, -6.0]), 0.5), [1.0, 0.5])


def test_3_hand_computed_loss():
    # chosen reward = 0.1 * (-9 - -10) = 0.1, rejected = 0.1 * (-12 - -11) = -0.1
    loss = dpo_loss(np.array([-9.0]), np.array([-12.0]), np.array([-10.0]), np.array([-11.0]), 0.1)
    assert np.isclose(loss, np.log(1 + np.exp(-0.2)))


def test_4_raising_chosen_lowers_the_loss():
    ref_c, ref_r = np.array([-10.0]), np.array([-10.0])
    base = dpo_loss(np.array([-10.0]), np.array([-10.0]), ref_c, ref_r, 0.2)
    better = dpo_loss(np.array([-8.0]), np.array([-10.0]), ref_c, ref_r, 0.2)
    worse = dpo_loss(np.array([-12.0]), np.array([-10.0]), ref_c, ref_r, 0.2)
    assert better < base < worse


def test_5_shared_shift_of_policy_and_reference_is_irrelevant():
    rng = np.random.RandomState(0)
    pc, pr, rc, rr = (rng.randn(6) for _ in range(4))
    base = dpo_loss(pc, pr, rc, rr, 0.3)
    assert np.isclose(base, dpo_loss(pc + 5, pr + 5, rc + 5, rr + 5, 0.3))
    assert np.isclose(base, dpo_loss(pc, pr, rc + 3, rr + 3, 0.3))


def test_6_larger_beta_sharpens_a_correct_preference():
    pc, pr = np.array([-8.0]), np.array([-12.0])
    ref = np.array([-10.0])
    assert dpo_loss(pc, pr, ref, ref, 1.0) < dpo_loss(pc, pr, ref, ref, 0.1)


def test_7_matches_naive_and_stable_for_large_margins():
    rng = np.random.RandomState(1)
    pc, pr, rc, rr = (rng.randn(10) for _ in range(4))
    d = 0.4 * ((pc - rc) - (pr - rr))
    assert np.isclose(dpo_loss(pc, pr, rc, rr, 0.4), np.mean(-np.log(1 / (1 + np.exp(-d)))))
    assert np.isfinite(dpo_loss(np.array([5000.0]), np.array([-5000.0]), np.array([0.0]), np.array([0.0]), 1.0))
