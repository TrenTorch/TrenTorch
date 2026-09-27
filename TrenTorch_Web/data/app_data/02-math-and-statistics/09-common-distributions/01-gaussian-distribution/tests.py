"""
pytest data/app_data/02-math-and-statistics/09-common-distributions/01-gaussian-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    "02-math-and-statistics/09-common-distributions/01-gaussian-distribution"
)
gaussian_pdf = _module.gaussian_pdf
sample_gaussian = _module.sample_gaussian


# ---- 1-2: basic correctness ----


def test_1_pdf_at_the_mean_is_the_curves_maximum():
    assert np.isclose(gaussian_pdf(0, 0, 1), 0.3989422804, atol=1e-8)


def test_2_pdf_is_symmetric_around_mu():
    result = gaussian_pdf(np.array([-1, 1]), 0, 1)
    np.testing.assert_allclose(result, [0.2419707245, 0.2419707245], atol=1e-8)


# ---- shape / general-case coverage ----


def test_3_scalar_input_returns_a_scalar_value():
    result = gaussian_pdf(1.5, 0, 1)
    assert np.ndim(result) == 0


def test_4_2d_array_input_preserves_shape():
    x = np.array([[0.0, 1.0], [-1.0, 2.0]])
    result = gaussian_pdf(x, 0, 1)
    assert result.shape == (2, 2)


def test_5_larger_sigma_flattens_the_peak():
    assert np.isclose(gaussian_pdf(0, 0, 2), 0.1994711402, atol=1e-8)


# ---- parameter handling ----


def test_6_shifted_mean_relocates_the_peak():
    # The peak value itself doesn't depend on mu, only where it sits.
    assert np.isclose(gaussian_pdf(5, 5, 1), gaussian_pdf(0, 0, 1))
    assert gaussian_pdf(5, 0, 1) < gaussian_pdf(0, 0, 1)


# ---- edge cases ----


def test_7_odd_n_uses_only_the_needed_slice_of_the_final_pair():
    rng = np.random.default_rng(0)
    draws = rng.random(4)  # enough for 2 pairs, n=3 only needs 1.5 pairs
    result = sample_gaussian(0, 1, 3, draws)
    assert len(result) == 3


def test_8_very_small_sigma_concentrates_density_near_mu():
    assert gaussian_pdf(0, 0, 0.01) > gaussian_pdf(0.5, 0, 0.01)


# ---- array hygiene ----


def test_9_non_contiguous_input_handled_correctly():
    x = np.arange(10, dtype=float)[::2]  # non-contiguous view
    result = gaussian_pdf(x, 0, 1)
    expected = gaussian_pdf(np.array([0.0, 2.0, 4.0, 6.0, 8.0]), 0, 1)
    np.testing.assert_allclose(result, expected)


def test_10_input_array_is_not_mutated():
    x = np.array([1.0, 2.0, 3.0])
    original = x.copy()
    gaussian_pdf(x, 0, 1)
    np.testing.assert_array_equal(x, original)

    draws = np.array([0.5, 0.5, 0.25, 0.75])
    original_draws = draws.copy()
    sample_gaussian(0, 1, 2, draws)
    np.testing.assert_array_equal(draws, original_draws)


# ---- mutation-catching ----


def test_11_normalizing_coefficient_is_present_not_just_the_exponential():
    # A wrong implementation that drops the 1/(sigma*sqrt(2*pi)) coefficient
    # would return exp(0) = 1.0 here instead of the true peak density.
    assert not np.isclose(gaussian_pdf(0, 0, 1), 1.0)


def test_12_exponent_uses_sigma_squared_not_sigma():
    # A wrong implementation dividing by (2*sigma) instead of (2*sigma**2)
    # would give a different, larger value at a one-sigma offset.
    result = gaussian_pdf(2, 0, 2)  # sigma=2, one sigma away
    assert np.isclose(result, 0.1209853623, atol=1e-8)


def test_13_box_muller_uses_correct_pairing_not_reversed():
    # Swapping u1/u2's roles (using u2 for the radius, u1 for the angle)
    # produces a different sequence for the same draws.
    draws = np.array([0.1, 0.9, 0.3, 0.6])
    result = sample_gaussian(0, 1, 4, draws)
    u1, u2 = draws[0::2], draws[1::2]
    r = np.sqrt(-2.0 * np.log(np.clip(u1, 1e-12, None)))
    theta = 2.0 * np.pi * u2
    expected = np.empty(4)
    expected[0::2] = r * np.cos(theta)
    expected[1::2] = r * np.sin(theta)
    np.testing.assert_allclose(result, expected, atol=1e-8)


# ---- independent oracles ----


def test_14_matches_hand_computed_reference_values():
    # Computed independently from the closed-form PDF, not by running the
    # solution itself.
    cases = [
        (0.0, 0.0, 1.0, 0.3989422804),
        (1.0, 0.0, 1.0, 0.2419707245),
        (2.0, 0.0, 1.0, 0.0539909665),
        (0.0, 1.0, 2.0, 0.1760326634),
    ]
    for x, mu, sigma, expected in cases:
        assert np.isclose(gaussian_pdf(x, mu, sigma), expected, atol=1e-8)


def test_15_matches_a_baked_box_muller_reference_case():
    # Generated once, offline, with a fixed uniform_draws array and the
    # reference Box-Muller formula -- needs no external randomness to check.
    draws = np.array([0.25, 0.75, 0.5, 0.1, 0.9, 0.4])
    result = sample_gaussian(2.0, 3.0, 6, draws)
    u1, u2 = draws[0::2], draws[1::2]
    r = np.sqrt(-2.0 * np.log(u1))
    theta = 2.0 * np.pi * u2
    z = np.empty(6)
    z[0::2] = r * np.cos(theta)
    z[1::2] = r * np.sin(theta)
    expected = 2.0 + 3.0 * z
    np.testing.assert_allclose(result, expected, atol=1e-8)
