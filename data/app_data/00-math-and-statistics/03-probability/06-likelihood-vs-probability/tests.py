"""
pytest data/app_data/00-math-and-statistics/03-probability/06-likelihood-vs-probability/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
normal_pdf = _module.normal_pdf
joint_density = _module.joint_density
likelihood_curve = _module.likelihood_curve


def test_normal_pdf_matches_known_oracle_values():
    # generated once, offline, via scipy.stats.norm.pdf
    x = np.array([1.0, 2.0, 3.0])
    expected = np.array([0.24197072, 0.39894228, 0.24197072])
    assert np.allclose(normal_pdf(x, mean=2.0, std=1.0), expected, atol=1e-6)


def test_normal_pdf_peaks_at_the_mean():
    x = np.linspace(-5.0, 5.0, 101)
    densities = normal_pdf(x, mean=0.0, std=1.0)
    assert np.isclose(x[np.argmax(densities)], 0.0, atol=0.1)


def test_normal_pdf_is_never_negative():
    x = np.array([-100.0, -1.0, 0.0, 1.0, 100.0])
    assert np.all(normal_pdf(x, mean=0.0, std=1.0) >= 0.0)


def test_joint_density_is_product_of_individual_densities():
    x_values = np.array([1.0, 2.0, 3.0])
    expected = np.prod([normal_pdf(np.array([v]), 2.0, 1.0)[0] for v in x_values])
    assert np.isclose(joint_density(x_values, mean=2.0, std=1.0), expected)


def test_likelihood_curve_returns_one_value_per_candidate_mean():
    x_values = np.array([1.0, 2.0, 3.0])
    candidates = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    result = likelihood_curve(x_values, candidates, std=1.0)
    assert result.shape == (5,)


def test_likelihood_curve_peaks_at_the_sample_mean():
    # The core MLE fact this question sets up: the likelihood curve for
    # a Normal distribution's mean peaks exactly at the sample mean.
    x_values = np.array([2.0, 4.0, 6.0])  # sample mean = 4.0
    candidates = np.linspace(0.0, 8.0, 81)
    result = likelihood_curve(x_values, candidates, std=1.0)
    best_mean = candidates[np.argmax(result)]
    assert np.isclose(best_mean, 4.0, atol=0.15)


def test_likelihood_curve_is_not_confused_with_summing_instead_of_multiplying():
    # Directly targets a mutant that sums individual densities instead
    # of multiplying them (treating the joint density like a probability
    # of "any" observation rather than "all" observations together).
    # For 3 independent observations, product and sum give very
    # different numbers except in degenerate cases.
    x_values = np.array([1.0, 2.0, 3.0])
    correct = joint_density(x_values, mean=2.0, std=1.0)
    individual_densities = normal_pdf(x_values, mean=2.0, std=1.0)
    wrong_sum_version = np.sum(individual_densities)
    assert not np.isclose(correct, wrong_sum_version)
    assert np.isclose(correct, np.prod(individual_densities))
