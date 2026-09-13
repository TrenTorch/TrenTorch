"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/12-reward-hacking-goodharts-law/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
select_best_by_proxy = _module.select_best_by_proxy
true_reward_of_selection = _module.true_reward_of_selection
reward_hacking_gap = _module.reward_hacking_gap


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_proxy_and_true_reward_agree_gives_zero_gap():
    true_rewards = [1.0, 5.0, 2.0]
    proxy_rewards = [1.0, 5.0, 2.0]  # identical to the true reward
    assert math.isclose(reward_hacking_gap(true_rewards, proxy_rewards), 0.0)


def test_02_a_misaligned_proxy_produces_a_positive_gap():
    # A rigged example of Goodhart's law: the proxy (e.g. response
    # length) rewards the WORST true-quality candidate the most.
    true_rewards = [9.0, 5.0, 1.0]  # candidate 0 is truly the best
    proxy_rewards = [1.0, 5.0, 9.0]  # but the proxy prefers candidate 2
    gap = reward_hacking_gap(true_rewards, proxy_rewards)
    assert gap > 0.0
    assert math.isclose(gap, 9.0 - 1.0)


# --- General-case coverage --------------------------------------------


def test_03_select_best_by_proxy_ignores_true_reward_entirely():
    candidates = ["a", "b", "c"]
    proxy_rewards = [0.1, 0.9, 0.5]
    assert select_best_by_proxy(candidates, proxy_rewards) == 1


def test_04_true_reward_of_selection_looks_up_the_right_index():
    true_rewards = [3.0, 7.0, 1.0]
    assert math.isclose(true_reward_of_selection(true_rewards, 1), 7.0)


def test_05_gap_grows_as_proxy_misalignment_worsens():
    true_rewards = [10.0, 5.0, 0.0]
    mild_proxy = [10.0, 6.0, 5.0]  # still picks the true best
    severe_proxy = [0.0, 5.0, 10.0]  # picks the true worst
    mild_gap = reward_hacking_gap(true_rewards, mild_proxy)
    severe_gap = reward_hacking_gap(true_rewards, severe_proxy)
    assert severe_gap > mild_gap


# --- Parameter handling -------------------------------------------------


def test_06_gap_is_never_negative():
    import numpy as np

    rng = np.random.default_rng(0)
    for _ in range(20):
        true_rewards = rng.normal(size=5).tolist()
        proxy_rewards = rng.normal(size=5).tolist()
        assert reward_hacking_gap(true_rewards, proxy_rewards) >= -1e-9


def test_07_selecting_via_the_true_reward_itself_gives_zero_gap():
    true_rewards = [2.0, 8.0, 4.0, 1.0]
    assert math.isclose(reward_hacking_gap(true_rewards, true_rewards), 0.0)


# --- Edge cases ---------------------------------------------------------


def test_08_single_candidate_always_has_zero_gap():
    assert math.isclose(reward_hacking_gap([5.0], [0.0]), 0.0)


def test_09_ties_in_true_reward_still_give_a_well_defined_gap():
    true_rewards = [5.0, 5.0, 1.0]
    proxy_rewards = [0.0, 0.0, 9.0]  # proxy picks the true-worst candidate
    gap = reward_hacking_gap(true_rewards, proxy_rewards)
    assert math.isclose(gap, 4.0)


# --- Independent correctness oracle -----------------------------------


def test_10_gap_matches_the_direct_difference_of_true_rewards():
    # Directly targets a mutant that computes the gap using PROXY
    # reward values instead of TRUE reward values in the subtraction
    # (which would misreport how much real quality was actually lost).
    true_rewards = [3.0, 9.0, 6.0]
    proxy_rewards = [9.0, 1.0, 2.0]  # proxy picks index 0 (true reward 3.0)
    expected = max(true_rewards) - true_rewards[0]
    assert math.isclose(reward_hacking_gap(true_rewards, proxy_rewards), expected)
