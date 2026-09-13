"""
pytest data/app_data/10-rl-alignment/01-reinforcement-learning/01-value-iteration-mdp/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/01-reinforcement-learning/{Path(__file__).resolve().parent.name}")
bellman_backup = _module.bellman_backup
value_iteration = _module.value_iteration
policy_evaluation_exact = _module.policy_evaluation_exact


def _toy_mdp():
    # 3 states, 2 actions, deterministic transitions:
    # s0 --a0--> s1 (r=0)     s0 --a1--> s2 (r=5, then stuck)
    # s1 --a0--> s2 (r=10)    s1 --a1--> s0 (r=0)
    # s2 is absorbing (both actions loop to s2, r=0)
    num_states, num_actions = 3, 2
    P = np.zeros((num_states, num_actions, num_states))
    R = np.zeros((num_states, num_actions, num_states))
    P[0, 0, 1] = 1.0
    P[0, 1, 2] = 1.0
    R[0, 1, 2] = 5.0
    P[1, 0, 2] = 1.0
    R[1, 0, 2] = 10.0
    P[1, 1, 0] = 1.0
    P[2, 0, 2] = 1.0
    P[2, 1, 2] = 1.0
    return P, R


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_value_iteration_finds_the_correct_optimal_values():
    P, R = _toy_mdp()
    V, policy = value_iteration(P, R, gamma=0.9)
    assert np.allclose(V, [9.0, 10.0, 0.0], atol=1e-4)


def test_02_optimal_policy_takes_the_higher_value_action():
    P, R = _toy_mdp()
    _, policy = value_iteration(P, R, gamma=0.9)
    # From s0: going straight to s2 for reward 5 is worse than going to
    # s1 first (0.9 * 10 = 9 > 5), so the optimal policy takes action 0.
    assert policy[0] == 0
    # From s1: going straight to s2 for reward 10 beats looping back to
    # s0 (whose best future value is only 9 after discounting).
    assert policy[1] == 0


# --- General-case coverage --------------------------------------------


def test_03_bellman_backup_matches_hand_computation():
    P, R = _toy_mdp()
    V = np.array([0.0, 0.0, 0.0])
    new_V, Q = bellman_backup(V, P, R, gamma=0.9)
    assert np.allclose(Q[0], [0.0, 5.0])
    assert np.allclose(Q[1], [10.0, 0.0])
    assert np.allclose(new_V, [5.0, 10.0, 0.0])


def test_04_value_iteration_matches_exact_policy_evaluation():
    # Independent oracle: solve the Bellman equation directly (linear
    # algebra) for the policy value_iteration converged to, and
    # confirm it's genuinely a fixed point, not just a plausible-looking
    # number from truncated iteration.
    P, R = _toy_mdp()
    V, policy = value_iteration(P, R, gamma=0.9)
    V_exact = policy_evaluation_exact(policy, P, R, gamma=0.9)
    assert np.allclose(V, V_exact, atol=1e-4)


def test_05_higher_discount_factor_favors_delayed_reward_more():
    P, R = _toy_mdp()
    V_low_gamma, _ = value_iteration(P, R, gamma=0.1)
    V_high_gamma, _ = value_iteration(P, R, gamma=0.99)
    # With low gamma, going straight to the immediate reward-5 exit
    # dominates; with high gamma, routing through s1 for reward 10 wins.
    assert V_low_gamma[0] < V_high_gamma[0]


# --- Parameter handling -------------------------------------------------


def test_06_converges_within_a_reasonable_number_of_iterations():
    P, R = _toy_mdp()
    V, _ = value_iteration(P, R, gamma=0.9, theta=1e-10, max_iterations=1000)
    assert np.allclose(V, [9.0, 10.0, 0.0], atol=1e-6)


def test_07_zero_discount_factor_only_values_immediate_reward():
    P, R = _toy_mdp()
    V, policy = value_iteration(P, R, gamma=0.0)
    # With gamma=0, the future is worthless -- from s0, the best
    # IMMEDIATE reward is 5 (action 1), even though it's a worse
    # long-term choice.
    assert np.isclose(V[0], 5.0)
    assert policy[0] == 1


# --- Edge cases ---------------------------------------------------------


def test_08_absorbing_state_has_zero_value():
    P, R = _toy_mdp()
    V, _ = value_iteration(P, R, gamma=0.9)
    assert np.isclose(V[2], 0.0)


def test_09_single_state_mdp():
    P = np.ones((1, 1, 1))
    R = np.array([[[3.0]]])
    V, policy = value_iteration(P, R, gamma=0.5)
    # V = R + gamma*V => V = R / (1 - gamma) = 3 / 0.5 = 6
    assert np.isclose(V[0], 6.0, atol=1e-4)
    assert policy[0] == 0


# --- Independent correctness oracle -----------------------------------


def test_10_bellman_backup_output_is_a_genuine_fixed_point_at_convergence():
    # Directly targets a mutant that stops one Bellman backup short of
    # true convergence (e.g. off-by-one iteration count): applying
    # bellman_backup ONE MORE TIME to the converged V must leave it
    # essentially unchanged.
    P, R = _toy_mdp()
    V, _ = value_iteration(P, R, gamma=0.9, theta=1e-10)
    V_next, _ = bellman_backup(V, P, R, gamma=0.9)
    assert np.allclose(V, V_next, atol=1e-6)
