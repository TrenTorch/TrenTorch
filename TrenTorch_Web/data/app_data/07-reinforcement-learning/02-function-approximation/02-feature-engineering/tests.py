import numpy as np
from numpy import array
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
polynomial_features = _module.polynomial_features


def test_degree_one():
    """Degree 1: [1, s]."""
    features = polynomial_features(state=2.0, degree=1)

    assert len(features) == 2
    assert isinstance(features, np.ndarray)


def test_degree_three():
    """Degree 3: [1, s, s^2, s^3]."""
    features = polynomial_features(state=0.5, degree=3)

    assert len(features) == 4


def test_normalization():
    """Features [1, s, s^2] for s=2 are [1, 2, 4]; standardized they have mean 0 and std 1."""
    features = polynomial_features(state=2.0, degree=2)
    assert np.isclose(np.mean(features), 0.0, atol=1e-6)
    assert np.isclose(np.std(features), 1.0, atol=1e-6)


def test_constant_features_are_left_unchanged():
    """For s=1 all features equal 1 (std 0), so no normalization is applied."""
    np.testing.assert_allclose(polynomial_features(state=1.0, degree=2), [1.0, 1.0, 1.0])

def test_different_states():
    """Different states give different features."""
    f1 = polynomial_features(state=0.0, degree=2)
    f2 = polynomial_features(state=1.0, degree=2)
    f3 = polynomial_features(state=2.0, degree=2)

    # Features should differ
    assert not np.allclose(f1, f2)
    assert not np.allclose(f2, f3)


def test_negative_state():
    """Handle negative states."""
    features = polynomial_features(state=-1.5, degree=2)

    assert len(features) == 3
    assert np.all(np.isfinite(features))


def test_zero_state():
    """Handle zero state."""
    features = polynomial_features(state=0.0, degree=2)

    assert len(features) == 3


def test_large_state():
    """Handle large states."""
    features = polynomial_features(state=100.0, degree=2)

    assert len(features) == 3
    assert np.all(np.isfinite(features))


def test_output_type():
    """Output is numpy array of floats."""
    features = polynomial_features(state=1.5, degree=2)

    assert isinstance(features, np.ndarray)
    assert features.dtype in [np.float32, np.float64]
