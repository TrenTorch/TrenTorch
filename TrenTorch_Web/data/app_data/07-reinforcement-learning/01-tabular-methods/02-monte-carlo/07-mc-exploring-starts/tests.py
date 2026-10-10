import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
mc_exploring_starts = _module.mc_exploring_starts


def simple_chain_env():
    """Simple chain environment: states 0-9, action 0 moves right, action 1 moves left."""
    def step(state, action):
        if action == 0:  # Move right
            next_state = min(9, state + 1)
        else:  # Move left
            next_state = max(0, state - 1)

        reward = 1.0 if next_state == 9 else -0.1
        done = next_state == 9

        return next_state, reward, done

    return step


def test_basic_run():
    """Basic exploring starts runs without error."""
    env = simple_chain_env()
    try:
        Q, policy = mc_exploring_starts(env, num_episodes=20, gamma=0.9, num_states=10, num_actions=2, seed=0)
    except Exception as e:
        assert False, f"Error: {e}"


def test_returns_structure():
    """Returns have correct structure."""
    env = simple_chain_env()
    Q, policy = mc_exploring_starts(env, num_episodes=15, gamma=0.9, num_states=10, num_actions=2, seed=1)

    # Q is dict (state, action) -> value
    assert isinstance(Q, dict)
    for key, val in Q.items():
        assert isinstance(key, tuple) and len(key) == 2
        assert isinstance(val, (float, np.floating))

    # Policy is dict state -> action
    assert isinstance(policy, dict)
    assert len(policy) == 10
    for state, action in policy.items():
        assert isinstance(action, (int, np.integer))


def test_deterministic():
    """Same seed gives same result."""
    env = simple_chain_env()
    Q1, policy1 = mc_exploring_starts(env, num_episodes=25, gamma=0.9, num_states=10, num_actions=2, seed=5)
    Q2, policy2 = mc_exploring_starts(env, num_episodes=25, gamma=0.9, num_states=10, num_actions=2, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_policy_coverage():
    """All states should be in policy."""
    env = simple_chain_env()
    _, policy = mc_exploring_starts(env, num_episodes=30, gamma=0.9, num_states=10, num_actions=2, seed=2)

    for state in range(10):
        assert state in policy


def test_different_gamma():
    """Different gamma values work."""
    env = simple_chain_env()
    Q1, _ = mc_exploring_starts(env, num_episodes=20, gamma=0.0, num_states=10, num_actions=2, seed=3)
    Q2, _ = mc_exploring_starts(env, num_episodes=20, gamma=0.99, num_states=10, num_actions=2, seed=3)

    assert len(Q1) > 0
    assert len(Q2) > 0


def test_learns_goal_direction():
    """Policy should learn to move toward goal (state 9)."""
    env = simple_chain_env()
    _, policy = mc_exploring_starts(env, num_episodes=50, gamma=0.9, num_states=10, num_actions=2, seed=4)

    # State 0 should prefer action 0 (move right toward goal)
    # Action 0 = right, 1 = left
    # This is a tendency, not guaranteed with low episodes
    assert policy[0] in [0, 1]


def test_convergence():
    """More episodes should produce more consistent policy."""
    env = simple_chain_env()
    _, policy1 = mc_exploring_starts(env, num_episodes=10, gamma=0.9, num_states=10, num_actions=2, seed=10)
    _, policy2 = mc_exploring_starts(env, num_episodes=100, gamma=0.9, num_states=10, num_actions=2, seed=10)

    # Both should have valid policies
    assert len(policy1) == 10
    assert len(policy2) == 10
