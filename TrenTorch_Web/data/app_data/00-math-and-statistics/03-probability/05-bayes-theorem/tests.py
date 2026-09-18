"""
pytest data/app_data/00-math-and-statistics/03-probability/05-bayes-theorem/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
bayes_theorem = _module.bayes_theorem
posterior_binary = _module.posterior_binary


def test_bayes_theorem_matches_hand_computation():
    # prior=0.5, likelihood=0.8, evidence=0.4 -> (0.8*0.5)/0.4 = 1.0
    assert np.isclose(bayes_theorem(0.5, 0.8, 0.4), 1.0)


def test_bayes_theorem_with_certain_evidence_reduces_to_likelihood_times_prior():
    assert np.isclose(bayes_theorem(0.3, 0.6, 1.0), 0.18)


def test_posterior_binary_classic_disease_test_example():
    # Prevalence 1%, true positive rate 99%, false positive rate 5%.
    # Known counterintuitive result: posterior ~= 16.67%, not 99%.
    result = posterior_binary(prior_h=0.01, likelihood_e_given_h=0.99, likelihood_e_given_not_h=0.05)
    assert np.isclose(result, 0.99 * 0.01 / (0.99 * 0.01 + 0.05 * 0.99), atol=1e-6)
    assert result < 0.2


def test_posterior_binary_with_a_perfectly_reliable_test():
    # If the test never gives false positives, a positive result implies
    # certainty (posterior = 1.0), regardless of how rare the disease is.
    result = posterior_binary(prior_h=0.001, likelihood_e_given_h=1.0, likelihood_e_given_not_h=0.0)
    assert np.isclose(result, 1.0)


def test_posterior_binary_with_uninformative_evidence_does_not_change_belief():
    # If the evidence is equally likely whether H is true or false, it
    # carries no information, the posterior should equal the prior.
    result = posterior_binary(prior_h=0.3, likelihood_e_given_h=0.5, likelihood_e_given_not_h=0.5)
    assert np.isclose(result, 0.3)


def test_posterior_binary_increases_with_more_reliable_positive_evidence():
    weak_test = posterior_binary(prior_h=0.1, likelihood_e_given_h=0.6, likelihood_e_given_not_h=0.4)
    strong_test = posterior_binary(prior_h=0.1, likelihood_e_given_h=0.95, likelihood_e_given_not_h=0.05)
    assert strong_test > weak_test


def test_posterior_binary_computes_its_own_evidence_not_a_wrong_shortcut():
    # Directly targets a mutant that treats evidence as simply
    # likelihood_e_given_h (ignoring the "or H is false" branch of the
    # weighted sum entirely). For the disease example, using
    # evidence=0.99 directly (instead of the correctly weighted 0.0594)
    # would give posterior = 0.01, not the correct ~0.1667.
    result = posterior_binary(prior_h=0.01, likelihood_e_given_h=0.99, likelihood_e_given_not_h=0.05)
    assert not np.isclose(result, 0.01, atol=1e-3)
    assert np.isclose(result, 0.16666667, atol=1e-6)
