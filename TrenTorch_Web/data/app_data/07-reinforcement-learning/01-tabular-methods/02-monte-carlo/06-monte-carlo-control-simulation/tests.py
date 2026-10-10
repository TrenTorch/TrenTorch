import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
mc_control_gridworld = _module.mc_control_gridworld


def test_basic_run():
    """Basic MC control runs without error."""
    try:
        Q, policy, rewards = mc_control_gridworld(num_episodes=10, epsilon=0.1, gamma=0.9, seed=0)
    except Exception as e:
        assert False, f"Error: {e}"


def test_returns_structure():
    """Returns correct structure."""
    Q, policy, rewards = mc_control_gridworld(num_episodes=5, epsilon=0.1, gamma=0.9, seed=1)

    # Q is dict (state, action) -> value
    assert isinstance(Q, dict)
    for key, val in Q.items():
        assert isinstance(key, tuple) and len(key) == 2
        assert isinstance(val, (float, np.floating))

    # Policy is dict state -> action
    assert isinstance(policy, dict)
    for state, action in policy.items():
        assert isinstance(state, tuple) and len(state) == 2
        assert isinstance(action, (int, np.integer))

    # Rewards is list
    assert isinstance(rewards, list)
    assert len(rewards) == 5


def test_convergence():
    """More episodes should improve policy."""
    _, _, rewards1 = mc_control_gridworld(num_episodes=10, epsilon=0.1, gamma=0.9, seed=10)
    _, _, rewards2 = mc_control_gridworld(num_episodes=100, epsilon=0.1, gamma=0.9, seed=10)

    # Later episodes in longer run should be better
    assert rewards2[-1] >= rewards2[0]


def test_deterministic():
    """Same seed gives same result."""
    Q1, policy1, _ = mc_control_gridworld(num_episodes=20, epsilon=0.1, gamma=0.9, seed=5)
    Q2, policy2, _ = mc_control_gridworld(num_episodes=20, epsilon=0.1, gamma=0.9, seed=5)

    for key in Q1:
        assert np.isclose(Q1[key], Q2[key])


def test_different_epsilon():
    """Different epsilon values."""
    _, policy_low, _ = mc_control_gridworld(num_episodes=30, epsilon=0.01, gamma=0.9, seed=11)
    _, policy_high, _ = mc_control_gridworld(num_episodes=30, epsilon=0.5, gamma=0.9, seed=11)

    # Both should produce valid policies
    assert len(policy_low) > 0
    assert len(policy_high) > 0


def test_goal_reachable():
    """Goal state (3,3) is in some policies."""
    _, policy, _ = mc_control_gridworld(num_episodes=50, epsilon=0.1, gamma=0.9, seed=12)

    # Goal should be in policy
    assert (3, 3) in policy


def test_episode_rewards_improve():
    """Episode rewards should trend positive after initial episodes."""
    _, _, rewards = mc_control_gridworld(num_episodes=30, epsilon=0.1, gamma=0.9, seed=13)

    # Last third should be better than first third
    if len(rewards) >= 6:
        first_third = np.mean(rewards[:10])
        last_third = np.mean(rewards[-10:])
        assert last_third > first_third


def test_all_states_in_policy():
    """All 16 grid states should be in policy."""
    _, policy, _ = mc_control_gridworld(num_episodes=50, epsilon=0.1, gamma=0.9, seed=14)

    expected_states = [(r, c) for r in range(4) for c in range(4)]
    for state in expected_states:
        assert state in policy
