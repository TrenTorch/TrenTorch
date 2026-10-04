import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
combine_value_advantage = _module.combine_value_advantage


def test_basic_combination():
    """Basic value-advantage combination."""
    value = 5.0
    advantage = [1.0, 2.0, 3.0]

    q_values = combine_value_advantage(value, advantage)

    assert q_values.shape == (3,)
    assert np.all(np.isfinite(q_values))


def test_zero_advantage():
    """Zero advantage gives value everywhere."""
    value = 10.0
    advantage = [0.0, 0.0, 0.0]

    q_values = combine_value_advantage(value, advantage)

    # Mean is 0, so Q = V + 0 = V
    assert np.allclose(q_values, value)


def test_advantage_centering():
    """Advantages are centered around zero."""
    value = 5.0
    advantage = [1.0, 2.0, 3.0]

    q_values = combine_value_advantage(value, advantage)

    # Mean advantage: (1+2+3)/3 = 2
    # Centered: [1-2, 2-2, 3-2] = [-1, 0, 1]
    # Q = 5 + centered = [4, 5, 6]
    expected = [4.0, 5.0, 6.0]
    assert np.allclose(q_values, expected)


def test_single_action():
    """Single action has zero centered advantage."""
    value = 7.0
    advantage = [2.0]

    q_values = combine_value_advantage(value, advantage)

    # Single value: mean = 2, centered = 0
    assert np.isclose(q_values[0], 7.0)


def test_negative_value():
    """Works with negative values."""
    value = -10.0
    advantage = [1.0, 0.0, -1.0]

    q_values = combine_value_advantage(value, advantage)

    # Mean advantage = 0, centered = same
    expected = [-10.0 + 1.0, -10.0, -10.0 - 1.0]
    assert np.allclose(q_values, expected)


def test_high_variance_advantage():
    """High variance advantages are preserved."""
    value = 0.0
    advantage = [10.0, -10.0]

    q_values = combine_value_advantage(value, advantage)

    # Mean = 0, centered = same
    assert np.allclose(q_values, advantage)
