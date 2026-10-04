import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
compute_cooperative_value = _module.compute_cooperative_value


def test_basic_cooperation():
    """Basic cooperative value computation."""
    individual = [1.0, 2.0, 3.0]
    shared = 5.0

    value = compute_cooperative_value(individual, shared)

    # 1 + 2 + 3 + 1*5 = 11
    assert np.isclose(value, 11.0)


def test_shared_weight():
    """Shared reward weight scales correctly."""
    individual = [0.0, 0.0]
    shared = 10.0

    value_half = compute_cooperative_value(individual, shared, weight=0.5)
    value_full = compute_cooperative_value(individual, shared, weight=1.0)
    value_double = compute_cooperative_value(individual, shared, weight=2.0)

    assert np.isclose(value_half, 5.0)
    assert np.isclose(value_full, 10.0)
    assert np.isclose(value_double, 20.0)


def test_zero_individual():
    """Cooperative value with no individual value."""
    individual = [0.0, 0.0, 0.0]
    shared = 15.0

    value = compute_cooperative_value(individual, shared)

    assert np.isclose(value, 15.0)


def test_zero_shared():
    """Individual values with no shared reward."""
    individual = [5.0, 3.0, 2.0]
    shared = 0.0

    value = compute_cooperative_value(individual, shared)

    assert np.isclose(value, 10.0)


def test_many_agents():
    """Scale to many agents."""
    individual = np.ones(100)
    shared = 5.0

    value = compute_cooperative_value(individual, shared)

    # 100 + 5 = 105
    assert np.isclose(value, 105.0)


def test_negative_rewards():
    """Works with negative rewards."""
    individual = [-1.0, -2.0]
    shared = -3.0

    value = compute_cooperative_value(individual, shared)

    assert np.isclose(value, -6.0)
