"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
group_advantages = _module.group_advantages
clipped_surrogate_loss = _module.clipped_surrogate_loss


def test_1_hand_computed_group():
    adv = group_advantages(np.array([[1.0, 0.0, 0.0, 1.0]]))
    assert np.allclose(adv, [[1, -1, -1, 1]], atol=1e-5)


def test_2_each_row_has_zero_mean_and_unit_spread():
    rng = np.random.RandomState(0)
    adv = group_advantages(rng.randn(5, 8))
    assert np.allclose(adv.mean(axis=1), 0.0, atol=1e-9)
    assert np.allclose(adv.std(axis=1), 1.0, atol=1e-4)


def test_3_uniform_group_has_zero_advantage():
    adv = group_advantages(np.array([[2.0, 2.0, 2.0], [0.0, 1.0, 2.0]]))
    assert np.all(adv[0] == 0.0) and np.any(adv[1] != 0.0)


def test_4_groups_are_normalized_independently():
    a = group_advantages(np.array([[0.0, 1.0], [100.0, 300.0]]))
    assert np.allclose(a[0], a[1], atol=1e-4)


def test_5_clip_is_inactive_inside_the_trust_region():
    ratio = np.array([1.05, 0.95])
    adv = np.array([2.0, -1.0])
    assert np.isclose(clipped_surrogate_loss(ratio, adv, 0.2), -np.mean(ratio * adv))


def test_6_clip_blocks_credit_beyond_the_region_for_positive_advantage():
    assert np.isclose(clipped_surrogate_loss(np.array([1.5]), np.array([2.0]), 0.2), -1.2 * 2.0)
    # for negative advantage a large ratio is NOT clipped (still penalized)
    assert np.isclose(clipped_surrogate_loss(np.array([1.5]), np.array([-2.0]), 0.2), 1.5 * 2.0)


def test_7_moving_toward_good_responses_lowers_the_loss_and_input_untouched():
    rewards = np.array([[1.0, 2.0, 3.0]])
    snap = rewards.copy()
    adv = group_advantages(rewards)
    base = clipped_surrogate_loss(np.ones(3), adv, 0.2)
    toward = clipped_surrogate_loss(1.0 + 0.1 * np.sign(adv), adv, 0.2)
    away = clipped_surrogate_loss(1.0 - 0.1 * np.sign(adv), adv, 0.2)
    assert np.isclose(base, 0.0, atol=1e-9)
    assert toward < base < away
    assert np.array_equal(rewards, snap)
