"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/09-rejection-sampling-finetuning/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
filter_top_k_by_reward = _module.filter_top_k_by_reward
build_rejection_sampling_sft_dataset = _module.build_rejection_sampling_sft_dataset


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_keeps_only_the_top_k_responses():
    responses = ["a", "b", "c", "d"]
    rewards = [1.0, 4.0, 2.0, 3.0]
    kept = filter_top_k_by_reward(responses, rewards, k=2)
    assert kept == ["b", "d"]


def test_02_builds_a_flat_prompt_response_dataset():
    prompts = ["p1", "p2"]
    response_groups = [["a", "b", "c"], ["x", "y"]]
    reward_groups = [[1.0, 3.0, 2.0], [5.0, 1.0]]
    dataset = build_rejection_sampling_sft_dataset(prompts, response_groups, reward_groups, k=1)
    assert dataset == [("p1", "b"), ("p2", "x")]


# --- General-case coverage --------------------------------------------


def test_03_top_k_preserves_best_to_worst_order():
    responses = ["a", "b", "c", "d", "e"]
    rewards = [5.0, 1.0, 4.0, 3.0, 2.0]
    kept = filter_top_k_by_reward(responses, rewards, k=3)
    assert kept == ["a", "c", "d"]


def test_04_k_equal_to_group_size_keeps_everything():
    responses = ["a", "b", "c"]
    rewards = [1.0, 2.0, 3.0]
    kept = filter_top_k_by_reward(responses, rewards, k=3)
    assert set(kept) == {"a", "b", "c"}


def test_05_dataset_size_matches_k_times_number_of_prompts():
    prompts = ["p1", "p2", "p3"]
    response_groups = [["a", "b", "c"]] * 3
    reward_groups = [[1.0, 2.0, 3.0]] * 3
    dataset = build_rejection_sampling_sft_dataset(prompts, response_groups, reward_groups, k=2)
    assert len(dataset) == 6


# --- Parameter handling -------------------------------------------------


def test_06_k_one_keeps_only_the_single_best():
    responses = ["low", "high", "mid"]
    rewards = [1.0, 9.0, 5.0]
    assert filter_top_k_by_reward(responses, rewards, k=1) == ["high"]


def test_07_every_kept_response_is_paired_with_its_own_prompt():
    prompts = ["question-A", "question-B"]
    response_groups = [["a1", "a2"], ["b1", "b2"]]
    reward_groups = [[1.0, 2.0], [9.0, 8.0]]
    dataset = build_rejection_sampling_sft_dataset(prompts, response_groups, reward_groups, k=1)
    assert ("question-A", "a2") in dataset
    assert ("question-B", "b1") in dataset


# --- Edge cases ---------------------------------------------------------


def test_08_k_zero_keeps_nothing():
    kept = filter_top_k_by_reward(["a", "b"], [1.0, 2.0], k=0)
    assert kept == []


def test_09_single_response_group():
    kept = filter_top_k_by_reward(["only"], [3.0], k=1)
    assert kept == ["only"]


# --- Independent correctness oracle -----------------------------------


def test_10_ties_do_not_crash_and_still_respect_k():
    # Directly targets a mutant that assumes rewards are always
    # distinct and breaks (or duplicates entries) on ties.
    responses = ["a", "b", "c", "d"]
    rewards = [2.0, 2.0, 2.0, 5.0]
    kept = filter_top_k_by_reward(responses, rewards, k=2)
    assert len(kept) == 2
    assert "d" in kept  # the unambiguous top response must be included
