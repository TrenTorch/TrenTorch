"""
pytest data/app_data/99-potd/01-daily/24-fraud-label-surprise-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
entropy = _module.entropy


def test_example_matches_the_specs_worked_value():
    p = np.array([0.995, 0.005])
    assert abs(entropy(p) - 0.045415) < 1e-5


def test_a_zero_probability_class_contributes_nothing_and_is_finite():
    p = np.array([0.5, 0.5, 0.0])
    h = entropy(p)
    assert np.isfinite(h)
    assert abs(h - 1.0) < 1e-6  # same as the two-class uniform case


def test_uniform_distribution_equals_log2_k():
    for k in [2, 4, 8, 100]:
        p = np.full(k, 1.0 / k)
        assert abs(entropy(p) - np.log2(k)) < 1e-6


def test_one_dominant_class_among_many_tiny_ones_is_stable():
    k = 100
    p = np.full(k, 0.0001)
    p[0] = 1.0 - 0.0001 * (k - 1)
    h = entropy(p)
    assert np.isfinite(h)
    assert 0 < h < np.log2(k)


def test_a_single_certain_outcome_has_zero_entropy():
    p = np.array([1.0, 0.0, 0.0, 0.0])
    assert abs(entropy(p)) < 1e-9


def test_matches_a_reference_on_random_distributions():
    rng = np.random.default_rng(24)
    for _ in range(20):
        k = rng.integers(2, 50)
        raw = rng.uniform(0, 1, size=k)
        p = raw / raw.sum()
        nz = p > 0
        expected = float(-np.sum(p[nz] * np.log2(p[nz])))
        assert abs(entropy(p) - expected) < 1e-6
