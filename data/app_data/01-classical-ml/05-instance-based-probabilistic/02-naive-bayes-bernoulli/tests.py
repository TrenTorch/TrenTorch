"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/02-naive-bayes-bernoulli/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
bernoulli_nb_fit = _module.bernoulli_nb_fit
bernoulli_log_likelihood = _module.bernoulli_log_likelihood
bernoulli_nb_predict = _module.bernoulli_nb_predict


def test_log_likelihood_matches_hand_computation():
    x = np.array([1.0, 0.0])
    feature_probs = np.array([0.8, 0.3])
    # log(0.8) + log(1-0.3) = log(0.8) + log(0.7)
    expected = np.log(0.8) + np.log(0.7)
    assert np.isclose(bernoulli_log_likelihood(x, feature_probs), expected)


def test_log_likelihood_of_all_zero_features():
    x = np.array([0.0, 0.0, 0.0])
    feature_probs = np.array([0.5, 0.5, 0.5])
    assert np.isclose(bernoulli_log_likelihood(x, feature_probs), 3 * np.log(0.5))


def test_fit_priors_match_class_frequencies():
    input = np.array([[1, 0], [1, 1], [0, 0], [0, 0]])
    labels = np.array([0, 0, 1, 1])
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    assert np.isclose(model["log_priors"][0], np.log(0.5))
    assert np.isclose(model["log_priors"][1], np.log(0.5))


def test_fit_feature_probs_use_laplace_smoothing():
    # class 0 has 2 samples, feature 0 present in both -> (2+1)/(2+2)=0.75, not 2/2=1.0
    input = np.array([[1, 0], [1, 1], [0, 0], [0, 0]])
    labels = np.array([0, 0, 1, 1])
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    assert np.isclose(model["feature_probs"][0][0], 0.75)


def test_smoothing_avoids_zero_probability_for_an_always_absent_feature():
    # feature 1 is always 0 within class 0 -- without smoothing, p=0
    # exactly, and log(0) is -inf, which would make a query with
    # feature 1 = 1 permanently impossible under class 0. With alpha=1,
    # p must be strictly positive.
    input = np.array([[1, 0], [1, 0], [1, 0], [0, 1]])
    labels = np.array([0, 0, 0, 1])
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    assert model["feature_probs"][0][1] > 0.0
    assert np.isfinite(bernoulli_log_likelihood(np.array([1.0, 1.0]), model["feature_probs"][0]))


def test_predict_recovers_a_clearly_separable_case():
    rng = np.random.default_rng(0)
    input = (rng.random((60, 4)) > 0.5).astype(int)
    labels = input[:, 0]  # class is literally feature 0's value
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    predictions = bernoulli_nb_predict(model, input)
    assert np.mean(predictions == labels) > 0.9


def test_smoothing_denominator_is_two_alpha_not_alpha():
    # Directly targets a mutant that adds alpha to the denominator
    # instead of 2*alpha: with alpha=1, class_count=2, feature always
    # present, correct is (2+1)/(2+2)=0.75; the mutant would give
    # (2+1)/(2+1)=1.0, a different, distinguishable value.
    input = np.array([[1], [1]])
    labels = np.array([0, 0])
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    assert np.isclose(model["feature_probs"][0][0], 0.75)


def test_matches_real_sklearn_bernoulli_nb_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(3)
    #   X = (rng.random((40, 5)) > 0.5).astype(int)
    #   y = (X[:, 0] | X[:, 1]).astype(int)
    #   clf = BernoulliNB(alpha=1.0)
    #   clf.fit(X, y)
    #   clf.predict(X)  # matches y exactly, accuracy 1.0
    #
    # This test needs no scikit-learn installed to run.
    input = np.array(
        [
            [0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1], [0, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 1, 1, 1, 0], [1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1], [0, 1, 0, 1, 0], [0, 1, 1, 1, 1], [0, 1, 0, 1, 1], [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [1, 0, 1, 1, 0], [1, 0, 1, 1, 1], [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 1, 0, 0, 1], [0, 1, 0, 0, 1], [0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [0, 1, 0, 1, 1], [1, 0, 0, 0, 1], [0, 1, 0, 0, 1],
            [0, 0, 1, 0, 1], [1, 0, 0, 1, 1], [1, 0, 0, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 1, 1],
        ]
    )
    labels = np.array(
        [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
         0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    )
    model = bernoulli_nb_fit(input, labels, alpha=1.0)
    predictions = bernoulli_nb_predict(model, input)
    assert np.array_equal(predictions, labels)
