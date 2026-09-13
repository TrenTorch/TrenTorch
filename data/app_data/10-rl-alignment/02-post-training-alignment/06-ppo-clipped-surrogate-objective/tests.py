"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/06-ppo-clipped-surrogate-objective/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
probability_ratio = _module.probability_ratio
ppo_clipped_surrogate_loss = _module.ppo_clipped_surrogate_loss
fraction_of_ratios_clipped = _module.fraction_of_ratios_clipped


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_probability_ratio_of_one_when_policy_unchanged():
    log_probs = np.array([-1.5, -0.3, -2.0])
    ratio = probability_ratio(log_probs, log_probs)
    assert np.allclose(ratio, 1.0)


def test_02_positive_advantage_large_ratio_gets_clipped():
    # ratio=1.5, advantage=1: unclipped=1.5, clipped=1.2 -> loss=-1.2
    loss = ppo_clipped_surrogate_loss(np.array([1.5]), np.array([1.0]), epsilon=0.2)
    assert math.isclose(loss[0], -1.2)


# --- General-case coverage --------------------------------------------


def test_03_negative_advantage_large_ratio_is_not_clipped_favorably():
    # ratio=1.5, advantage=-1: unclipped=-1.5, clipped=-1.2,
    # min(-1.5,-1.2)=-1.5 -> loss=+1.5 (clipping does NOT protect
    # against moving too far in the WRONG direction).
    loss = ppo_clipped_surrogate_loss(np.array([1.5]), np.array([-1.0]), epsilon=0.2)
    assert math.isclose(loss[0], 1.5)


def test_04_ratio_within_trust_region_is_unaffected_by_clipping():
    ratio = np.array([1.05])
    advantage = np.array([2.0])
    loss = ppo_clipped_surrogate_loss(ratio, advantage, epsilon=0.2)
    assert math.isclose(loss[0], -(1.05 * 2.0))


def test_05_matches_hand_computation_for_a_batch():
    ratio = np.array([1.0, 1.5, 0.5])
    advantage = np.array([1.0, 1.0, 1.0])
    loss = ppo_clipped_surrogate_loss(ratio, advantage, epsilon=0.2)
    assert np.allclose(loss, [-1.0, -1.2, -0.5])


# --- Parameter handling -------------------------------------------------


def test_06_fraction_clipped_counts_ratios_outside_the_trust_region():
    ratio = np.array([1.0, 1.5, 0.5, 1.1, 0.7])
    assert math.isclose(fraction_of_ratios_clipped(ratio, epsilon=0.2), 0.6)  # 1.5, 0.5, 0.7 are out


def test_07_smaller_epsilon_clips_more_often():
    ratio = np.array([1.1, 1.15, 1.25])
    loose = fraction_of_ratios_clipped(ratio, epsilon=0.2)
    tight = fraction_of_ratios_clipped(ratio, epsilon=0.05)
    assert tight >= loose


# --- Edge cases ---------------------------------------------------------


def test_08_ratio_exactly_at_the_clip_boundary():
    ratio = np.array([1.2])
    advantage = np.array([3.0])
    loss = ppo_clipped_surrogate_loss(ratio, advantage, epsilon=0.2)
    assert math.isclose(loss[0], -(1.2 * 3.0))


def test_09_zero_advantage_gives_zero_loss_regardless_of_ratio():
    ratio = np.array([0.1, 1.0, 5.0])
    loss = ppo_clipped_surrogate_loss(ratio, np.zeros(3), epsilon=0.2)
    assert np.allclose(loss, 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_clipping_only_ever_makes_the_objective_more_conservative():
    # Directly targets a mutant that clips the WRONG way (e.g. using
    # max instead of min, which would let the policy move MORE
    # aggressively than the unclipped objective, defeating PPO's
    # entire purpose): the clipped loss must never be LESS than the
    # plain unclipped policy-gradient loss.
    rng = np.random.default_rng(0)
    ratio = rng.uniform(0.1, 3.0, size=50)
    advantage = rng.normal(size=50)
    clipped_loss = ppo_clipped_surrogate_loss(ratio, advantage, epsilon=0.2)
    unclipped_loss = -(ratio * advantage)
    assert np.all(clipped_loss >= unclipped_loss - 1e-9)
