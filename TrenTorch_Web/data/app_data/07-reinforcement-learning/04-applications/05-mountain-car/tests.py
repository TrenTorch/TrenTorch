import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
simulate_mountain_car = _module.simulate_mountain_car


def test_basic_simulation():
    """Basic Mountain Car simulation."""
    initial = [-0.5, 0.0]
    actions = [-1, 0, 1] * 50

    trajectory = simulate_mountain_car(initial, actions)

    assert len(trajectory) > 0
    for state, reward, done in trajectory:
        assert state.shape == (2,)
        assert reward >= -1 or reward == 10


def test_no_direct_climb():
    """Can't climb directly right."""
    initial = [-0.5, 0.0]
    actions = [1] * 100  # Always push right

    trajectory = simulate_mountain_car(initial, actions, max_steps=10)

    # Shouldn't reach goal quickly
    assert len(trajectory) > 1
    assert not trajectory[-1][2]


def test_oscillation_helps():
    """Oscillating can eventually reach goal."""
    initial = [-0.5, 0.0]
    actions = [-1, 1] * 500  # Oscillate

    trajectory = simulate_mountain_car(initial, actions, max_steps=1000)

    # Long enough, might reach
    assert len(trajectory) > 1


def test_bounds():
    """Position stays within bounds."""
    initial = [0.0, 0.0]
    actions = [1] * 100

    trajectory = simulate_mountain_car(initial, actions)

    for state, _, _ in trajectory:
        assert -1.2 <= state[0] <= 0.6


def test_goal_reward():
    """Reaching goal gives +10 reward."""
    initial = [0.5, 0.01]  # Near goal
    actions = [1, 1, 1]

    trajectory = simulate_mountain_car(initial, actions)

    # Should quickly reach goal
    if trajectory[-1][2]:  # If done
        assert trajectory[-1][1] == 10.0
