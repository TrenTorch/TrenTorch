"""
pytest data/app_data/10-rl-alignment/01-reinforcement-learning/02-tabular-q-learning/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/01-reinforcement-learning/{Path(__file__).resolve().parent.name}")
epsilon_greedy_action = _module.epsilon_greedy_action
q_learning_update = _module.q_learning_update
train_q_learning = _module.train_q_learning

value_iteration = load_solution("10-rl-alignment/01-reinforcement-learning/01-value-iteration-mdp").value_iteration


def _toy_mdp():
    # Same 3-state MDP as 01-value-iteration-mdp, so Q-learning's
    # model-free answer can be checked against value iteration's
    # model-based (exact) one.
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
    return P, R, {2}


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_q_learning_converges_near_optimal_values():
    P, R, terminal = _toy_mdp()
    Q = train_q_learning(P, R, terminal, gamma=0.9, num_episodes=3000, seed=0)
    V_q = Q.max(axis=1)
    assert np.allclose(V_q, [9.0, 10.0, 0.0], atol=0.75)


def test_02_q_learning_update_matches_hand_computation():
    Q = np.zeros((2, 2))
    Q = q_learning_update(Q, state=0, action=0, reward=10.0, next_state=1, alpha=0.5, gamma=0.9, done=False)
    # target = 10 + 0.9*max(Q[1]) = 10 + 0 = 10; Q[0,0] += 0.5*(10-0) = 5
    assert np.isclose(Q[0, 0], 5.0)


# --- General-case coverage --------------------------------------------


def test_03_q_learning_matches_value_iteration_within_tolerance():
    # Independent oracle: model-free Q-learning (samples transitions
    # one at a time, never sees P/R directly to plan) should converge
    # toward the SAME optimal values as model-based value iteration on
    # the identical MDP.
    P, R, terminal = _toy_mdp()
    V_exact, _ = value_iteration(P, R, gamma=0.9)
    Q = train_q_learning(P, R, terminal, gamma=0.9, num_episodes=5000, seed=1)
    V_q = Q.max(axis=1)
    assert np.allclose(V_q, V_exact, atol=0.75)


def test_04_terminal_state_update_ignores_future_value():
    Q = np.array([[5.0, 5.0], [100.0, 100.0]])
    Q = q_learning_update(Q, state=0, action=0, reward=2.0, next_state=1, alpha=1.0, gamma=0.9, done=True)
    # done=True means the huge Q[1] values must NOT leak into the target.
    assert np.isclose(Q[0, 0], 2.0)


def test_05_epsilon_zero_is_fully_greedy():
    Q = np.array([[1.0, 9.0, 3.0]])
    rng = np.random.default_rng(0)
    actions = [epsilon_greedy_action(Q, 0, epsilon=0.0, rng=rng) for _ in range(20)]
    assert all(a == 1 for a in actions)


# --- Parameter handling -------------------------------------------------


def test_06_epsilon_one_is_fully_random():
    Q = np.array([[1.0, 9.0, 3.0]])
    rng = np.random.default_rng(0)
    actions = [epsilon_greedy_action(Q, 0, epsilon=1.0, rng=rng) for _ in range(200)]
    assert len(set(actions)) > 1  # not always picking the greedy action


def test_07_q_values_stay_finite_and_bounded_for_reasonable_training():
    P, R, terminal = _toy_mdp()
    Q = train_q_learning(P, R, terminal, gamma=0.9, num_episodes=500, seed=2)
    assert np.all(np.isfinite(Q))
    assert np.all(Q <= 15.0)  # can't exceed the best possible discounted return


# --- Edge cases ---------------------------------------------------------


def test_08_zero_episodes_leaves_q_at_zero():
    P, R, terminal = _toy_mdp()
    Q = train_q_learning(P, R, terminal, gamma=0.9, num_episodes=0, seed=0)
    assert np.allclose(Q, 0.0)


def test_09_update_does_not_mutate_unrelated_entries():
    Q = np.ones((3, 2)) * 7.0
    Q_copy = Q.copy()
    q_learning_update(Q, state=0, action=1, reward=1.0, next_state=2, alpha=0.5, gamma=0.9, done=False)
    assert np.isclose(Q[0, 0], Q_copy[0, 0])  # untouched entry unchanged
    assert not np.isclose(Q[0, 1], Q_copy[0, 1])  # the targeted entry did change


# --- Independent correctness oracle -----------------------------------


def test_10_learned_greedy_policy_matches_the_optimal_policy():
    # Directly targets a mutant that bootstraps off the wrong action's
    # Q-value (e.g. Q[next_state, action] instead of
    # Q[next_state].max()), which would still often look numerically
    # close but converge to the WRONG greedy policy in a state where
    # the two actions' values are close.
    P, R, terminal = _toy_mdp()
    _, optimal_policy = value_iteration(P, R, gamma=0.9)
    Q = train_q_learning(P, R, terminal, gamma=0.9, num_episodes=5000, seed=3)
    learned_policy = np.argmax(Q, axis=1)
    for s in range(P.shape[0]):
        if s in terminal:
            continue
        assert learned_policy[s] == optimal_policy[s]
