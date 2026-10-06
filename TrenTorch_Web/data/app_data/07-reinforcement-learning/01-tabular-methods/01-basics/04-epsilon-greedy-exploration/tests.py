import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
select_epsilon_greedy_action = _module.select_epsilon_greedy_action


def test_zero_epsilon_is_greedy():
    """With epsilon=0, always select max."""
    q_values = np.array([1.0, 5.0, 3.0, 2.0])
    rng = np.random.default_rng(seed=42)

    # Run many times
    for _ in range(50):
        action = select_epsilon_greedy_action(q_values, 0.0, rng)
        assert action == 1  # Index of max (5.0)


def test_one_epsilon_is_random():
    """With epsilon=1, always explore (random)."""
    q_values = np.array([1.0, 5.0, 3.0, 2.0])
    rng = np.random.default_rng(seed=42)

    # Collect actions over many samples
    actions = []
    for _ in range(200):
        action = select_epsilon_greedy_action(q_values, 1.0, rng)
        actions.append(action)

    # Should visit all actions with roughly equal probability
    unique_actions = set(actions)
    assert len(unique_actions) == 4
    # Each action visited ~50 times
    for action in range(4):
        count = sum(1 for a in actions if a == action)
        assert 30 < count < 70  # Rough uniform distribution


def test_half_epsilon():
    """With epsilon=0.5, roughly 50% greedy, 50% random."""
    q_values = np.array([1.0, 10.0, 2.0, 1.0])  # Best is action 1
    rng = np.random.default_rng(seed=42)

    actions = []
    for _ in range(1000):
        action = select_epsilon_greedy_action(q_values, 0.5, rng)
        actions.append(action)

    # Count times action 1 (greedy) was chosen
    greedy_count = sum(1 for a in actions if a == 1)
    # Should be roughly 50% + (1-50%)/4 = 50% + 12.5% = 62.5%
    # Allow wide margin
    assert 500 < greedy_count < 700


def test_small_epsilon():
    """With small epsilon, mostly greedy but occasional exploration."""
    q_values = np.array([1.0, 100.0, 1.0])  # Best is action 1
    rng = np.random.default_rng(seed=42)

    actions = []
    for _ in range(1000):
        action = select_epsilon_greedy_action(q_values, 0.05, rng)
        actions.append(action)

    # Most actions should be 1 (greedy)
    greedy_count = sum(1 for a in actions if a == 1)
    assert greedy_count > 900  # >90% greedy


def test_single_action():
    """Single action case should return action 0."""
    q_values = np.array([5.0])
    rng = np.random.default_rng(seed=42)

    for _ in range(20):
        action = select_epsilon_greedy_action(q_values, 0.5, rng)
        assert action == 0


def test_all_equal_values():
    """When all q-values are equal, greedy picks one (ties broken by argmax)."""
    q_values = np.array([5.0, 5.0, 5.0, 5.0])
    rng = np.random.default_rng(seed=42)

    # With epsilon=0, greedy is argmax which is action 0
    action = select_epsilon_greedy_action(q_values, 0.0, rng)
    assert action == 0


def test_negative_values():
    """Should handle negative q-values."""
    q_values = np.array([-10.0, -5.0, -20.0])
    rng = np.random.default_rng(seed=42)

    action = select_epsilon_greedy_action(q_values, 0.0, rng)
    assert action == 1  # Index of max (-5.0)


def test_determinism_with_seed():
    """Same seed should give same sequence."""
    q_values = np.array([1.0, 5.0, 3.0])

    rng1 = np.random.default_rng(seed=123)
    actions1 = [select_epsilon_greedy_action(q_values, 0.5, rng1) for _ in range(10)]

    rng2 = np.random.default_rng(seed=123)
    actions2 = [select_epsilon_greedy_action(q_values, 0.5, rng2) for _ in range(10)]

    assert actions1 == actions2


def test_return_type():
    """Should return an int."""
    q_values = np.array([1.0, 2.0, 3.0])
    rng = np.random.default_rng(seed=42)

    action = select_epsilon_greedy_action(q_values, 0.5, rng)
    assert isinstance(action, (int, np.integer))


def test_large_action_space():
    """Should work with many actions."""
    q_values = np.arange(100, dtype=float)[::-1]  # [99, 98, ..., 1, 0]
    rng = np.random.default_rng(seed=42)

    action = select_epsilon_greedy_action(q_values, 0.0, rng)
    assert action == 0  # Index of max (99)


def test_exploration_rate():
    """Test that exploration rate matches epsilon."""
    q_values = np.array([10.0, 1.0, 1.0])  # Best is action 0
    epsilon = 0.1
    rng = np.random.default_rng(seed=42)

    actions = []
    for _ in range(10000):
        action = select_epsilon_greedy_action(q_values, epsilon, rng)
        actions.append(action)

    # Non-greedy actions should be roughly epsilon * len(actions)
    non_greedy = sum(1 for a in actions if a != 0)
    expected_non_greedy = epsilon * len(actions)

    # Allow 20% error margin
    assert abs(non_greedy - expected_non_greedy) < 0.2 * expected_non_greedy
