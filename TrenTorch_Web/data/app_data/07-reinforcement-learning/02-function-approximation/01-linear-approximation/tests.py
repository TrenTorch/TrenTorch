import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
linear_td_update = _module.linear_td_update


def test_basic_update():
    """Basic linear TD update."""
    w = np.array([1.0, 2.0])
    phi = np.array([1.0, 0.0])
    next_phi = np.array([0.5, 1.0])

    w_new = linear_td_update(w, phi, reward=1.0, next_phi=next_phi, gamma=0.9, alpha=0.1)

    assert isinstance(w_new, np.ndarray)
    assert len(w_new) == 2


def test_td_error_positive():
    """Positive TD error increases weights."""
    w = np.ones(3)
    phi = np.ones(3)
    next_phi = np.zeros(3)

    # TD error = 10 + 0 - 3 = 7 (positive)
    w_new = linear_td_update(w, phi, reward=10.0, next_phi=next_phi, gamma=0.9, alpha=0.1)

    # All weights should increase
    assert np.all(w_new > w)


def test_td_error_negative():
    """Negative TD error decreases weights."""
    w = np.ones(3)
    phi = np.ones(3)
    next_phi = np.ones(3) * 10

    # TD error = 0 + 0.9*10 - 3 < 0
    w_new = linear_td_update(w, phi, reward=0.0, next_phi=next_phi, gamma=0.9, alpha=0.1)

    # All weights should decrease
    assert np.all(w_new < w)


def test_zero_alpha():
    """alpha=0 means no update."""
    w = np.array([1.0, 2.0])
    phi = np.array([1.0, 0.0])
    next_phi = np.array([0.5, 1.0])

    w_new = linear_td_update(w, phi, reward=10.0, next_phi=next_phi, gamma=0.9, alpha=0.0)

    assert np.allclose(w_new, w)


def test_zero_features():
    """Zero features mean no weight change."""
    w = np.array([1.0, 2.0])
    phi = np.array([0.0, 0.0])
    next_phi = np.array([1.0, 1.0])

    w_new = linear_td_update(w, phi, reward=5.0, next_phi=next_phi, gamma=0.9, alpha=0.1)

    # No change to w if phi is zero
    assert np.allclose(w_new, w)


def test_convergence():
    """Multiple updates converge to value."""
    w = np.zeros(1)
    phi = np.array([1.0])
    next_phi = np.array([0.0])

    for _ in range(100):
        w = linear_td_update(w, phi, reward=1.0, next_phi=next_phi, gamma=0.0, alpha=0.01)

    # Should converge to V(s) = 1.0
    assert np.isclose(w[0], 1.0, atol=0.1)


def test_different_gamma():
    """Different gamma values."""
    w = np.ones(2)
    phi = np.ones(2)
    next_phi = np.ones(2) * 2

    w1 = linear_td_update(w, phi, reward=1.0, next_phi=next_phi, gamma=0.0, alpha=0.1)
    w2 = linear_td_update(w, phi, reward=1.0, next_phi=next_phi, gamma=0.99, alpha=0.1)

    # Different gamma should give different updates
    assert not np.allclose(w1, w2)
