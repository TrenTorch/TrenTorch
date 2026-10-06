import numpy as np
import pytest

from _load import load_solution

# Load the solution
_module = load_solution(__file__)
compute_discounted_return = _module.compute_discounted_return


def test_single_reward():
    """Single reward should return just that reward."""
    assert compute_discounted_return([5.0], 0.9) == 5.0
    assert compute_discounted_return([10.0], 0.5) == 10.0


def test_zero_discount():
    """With gamma=0, only first reward counts."""
    assert compute_discounted_return([10.0, 5.0, 3.0], 0.0) == 10.0
    assert compute_discounted_return([1.0, 1.0, 1.0], 0.0) == 1.0


def test_full_discount():
    """With gamma=1, all rewards count equally."""
    result = compute_discounted_return([1.0, 1.0, 1.0], 1.0)
    assert np.isclose(result, 3.0)


def test_example_from_docstring():
    """Test the example: [10, 5, 3] with gamma=0.9."""
    rewards = [10.0, 5.0, 3.0]
    gamma = 0.9
    expected = 10.0 + 0.9 * 5.0 + 0.81 * 3.0
    result = compute_discounted_return(rewards, gamma)
    assert np.isclose(result, expected)


def test_geometric_series():
    """Test with uniform rewards: G = r * (1 - gamma^n) / (1 - gamma)."""
    r = 2.0
    gamma = 0.5
    n = 5
    rewards = [r] * n
    result = compute_discounted_return(rewards, gamma)
    expected = r * (1.0 - gamma**n) / (1.0 - gamma)
    assert np.isclose(result, expected)


def test_numpy_array_input():
    """Should handle numpy arrays as input."""
    rewards = np.array([1.0, 2.0, 3.0])
    result = compute_discounted_return(rewards, 0.9)
    expected = 1.0 + 0.9 * 2.0 + 0.81 * 3.0
    assert np.isclose(result, expected)


def test_list_input():
    """Should handle Python lists."""
    rewards = [1.0, 2.0, 3.0]
    result = compute_discounted_return(rewards, 0.9)
    expected = 1.0 + 0.9 * 2.0 + 0.81 * 3.0
    assert np.isclose(result, expected)


def test_long_episode():
    """Test on a longer episode where later terms are negligible."""
    rewards = np.ones(100)
    gamma = 0.99
    result = compute_discounted_return(rewards, gamma)
    # Expected: geometric series sum
    expected = (1.0 - gamma**100) / (1.0 - gamma)
    assert np.isclose(result, expected, rtol=1e-10)


def test_negative_rewards():
    """Should handle negative rewards correctly."""
    rewards = [10.0, -5.0, 3.0]
    gamma = 0.9
    expected = 10.0 + 0.9 * (-5.0) + 0.81 * 3.0
    result = compute_discounted_return(rewards, gamma)
    assert np.isclose(result, expected)


def test_zero_rewards():
    """With all zero rewards, return should be zero."""
    result = compute_discounted_return([0.0, 0.0, 0.0], 0.95)
    assert np.isclose(result, 0.0)


def test_input_not_modified():
    """Original input should not be modified."""
    rewards = [1.0, 2.0, 3.0]
    original = rewards.copy()
    compute_discounted_return(rewards, 0.9)
    assert rewards == original


def test_very_small_gamma():
    """With very small gamma, only first reward matters."""
    result = compute_discounted_return([100.0, 1000.0, 1000.0], 0.01)
    # 100 + 0.01*1000 + 0.0001*1000 = 100 + 10 + 0.1 = 110.1
    expected = 100.0 + 0.01 * 1000.0 + 0.0001 * 1000.0
    assert np.isclose(result, expected)
