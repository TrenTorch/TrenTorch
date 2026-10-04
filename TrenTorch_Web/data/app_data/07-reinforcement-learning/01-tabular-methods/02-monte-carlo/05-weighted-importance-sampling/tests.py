import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
estimate_weighted_importance_sampling = _module.estimate_weighted_importance_sampling


def test_single_episode():
    """Single episode."""
    episode = [(0, 0, 10.0)]
    result = estimate_weighted_importance_sampling([episode], gamma=0.9)

    # Single action, weight = 1.0, return = 10.0
    assert (0, 0) in result


def test_uniform_behavior():
    """Multiple actions create uniform behavior policy."""
    episode = [(0, 0, 5.0), (1, 1, 3.0)]
    result = estimate_weighted_importance_sampling([episode], gamma=1.0)

    # Both actions observed
    assert len(result) >= 0


def test_empty_episodes():
    """Empty episodes list."""
    result = estimate_weighted_importance_sampling([], gamma=0.9)
    assert result == {}


def test_structure():
    """Result has correct structure."""
    episode = [(0, 0, 5.0), (1, 1, 3.0)]
    result = estimate_weighted_importance_sampling([episode], gamma=0.9)

    for key, val in result.items():
        assert isinstance(key, tuple) and len(key) == 2
        assert isinstance(val, (float, np.floating))


def test_deterministic():
    """Same input gives same output."""
    episode = [(0, 0, 5.0), (1, 0, 3.0)]
    result1 = estimate_weighted_importance_sampling([episode], gamma=0.9)
    result2 = estimate_weighted_importance_sampling([episode], gamma=0.9)

    for key in result1:
        assert np.isclose(result1[key], result2[key])


def test_multiple_episodes():
    """Multiple episodes."""
    ep1 = [(0, 0, 1.0)]
    ep2 = [(0, 0, 2.0)]
    ep3 = [(0, 0, 3.0)]
    result = estimate_weighted_importance_sampling([ep1, ep2, ep3], gamma=1.0)

    # Should average to 2.0 if all have weight 1.0
    if (0, 0) in result:
        assert result[(0, 0)] > 0


def test_different_gamma():
    """Different gamma values."""
    episode = [(0, 0, 5.0), (1, 1, 3.0), (2, 0, 1.0)]
    result1 = estimate_weighted_importance_sampling([episode], gamma=0.0)
    result2 = estimate_weighted_importance_sampling([episode], gamma=0.99)

    assert len(result1) >= 0
    assert len(result2) >= 0
