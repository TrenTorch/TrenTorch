import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
rbf_features = _module.rbf_features


def test_rbf_basic():
    """Basic RBF features."""
    state = 0.0
    centers = [0.0, 1.0, 2.0]

    features = rbf_features(state, centers)

    assert features.shape == (3,)
    assert np.all(features >= 0)
    assert np.all(features <= 1)


def test_rbf_at_center():
    """RBF is maximum at center."""
    state = 0.0
    centers = [0.0, 1.0]

    features = rbf_features(state, centers)

    # First center should have highest feature
    assert features[0] > features[1]
    assert np.isclose(features[0], 1.0)


def test_rbf_decays():
    """RBF decays with distance."""
    state = 0.0
    centers = np.array([0.0, 0.5, 1.0, 2.0])

    features = rbf_features(state, centers)

    # Should be monotonically decreasing
    assert np.all(np.diff(features) < 0)


def test_rbf_sigma_effect():
    """Larger sigma makes RBF wider."""
    state = 0.0
    centers = [2.0]

    features_narrow = rbf_features(state, centers, sigma=0.5)
    features_wide = rbf_features(state, centers, sigma=2.0)

    # Wide RBF should have higher value far from center
    assert features_wide[0] > features_narrow[0]


def test_rbf_multidimensional():
    """RBF works on multi-dimensional states."""
    state = [0.0, 0.0]
    centers = [[0.0, 0.0], [1.0, 1.0], [2.0, 0.0]]

    features = rbf_features(state, centers)

    assert features.shape == (3,)
    assert np.isclose(features[0], 1.0)  # At origin center


def test_rbf_normalization():
    """RBF features are in [0, 1]."""
    state = np.random.randn(2)
    centers = np.random.randn(5, 2)

    features = rbf_features(state, centers)

    assert np.all(features >= 0)
    assert np.all(features <= 1)
