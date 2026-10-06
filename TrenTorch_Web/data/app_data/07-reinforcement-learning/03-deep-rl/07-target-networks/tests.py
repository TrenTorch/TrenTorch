import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
soft_update_target_network = _module.soft_update_target_network


def test_soft_update_basic():
    """Basic soft update."""
    params_main = [2.0, 4.0]
    params_target = [0.0, 0.0]

    updated = soft_update_target_network(params_main, params_target, tau=0.1)

    assert updated.shape == (2,)
    assert np.allclose(updated, [0.2, 0.4])


def test_soft_update_identity():
    """Soft update with τ=1 equals main params."""
    params_main = [1.0, 2.0, 3.0]
    params_target = [5.0, 6.0, 7.0]

    updated = soft_update_target_network(params_main, params_target, tau=1.0)

    assert np.allclose(updated, params_main)


def test_soft_update_no_change():
    """Soft update with τ=0 equals target params."""
    params_main = [1.0, 2.0]
    params_target = [5.0, 6.0]

    updated = soft_update_target_network(params_main, params_target, tau=0.0)

    assert np.allclose(updated, params_target)


def test_soft_update_incremental():
    """Soft update interpolates."""
    params_main = [10.0]
    params_target = [0.0]

    updated = soft_update_target_network(params_main, params_target, tau=0.5)

    assert np.allclose(updated, [5.0])


def test_soft_update_small_tau():
    """Small τ changes target slowly."""
    params_main = [100.0, 100.0]
    params_target = [0.0, 0.0]

    tau = 0.001
    updated = soft_update_target_network(params_main, params_target, tau=tau)

    # Should be very close to target
    expected = (1 - tau) * params_target + tau * params_main
    assert np.allclose(updated, expected)
