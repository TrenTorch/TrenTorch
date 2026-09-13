"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/07-dpo-direct-preference-optimization/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
implicit_reward_margin = _module.implicit_reward_margin
dpo_loss = _module.dpo_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_loss_is_lower_when_policy_correctly_prefers_chosen():
    good_loss = dpo_loss(
        policy_chosen_logprob=np.array([-1.0]),
        policy_rejected_logprob=np.array([-5.0]),
        ref_chosen_logprob=np.array([-2.0]),
        ref_rejected_logprob=np.array([-2.0]),
        beta=0.1,
    )
    bad_loss = dpo_loss(
        policy_chosen_logprob=np.array([-5.0]),
        policy_rejected_logprob=np.array([-1.0]),
        ref_chosen_logprob=np.array([-2.0]),
        ref_rejected_logprob=np.array([-2.0]),
        beta=0.1,
    )
    assert good_loss[0] < bad_loss[0]


def test_02_zero_margin_gives_loss_of_negative_log_half():
    margin = implicit_reward_margin(
        np.array([-2.0]), np.array([-2.0]), np.array([-2.0]), np.array([-2.0]), beta=0.1
    )
    assert np.isclose(margin[0], 0.0)
    loss = dpo_loss(np.array([-2.0]), np.array([-2.0]), np.array([-2.0]), np.array([-2.0]), beta=0.1)
    assert math.isclose(loss[0], -math.log(0.5), abs_tol=1e-9)


# --- General-case coverage --------------------------------------------


def test_03_margin_matches_hand_computation():
    margin = implicit_reward_margin(
        policy_chosen_logprob=np.array([-1.0]),
        policy_rejected_logprob=np.array([-3.0]),
        ref_chosen_logprob=np.array([-2.0]),
        ref_rejected_logprob=np.array([-2.0]),
        beta=0.5,
    )
    # beta * [(-1 - -2) - (-3 - -2)] = 0.5 * [1 - (-1)] = 1.0
    assert math.isclose(margin[0], 1.0)


def test_04_higher_beta_amplifies_the_margin():
    args = (np.array([-1.0]), np.array([-3.0]), np.array([-2.0]), np.array([-2.0]))
    small_beta = implicit_reward_margin(*args, beta=0.1)
    large_beta = implicit_reward_margin(*args, beta=1.0)
    assert abs(large_beta[0]) > abs(small_beta[0])


def test_05_loss_decreases_monotonically_with_margin():
    margins_as_losses = [
        dpo_loss(np.array([m]), np.array([0.0]), np.array([0.0]), np.array([0.0]), beta=1.0)[0]
        for m in [-2.0, -1.0, 0.0, 1.0, 2.0]
    ]
    assert all(margins_as_losses[i] > margins_as_losses[i + 1] for i in range(len(margins_as_losses) - 1))


# --- Parameter handling -------------------------------------------------


def test_06_works_on_batches():
    n = 5
    policy_chosen = np.full(n, -1.0)
    policy_rejected = np.full(n, -3.0)
    ref_chosen = np.full(n, -2.0)
    ref_rejected = np.full(n, -2.0)
    loss = dpo_loss(policy_chosen, policy_rejected, ref_chosen, ref_rejected, beta=0.1)
    assert loss.shape == (n,)


def test_07_reference_model_only_matters_relatively():
    # Shifting BOTH ref log-probs by the same constant must not change
    # the margin at all (only relative log-ratios matter).
    args_base = (np.array([-1.0]), np.array([-3.0]))
    m1 = implicit_reward_margin(*args_base, np.array([-2.0]), np.array([-2.0]), beta=0.2)
    m2 = implicit_reward_margin(*args_base, np.array([-2.0 - 5.0]), np.array([-2.0 - 5.0]), beta=0.2)
    assert np.isclose(m1[0], m2[0])


# --- Edge cases ---------------------------------------------------------


def test_08_beta_zero_gives_loss_of_negative_log_half_always():
    loss = dpo_loss(np.array([-1.0]), np.array([-10.0]), np.array([-2.0]), np.array([-2.0]), beta=0.0)
    assert math.isclose(loss[0], -math.log(0.5), abs_tol=1e-9)


def test_09_identical_chosen_and_rejected_logprobs_give_zero_margin():
    margin = implicit_reward_margin(
        np.array([-1.5]), np.array([-1.5]), np.array([-2.0]), np.array([-2.0]), beta=0.3
    )
    assert np.isclose(margin[0], 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_loss_matches_the_published_dpo_formula_directly():
    # Directly targets a mutant that drops the reference-model term
    # entirely (e.g. using only the policy log-probs, which would make
    # this just a plain Bradley-Terry loss on raw log-probabilities,
    # not DPO's actual reference-relative formulation).
    pc, pr, rc, rr, beta = -1.0, -4.0, -1.5, -1.5, 0.3
    expected_margin = beta * ((pc - rc) - (pr - rr))
    expected_loss = -math.log(1.0 / (1.0 + math.exp(-expected_margin)))
    loss = dpo_loss(np.array([pc]), np.array([pr]), np.array([rc]), np.array([rr]), beta=beta)
    assert math.isclose(loss[0], expected_loss, rel_tol=1e-9)
