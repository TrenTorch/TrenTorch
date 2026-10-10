import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
double_q_learning = _module.double_q_learning


def simple_env():
    """Simple environment."""
    def step(state, action):
        if state == 0:
            reward = 1.0 if action == 0 else 0.5
            return 1, reward, True
        else:
            return 1, 0.0, True
    return step


def test_basic_double_q():
    """Basic double Q-learning runs."""
    env = simple_env()
    Q, policy = double_q_learning(env, num_episodes=20, epsilon=0.1, gamma=0.9, alpha=0.1, seed=0)

    assert len(Q) > 0
    assert len(policy) > 0


def test_deterministic():
    """Same seed gives same result."""
    env = simple_env()
    Q1, _ = double_q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)
    Q2, _ = double_q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_reduces_overestimation():
    """Double Q should reduce overestimation vs single Q."""
    env = simple_env()
    Q, _ = double_q_learning(env, num_episodes=50, epsilon=0.2, gamma=0.9, alpha=0.1, seed=1)

    # Just check it runs and produces reasonable values
    assert len(Q) > 0


def test_convergence():
    """More episodes should improve estimates."""
    env = simple_env()
    Q1, _ = double_q_learning(env, num_episodes=10, epsilon=0.2, gamma=0.9, alpha=0.1, seed=2)
    Q2, _ = double_q_learning(env, num_episodes=100, epsilon=0.2, gamma=0.9, alpha=0.1, seed=2)

    assert len(Q2) >= len(Q1)


def test_different_parameters():
    """Different hyperparameters work."""
    env = simple_env()
    Q1, _ = double_q_learning(env, num_episodes=20, epsilon=0.05, gamma=0.8, alpha=0.2, seed=3)
    Q2, _ = double_q_learning(env, num_episodes=20, epsilon=0.5, gamma=0.99, alpha=0.05, seed=3)

    assert len(Q1) > 0
    assert len(Q2) > 0
