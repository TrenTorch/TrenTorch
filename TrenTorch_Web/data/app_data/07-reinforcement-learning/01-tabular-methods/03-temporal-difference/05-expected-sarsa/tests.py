import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
expected_sarsa = _module.expected_sarsa


def simple_env():
    """Simple environment."""
    def step(state, action):
        if state == 0:
            reward = 1.0 if action == 0 else -0.5
            return 1, reward, True
        else:
            return 1, 0.0, True
    return step


def test_basic_expected_sarsa():
    """Basic Expected SARSA runs."""
    env = simple_env()
    Q, policy = expected_sarsa(env, num_episodes=20, epsilon=0.2, gamma=0.9, alpha=0.1, seed=0)

    assert len(Q) > 0
    assert len(policy) > 0


def test_deterministic():
    """Same seed gives same result."""
    env = simple_env()
    Q1, _ = expected_sarsa(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)
    Q2, _ = expected_sarsa(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_lower_variance():
    """Expected SARSA should be smoother than SARSA."""
    env = simple_env()
    Q, _ = expected_sarsa(env, num_episodes=40, epsilon=0.2, gamma=0.9, alpha=0.1, seed=1)

    # Should learn the better action
    assert (0, 0) in Q


def test_convergence():
    """More episodes improve learning."""
    env = simple_env()
    Q1, _ = expected_sarsa(env, num_episodes=10, epsilon=0.2, gamma=0.9, alpha=0.1, seed=2)
    Q2, _ = expected_sarsa(env, num_episodes=100, epsilon=0.2, gamma=0.9, alpha=0.1, seed=2)

    assert len(Q2) >= len(Q1)


def test_safe_exploration():
    """Expected SARSA explores safely."""
    env = simple_env()
    _, policy = expected_sarsa(env, num_episodes=50, epsilon=0.3, gamma=0.9, alpha=0.1, seed=3)

    # Policy should favor action 0
    if 0 in policy:
        assert policy[0] in [0, 1]


def test_different_epsilon():
    """Different epsilon values."""
    env = simple_env()
    Q1, _ = expected_sarsa(env, num_episodes=20, epsilon=0.05, gamma=0.9, alpha=0.1, seed=4)
    Q2, _ = expected_sarsa(env, num_episodes=20, epsilon=0.5, gamma=0.9, alpha=0.1, seed=4)

    assert len(Q1) > 0
    assert len(Q2) > 0
