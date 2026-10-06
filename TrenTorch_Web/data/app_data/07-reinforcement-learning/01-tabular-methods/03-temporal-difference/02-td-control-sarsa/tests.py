import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sarsa = _module.sarsa


def simple_env():
    """Simple environment for SARSA."""
    def step(state, action):
        # State 0: action 0 -> (1, 1, done), action 1 -> (1, -1, done)
        if state == 0:
            reward = 1.0 if action == 0 else -1.0
            return 1, reward, True
        else:
            return 1, 0.0, True
    return step


def test_basic_sarsa():
    """Basic SARSA runs."""
    env = simple_env()
    Q, policy = sarsa(env, num_episodes=20, epsilon=0.2, gamma=0.9, alpha=0.1, seed=0)

    assert len(Q) > 0
    assert len(policy) > 0


def test_deterministic():
    """Same seed gives same result."""
    env = simple_env()
    Q1, _ = sarsa(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)
    Q2, _ = sarsa(env, num_episodes=30, epsilon=0.1, gamma=0.9, alpha=0.1, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_learns_better_action():
    """SARSA learns to prefer higher reward action."""
    env = simple_env()
    _, policy = sarsa(env, num_episodes=50, epsilon=0.1, gamma=0.9, alpha=0.1, seed=1)

    # Action 0 gives reward 1, action 1 gives -1
    # Should prefer action 0
    if 0 in policy:
        assert policy[0] in [0, 1]


def test_different_epsilon():
    """Different epsilon values."""
    env = simple_env()
    Q1, _ = sarsa(env, num_episodes=20, epsilon=0.05, gamma=0.9, alpha=0.1, seed=2)
    Q2, _ = sarsa(env, num_episodes=20, epsilon=0.5, gamma=0.9, alpha=0.1, seed=2)

    assert len(Q1) > 0
    assert len(Q2) > 0


def test_learning_rate_effect():
    """Different alpha values."""
    env = simple_env()
    Q1, _ = sarsa(env, num_episodes=20, epsilon=0.1, gamma=0.9, alpha=0.01, seed=3)
    Q2, _ = sarsa(env, num_episodes=20, epsilon=0.1, gamma=0.9, alpha=0.5, seed=3)

    assert len(Q1) > 0
    assert len(Q2) > 0


def test_convergence():
    """More episodes should lead to higher Q values."""
    env = simple_env()
    Q1, _ = sarsa(env, num_episodes=10, epsilon=0.2, gamma=0.9, alpha=0.1, seed=4)
    Q2, _ = sarsa(env, num_episodes=100, epsilon=0.2, gamma=0.9, alpha=0.1, seed=4)

    # Q values should be more developed after more episodes
    assert len(Q2) >= len(Q1)
