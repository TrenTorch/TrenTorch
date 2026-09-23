"""
pytest data/app_data/99-potd/01-daily/15-thumbnail-normalize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
normalize_image = _module.normalize_image


def test_example_matches_the_specs_worked_values():
    matrix = np.array([[100.0, 150.0], [200.0, 250.0]])
    mu, sigma, normalized = normalize_image(matrix)
    assert abs(mu - 175.0) < 1e-6
    assert abs(sigma - 55.901699) < 1e-5
    np.testing.assert_allclose(
        normalized, [[-1.341641, -0.447214], [0.447214, 1.341641]], atol=1e-5
    )


def test_constant_image_gives_zero_sigma_and_all_zero_output():
    matrix = np.full((5, 5), 42.0)
    mu, sigma, normalized = normalize_image(matrix)
    assert abs(mu - 42.0) < 1e-9
    assert sigma == 0.0
    assert not normalized.any()


def test_single_pixel_image_is_the_same_convention():
    matrix = np.array([[7.0]])
    mu, sigma, normalized = normalize_image(matrix)
    assert mu == 7.0
    assert sigma == 0.0
    assert normalized[0, 0] == 0.0


def test_large_dynamic_range_is_numerically_stable():
    rng = np.random.default_rng(9)
    matrix = rng.integers(0, 65536, size=(64, 64)).astype(float)
    mu, sigma, normalized = normalize_image(matrix)
    expected_mu = matrix.mean()
    expected_sigma = matrix.std()
    assert abs(mu - expected_mu) < 1e-3
    assert abs(sigma - expected_sigma) < 1e-3
    np.testing.assert_allclose(normalized, (matrix - expected_mu) / expected_sigma, atol=1e-3)


def test_normalized_output_has_zero_mean_and_unit_std():
    rng = np.random.default_rng(10)
    matrix = rng.uniform(0, 255, size=(32, 32))
    _, _, normalized = normalize_image(matrix)
    assert abs(normalized.mean()) < 1e-9
    assert abs(normalized.std() - 1.0) < 1e-9
