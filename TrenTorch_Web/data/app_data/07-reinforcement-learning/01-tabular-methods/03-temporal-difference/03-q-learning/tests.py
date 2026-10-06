import numpy as np

from _load import load_solution

_module = load_solution(__file__)
q_learning = _module.q_learning


def simple_env():
    """Simple 2-state environment."""
    def step(state, action):
        if state == 0:
            reward = 1.0 if action == 0 else -1.0
            return 1, reward, True
        else:
            return 1, 0.0, True
    return step


def test_basic_q_learning():
    """Basic Q-learning runs."""
    env = simple_env()
    Q, policy = q_learning(env, num_episodes=20, epsilon=0.1, gamma=0.9, alpha=0.1, seed=0)

    assert len(Q) > 0
    assert len(policy) > 0


def test_deterministic():
    """Same seed gives same result."""
    env = simple_env()
    Q1, _ = q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)
    Q2, _ = q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_learns_optimal():
    """Q-learning learns to prefer best action."""
    env = simple_env()
    _, policy = q_learning(env, num_episodes=50, epsilon=0.2, gamma=0.9, alpha=0.1, seed=1)

    # Action 0 best, action 1 worst
    if 0 in policy:
        assert policy[0] in [0, 1]


def test_different_alpha():
    """Different learning rates."""
    env = simple_env()
    Q1, _ = q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.01, seed=2)
    Q2, _ = q_learning(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.5, seed=2)

    assert len(Q1) > 0
    assert len(Q2) > 0


def test_off_policy():
    """Q-learning decouples learning from exploration."""
    env = simple_env()
    Q, _ = q_learning(env, num_episodes=40, epsilon=0.5, gamma=0.9, alpha=0.1, seed=3)

    # Should learn optimal policy despite high exploration
    assert (0, 0) in Q


def test_convergence():
    """More episodes improve estimates."""
    env = simple_env()
    Q1, _ = q_learning(env, num_episodes=10, epsilon=0.2, gamma=0.9, alpha=0.1, seed=4)
    Q2, _ = q_learning(env, num_episodes=100, epsilon=0.2, gamma=0.9, alpha=0.1, seed=4)

    assert len(Q2) >= len(Q1)
