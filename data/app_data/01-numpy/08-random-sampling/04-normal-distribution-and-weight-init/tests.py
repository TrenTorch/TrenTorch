"""
pytest data/app_data/01-numpy/08-random-sampling/04-normal-distribution-and-weight-init/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/08-random-sampling/{Path(__file__).resolve().parent.name}")
sample_normal = _module.sample_normal
empirical_mean_std = _module.empirical_mean_std
he_init = _module.he_init


def test_correct_shape():
    rng = np.random.default_rng(0)
    assert sample_normal(rng, 0, 1, (3, 4)).shape == (3, 4)
    assert he_init(rng, 10, 20).shape == (10, 20)


def test_sample_statistics_near_the_parameters():
    rng = np.random.default_rng(0)
    samples = sample_normal(rng, 5.0, 3.0, (500_000,))
    mean, std = empirical_mean_std(samples)
    assert abs(mean - 5.0) < 0.05
    assert abs(std - 3.0) < 0.05


def test_empirical_mean_std_works_on_multidimensional_input():
    rng = np.random.default_rng(0)
    samples_2d = sample_normal(rng, 0, 1, (100, 50))
    mean_2d, std_2d = empirical_mean_std(samples_2d)
    mean_flat, std_flat = empirical_mean_std(samples_2d.flatten())
    assert mean_2d == mean_flat
    assert std_2d == std_flat
    assert isinstance(mean_2d, float)
    assert isinstance(std_2d, float)


def test_he_initialization_scale():
    rng = np.random.default_rng(0)
    fan_in = 256
    weights = he_init(rng, fan_in, 128)
    expected_std = np.sqrt(2.0 / fan_in)
    assert abs(weights.std() - expected_std) < 0.01
    assert abs(weights.mean()) < 0.01


def test_he_scale_depends_on_fan_in_not_fan_out():
    fan_in = 100
    rng_a = np.random.default_rng(1)
    rng_b = np.random.default_rng(2)
    weights_small_out = he_init(rng_a, fan_in, 10)
    weights_large_out = he_init(rng_b, fan_in, 10000)
    assert abs(weights_small_out.std() - weights_large_out.std()) < 0.05


def test_not_degenerate():
    rng = np.random.default_rng(0)
    weights = he_init(rng, 20, 10)
    assert weights.std() > 0
    assert not np.any(np.all(weights == 0, axis=1))


def test_reproducible():
    rng_a = np.random.default_rng(42)
    rng_b = np.random.default_rng(42)
    np.testing.assert_array_equal(he_init(rng_a, 5, 5), he_init(rng_b, 5, 5))
