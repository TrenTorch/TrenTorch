import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
simulate_lunar_lander = _module.simulate_lunar_lander


def test_basic_simulation():
    """Basic Lunar Lander simulation."""
    initial = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    actions = [2] * 100  # Main engine

    trajectory = simulate_lunar_lander(initial, actions)

    assert len(trajectory) > 0
    for state, reward, done in trajectory:
        assert state.shape == (7,)


def test_gravity_descent():
    """No thrust causes descent."""
    initial = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    actions = [0] * 50  # No thrust

    trajectory = simulate_lunar_lander(initial, actions)

    # Should descend
    first_y = trajectory[0][0][1]
    for state, _, _ in trajectory[1:]:
        if state[1] < 0:
            break
        assert state[1] < first_y


def test_safe_landing():
    """Soft landing with correct thrust."""
    initial = [0.0, 5.0, 0.0, -0.5, 0.0, 0.0, 1.0]
    actions = [2] * 100

    trajectory = simulate_lunar_lander(initial, actions)

    # Should eventually land
    assert trajectory[-1][2] == True


def test_state_dimension():
    """State has correct dimension."""
    initial = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    actions = [0, 1, 2, 3]

    trajectory = simulate_lunar_lander(initial, actions)

    for state, _, _ in trajectory:
        assert len(state) == 7


def test_fuel_depletion():
    """Fuel eventually depletes."""
    initial = [0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.01]
    actions = [2] * 100

    trajectory = simulate_lunar_lander(initial, actions, max_steps=20)

    # Should run out of fuel or reach ground
    assert len(trajectory) > 0
