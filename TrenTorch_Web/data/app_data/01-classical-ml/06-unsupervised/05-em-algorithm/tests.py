"""
pytest data/app_data/01-classical-ml/06-unsupervised/05-em-algorithm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
gmm_log_likelihood = _module.gmm_log_likelihood
fit_gmm = _module.fit_gmm


def test_log_likelihood_matches_hand_computation():
    input = np.array([[0.0]])
    weights = np.array([0.5, 0.5])
    means = np.array([[0.0], [0.0]])
    variances = np.ones((2, 1))
    # both components identical: P(x|comp) is the same standard normal
    # density for both -> mixture density = that density (weights sum to 1)
    standard_normal_density_log = -0.5 * np.log(2 * np.pi)
    result = gmm_log_likelihood(input, weights, means, variances)
    assert np.isclose(result, standard_normal_density_log)


def test_log_likelihood_is_numerically_stable_for_extreme_values():
    # Without the log-sum-exp max-subtraction trick, exponentiating a
    # very negative log-probability (a point extremely far from every
    # component) underflows to exactly 0 for every component, and
    # log(0) is -inf -- a real, not hypothetical, numerical failure.
    input = np.array([[1000.0]])
    weights = np.array([0.5, 0.5])
    means = np.array([[0.0], [0.0]])
    variances = np.array([[1.0], [1.0]])
    result = gmm_log_likelihood(input, weights, means, variances)
    assert np.isfinite(result)


def test_fit_gmm_returns_expected_shapes():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(40, 3))
    result = fit_gmm(input, n_components=2, max_iter=5, seed=1)
    assert result["weights"].shape == (2,)
    assert result["means"].shape == (2, 3)
    assert result["variances"].shape == (2, 3)
    assert result["responsibilities"].shape == (40, 2)
    assert result["log_likelihood_history"].shape == (5,)


def test_log_likelihood_never_decreases_across_iterations():
    # The actual EM guarantee, checked across several random datasets
    # and initializations, not just one lucky case.
    for seed in range(4):
        rng = np.random.default_rng(seed)
        input = np.vstack(
            [rng.normal(loc=-3.0, size=(30, 2)), rng.normal(loc=3.0, size=(30, 2))]
        )
        result = fit_gmm(input, n_components=2, max_iter=15, seed=seed)
        history = result["log_likelihood_history"]
        diffs = np.diff(history)
        assert np.all(diffs >= -1e-6), f"log-likelihood decreased, seed={seed}: {history}"


def test_recovers_two_well_separated_clusters():
    rng = np.random.default_rng(2)
    cluster0 = rng.normal(loc=-5.0, scale=0.5, size=(50, 2))
    cluster1 = rng.normal(loc=5.0, scale=0.5, size=(50, 2))
    input = np.vstack([cluster0, cluster1])
    result = fit_gmm(input, n_components=2, max_iter=20, seed=3)
    sorted_means = result["means"][np.argsort(result["means"][:, 0])]
    assert np.allclose(sorted_means[0], [-5.0, -5.0], atol=0.5)
    assert np.allclose(sorted_means[1], [5.0, 5.0], atol=0.5)


def test_more_iterations_never_decreases_final_log_likelihood():
    # Running the loop longer should never leave the model in a worse
    # (lower log-likelihood) place than a shorter run reached, on the
    # same data and initialization -- a direct consequence of EM's
    # monotonic guarantee, checked end to end rather than only
    # within a single run's own history.
    rng = np.random.default_rng(6)
    input = np.vstack([rng.normal(loc=-3.0, size=(30, 2)), rng.normal(loc=3.0, size=(30, 2))])
    short_run = fit_gmm(input, n_components=2, max_iter=3, seed=2)
    long_run = fit_gmm(input, n_components=2, max_iter=15, seed=2)
    assert long_run["log_likelihood_history"][-1] >= short_run["log_likelihood_history"][-1] - 1e-6
