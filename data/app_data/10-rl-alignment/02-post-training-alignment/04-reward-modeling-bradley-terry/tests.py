"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/04-reward-modeling-bradley-terry/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
pooled_last_token_representation = _module.pooled_last_token_representation
reward_model_score = _module.reward_model_score
reward_model_loss = _module.reward_model_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_pooled_representation_is_the_last_real_token():
    hidden_states = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [99.0, 99.0]])
    pooled = pooled_last_token_representation(hidden_states, seq_len=3)
    assert np.allclose(pooled, [3.0, 3.0])


def test_02_reward_model_loss_favors_correctly_ranked_pairs():
    correct_ranking_loss = reward_model_loss(chosen_reward=5.0, rejected_reward=-5.0)
    wrong_ranking_loss = reward_model_loss(chosen_reward=-5.0, rejected_reward=5.0)
    assert correct_ranking_loss < wrong_ranking_loss


# --- General-case coverage --------------------------------------------


def test_03_reward_model_score_matches_hand_computed_linear():
    pooled = np.array([1.0, 2.0, 3.0])
    weight = np.array([[0.5, 0.5, 0.5]])
    bias = np.array([1.0])
    assert math.isclose(reward_model_score(pooled, weight, bias), 4.0)


def test_04_equal_rewards_give_loss_of_negative_log_half():
    loss = reward_model_loss(chosen_reward=2.0, rejected_reward=2.0)
    assert math.isclose(loss, -math.log(0.5), abs_tol=1e-9)


def test_05_loss_decreases_as_the_reward_gap_grows_in_the_right_direction():
    small_gap = reward_model_loss(chosen_reward=1.0, rejected_reward=0.5)
    large_gap = reward_model_loss(chosen_reward=5.0, rejected_reward=-5.0)
    assert large_gap < small_gap


# --- Parameter handling -------------------------------------------------


def test_06_pooled_representation_ignores_padding_after_seq_len():
    hidden_states = np.zeros((10, 3))
    hidden_states[4] = [7.0, 8.0, 9.0]
    hidden_states[5:] = 999.0  # padding
    pooled = pooled_last_token_representation(hidden_states, seq_len=5)
    assert np.allclose(pooled, [7.0, 8.0, 9.0])


def test_07_reward_score_shape_is_scalar():
    pooled = np.array([1.0, 2.0])
    weight = np.array([[1.0, 1.0]])
    bias = np.array([0.0])
    score = reward_model_score(pooled, weight, bias)
    assert isinstance(score, float)


# --- Edge cases ---------------------------------------------------------


def test_08_single_token_sequence():
    hidden_states = np.array([[5.0, 6.0]])
    pooled = pooled_last_token_representation(hidden_states, seq_len=1)
    assert np.allclose(pooled, [5.0, 6.0])


def test_09_zero_bias_and_weight_gives_zero_score():
    pooled = np.array([1.0, 2.0, 3.0])
    weight = np.zeros((1, 3))
    bias = np.zeros(1)
    assert math.isclose(reward_model_score(pooled, weight, bias), 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_loss_matches_the_bradley_terry_formula_directly():
    # Directly targets a mutant that swaps the sign or the argument
    # order (e.g. sigmoid(rejected - chosen), which would silently
    # reward the model for getting rankings BACKWARDS): cross-check
    # against the formula computed independently, term by term.
    chosen, rejected = 3.0, 1.0
    expected = -math.log(1.0 / (1.0 + math.exp(-(chosen - rejected))))
    assert math.isclose(reward_model_loss(chosen, rejected), expected, rel_tol=1e-9)
