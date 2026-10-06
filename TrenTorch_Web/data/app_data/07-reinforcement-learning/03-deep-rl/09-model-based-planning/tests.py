import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
dyna_backup = _module.dyna_backup


def test_basic_backup():
    """Basic Dyna backup."""
    rewards = [1.0, 0.0, -1.0]
    values = [5.0, 3.0, 0.0]

    targets = dyna_backup(rewards, values)

    assert targets.shape == (3,)
    np.testing.assert_allclose(targets, [5.95, 2.97, -1.0], atol=1e-5)


def test_zero_discount():
    """Zero gamma equals immediate reward."""
    rewards = [2.0, 3.0]
    values = [100.0, 100.0]

    targets = dyna_backup(rewards, values, gamma=0.0)

    assert np.allclose(targets, rewards)


def test_full_discount():
    """Gamma=1 includes full future value."""
    rewards = [0.0, 0.0]
    values = [10.0, 20.0]

    targets = dyna_backup(rewards, values, gamma=1.0)

    assert np.allclose(targets, values)


def test_mixed_planning():
    """Mixed real and imagined updates."""
    rewards = [1.0, 0.5, 0.0]  # Mix of real/imagined
    values = [2.0, 1.5, 1.0]

    targets = dyna_backup(rewards, values, gamma=0.99)

    # All should follow same backup
    np.testing.assert_allclose(targets, [2.98, 1.985, 0.99], atol=1e-5)


def test_converges_to_bootstrap():
    """High value states should have targets dominated by value."""
    rewards = [0.0]
    values = [100.0]

    targets = dyna_backup(rewards, values, gamma=0.99)

    assert targets[0] > 50.0  # Dominated by value
