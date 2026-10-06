import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
compute_curiosity_reward = _module.compute_curiosity_reward


def test_perfect_prediction():
    """Perfect prediction gives zero curiosity reward."""
    state = [1.0, 2.0]
    action = 0
    next_state = [2.0, 3.0]
    predicted = [2.0, 3.0]

    reward = compute_curiosity_reward(state, action, next_state, predicted)

    assert np.isclose(reward, 0.0)


def test_high_error():
    """High prediction error gives high curiosity."""
    state = [0.0, 0.0]
    action = 0
    next_state = [10.0, 10.0]
    predicted = [0.0, 0.0]

    reward = compute_curiosity_reward(state, action, next_state, predicted)

    # Error = sqrt(100 + 100) = 14.14, squared = 200
    assert reward > 0


def test_curiosity_scaling():
    """Higher curiosity_strength scales reward."""
    state = [0.0]
    action = 0
    next_state = [2.0]
    predicted = [0.0]

    reward1 = compute_curiosity_reward(state, action, next_state, predicted, curiosity_strength=1.0)
    reward2 = compute_curiosity_reward(state, action, next_state, predicted, curiosity_strength=2.0)

    assert np.isclose(reward2, 2 * reward1)


def test_novelty_vs_known():
    """Novel states give more reward than known."""
    state = [1.0, 1.0]
    action = 0
    next_state = [5.0, 5.0]

    # Novel: high error
    novel_predicted = [1.0, 1.0]
    novel_reward = compute_curiosity_reward(state, action, next_state, novel_predicted)

    # Known: low error
    known_predicted = [4.9, 4.9]
    known_reward = compute_curiosity_reward(state, action, next_state, known_predicted)

    assert novel_reward > known_reward


def test_multidimensional_state():
    """Works with multi-dimensional states."""
    state = np.random.randn(10)
    action = 3
    next_state = np.random.randn(10)
    predicted = next_state + np.random.randn(10) * 0.1

    reward = compute_curiosity_reward(state, action, next_state, predicted)

    assert reward >= 0
