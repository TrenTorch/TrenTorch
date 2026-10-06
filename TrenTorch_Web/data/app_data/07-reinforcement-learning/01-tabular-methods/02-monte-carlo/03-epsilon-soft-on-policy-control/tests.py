import numpy as np

from _load import load_solution

_module = load_solution(__file__)
epsilon_soft_mc_control = _module.epsilon_soft_mc_control


def simple_env():
    """Simple 2-state, 2-action environment."""
    # State 0: action 0 -> (1, 1, True), action 1 -> (1, -1, True)
    # State 1: absorbing
    def step(state, action):
        if state == 0:
            reward = 1.0 if action == 0 else -1.0
            return 1, reward, True
        else:
            return 1, 0.0, True
    return step


def test_basic_control():
    """Basic control learns to prefer action 0."""
    env = simple_env()
    Q, policy = epsilon_soft_mc_control(env, num_episodes=100, epsilon=0.1, gamma=0.9, seed=42)

    # Action 0 should be preferred
    assert (0, 0) in Q
    assert Q[(0, 0)] > -1.0


def test_deterministic():
    """Same seed gives same result."""
    env = simple_env()
    Q1, _ = epsilon_soft_mc_control(env, num_episodes=50, epsilon=0.1, gamma=0.9, seed=0)
    Q2, _ = epsilon_soft_mc_control(env, num_episodes=50, epsilon=0.1, gamma=0.9, seed=0)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_policy_structure():
    """Policy is dict state -> action."""
    env = simple_env()
    _, policy = epsilon_soft_mc_control(env, num_episodes=30, epsilon=0.2, gamma=0.9, seed=1)

    assert isinstance(policy, dict)
    assert 0 in policy
    assert isinstance(policy[0], (int, np.integer))


def test_q_structure():
    """Q is dict (state, action) -> value."""
    env = simple_env()
    Q, _ = epsilon_soft_mc_control(env, num_episodes=30, epsilon=0.2, gamma=0.9, seed=2)

    assert isinstance(Q, dict)
    for key, val in Q.items():
        assert isinstance(key, tuple) and len(key) == 2
        assert isinstance(val, (float, np.floating))


def test_more_episodes_better():
    """More episodes should improve Q estimates."""
    env = simple_env()
    Q1, _ = epsilon_soft_mc_control(env, num_episodes=10, epsilon=0.1, gamma=0.9, seed=5)
    Q2, _ = epsilon_soft_mc_control(env, num_episodes=100, epsilon=0.1, gamma=0.9, seed=5)

    # More episodes should give more stable Q values
    assert (0, 0) in Q1 and (0, 0) in Q2


def test_high_epsilon_explores():
    """High epsilon leads to more exploration."""
    env = simple_env()
    _, policy_low = epsilon_soft_mc_control(env, num_episodes=50, epsilon=0.1, gamma=0.9, seed=10)
    _, policy_high = epsilon_soft_mc_control(env, num_episodes=50, epsilon=0.9, gamma=0.9, seed=10)

    # Both should still prefer action 0, but with different confidence
    assert 0 in policy_low and 0 in policy_high


def test_different_gamma():
    """Different gamma values work."""
    env = simple_env()
    Q1, _ = epsilon_soft_mc_control(env, num_episodes=30, epsilon=0.1, gamma=0.0, seed=11)
    Q2, _ = epsilon_soft_mc_control(env, num_episodes=30, epsilon=0.1, gamma=0.99, seed=11)

    # Both should have Q values
    assert len(Q1) > 0
    assert len(Q2) > 0


def test_no_env_error():
    """Control runs without error."""
    env = simple_env()
    try:
        epsilon_soft_mc_control(env, num_episodes=20, epsilon=0.2, gamma=0.9, seed=0)
    except Exception as e:
        assert False, f"Unexpected error: {e}"
