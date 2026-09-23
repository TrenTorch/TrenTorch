"""
pytest data/app_data/99-potd/01-daily/39-gradient-seatbelt-clipping/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
clip_grad_norm = _module.clip_grad_norm


def test_example_matches_the_specs_worked_values():
    g = np.array([3.0, 4.0])
    result = clip_grad_norm(g, 2.0)
    np.testing.assert_allclose(result, [1.2, 1.6], atol=1e-6)


def test_norm_exactly_equal_to_tau_is_not_clipped():
    g = np.array([3.0, 4.0])  # norm = 5.0
    result = clip_grad_norm(g, 5.0)
    np.testing.assert_allclose(result, g, atol=1e-12)


def test_norm_well_below_tau_passes_through_unchanged():
    g = np.array([0.1, 0.2, -0.1])
    result = clip_grad_norm(g, 100.0)
    np.testing.assert_allclose(result, g, atol=1e-12)


def test_zero_gradient_stays_zero():
    g = np.zeros(5)
    result = clip_grad_norm(g, 1.0)
    assert not result.any()


def test_clipped_gradient_has_norm_exactly_tau():
    rng = np.random.default_rng(36)
    g = rng.uniform(-100, 100, size=50)
    tau = 3.5
    result = clip_grad_norm(g, tau)
    if np.linalg.norm(g) > tau:
        assert abs(np.linalg.norm(result) - tau) < 1e-6


def test_matches_a_reference_on_random_vectors():
    rng = np.random.default_rng(37)
    for _ in range(30):
        d = rng.integers(1, 200)
        g = rng.uniform(-50, 50, size=d)
        tau = rng.uniform(0.1, 50.0)
        norm = np.linalg.norm(g)
        expected = g * (tau / norm) if norm > tau else g
        np.testing.assert_allclose(clip_grad_norm(g, tau), expected, atol=1e-6)
