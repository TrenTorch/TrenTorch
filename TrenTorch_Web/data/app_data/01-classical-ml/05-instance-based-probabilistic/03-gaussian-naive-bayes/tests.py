"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/03-gaussian-naive-bayes/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
gaussian_nb_fit = _module.gaussian_nb_fit
gaussian_log_likelihood = _module.gaussian_log_likelihood
gaussian_nb_predict = _module.gaussian_nb_predict


def test_log_likelihood_at_standard_normal_matches_hand_computation():
    x = np.array([0.0])
    mean = np.array([0.0])
    variance = np.array([1.0])
    assert np.isclose(gaussian_log_likelihood(x, mean, variance), -0.5 * np.log(2 * np.pi))


def test_log_likelihood_peaks_at_the_mean():
    mean = np.array([3.0])
    variance = np.array([1.0])
    at_mean = gaussian_log_likelihood(np.array([3.0]), mean, variance)
    away_from_mean = gaussian_log_likelihood(np.array([5.0]), mean, variance)
    assert at_mean > away_from_mean


def test_fit_means_and_variances_match_hand_computation():
    input = np.array([[1.0], [3.0], [5.0]])  # mean=3, population var = ((2^2+0+2^2)/3)=8/3
    labels = np.array([0, 0, 0])
    model = gaussian_nb_fit(input, labels, var_smoothing=0.0)
    assert np.isclose(model["means"][0][0], 3.0)
    assert np.isclose(model["variances"][0][0], 8.0 / 3.0)


def test_var_smoothing_prevents_zero_variance():
    # Feature is exactly constant within class 0 -- without smoothing,
    # variance is 0 and the Gaussian formula would divide by zero.
    input = np.array([[5.0], [5.0], [5.0], [1.0], [9.0]])
    labels = np.array([0, 0, 0, 1, 1])
    model = gaussian_nb_fit(input, labels, var_smoothing=1e-9)
    assert model["variances"][0][0] > 0.0
    assert np.isfinite(gaussian_log_likelihood(np.array([6.0]), model["means"][0], model["variances"][0]))


def test_predict_recovers_a_clearly_separable_case():
    rng = np.random.default_rng(2)
    class0 = rng.normal(loc=-3.0, size=(30, 2))
    class1 = rng.normal(loc=3.0, size=(30, 2))
    input = np.vstack([class0, class1])
    labels = np.concatenate([np.zeros(30, dtype=int), np.ones(30, dtype=int)])
    model = gaussian_nb_fit(input, labels)
    predictions = gaussian_nb_predict(model, input)
    assert np.mean(predictions == labels) > 0.95


def test_normalization_term_is_not_dropped():
    # Directly targets a mutant that computes only -(x-mean)^2/(2*var),
    # dropping the -0.5*log(2*pi*var) normalization term entirely.
    # Right AT both means, the quadratic term is exactly 0 for both --
    # a mutant without normalization would score them identically
    # (both 0), unable to prefer either. The correct formula must
    # favor the tighter (more sharply peaked) distribution: a narrow
    # Gaussian is genuinely more probable right at its own mean than a
    # wide one is at its own mean.
    tight_mean, tight_var = np.array([0.0]), np.array([0.01])
    wide_mean, wide_var = np.array([0.0]), np.array([100.0])
    x = np.array([0.0])
    tight_score = gaussian_log_likelihood(x, tight_mean, tight_var)
    wide_score = gaussian_log_likelihood(x, wide_mean, wide_var)
    assert tight_score > wide_score


def test_matches_real_sklearn_gaussian_nb_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(5)
    #   X = rng.normal(size=(60, 3))
    #   y = (X[:, 0] + X[:, 1] > 0).astype(int)
    #   clf = GaussianNB()
    #   clf.fit(X, y)
    #   clf.predict(X)  # baked below, accuracy 0.9667 on training data
    #
    # This test needs no scikit-learn installed to run.
    input = np.array(
        [
            [-0.8019, -1.3244, -0.2484], [0.4204, 1.136, 0.1097], [-0.5526, -0.7848, 0.7487],
            [1.6348, 0.2728, -1.2333], [-0.9583, 1.6, 0.2029], [-1.7321, -0.0837, -1.1632],
            [-0.6293, -0.488, -0.7133], [0.5534, -0.0631, -0.5894], [0.4096, 0.8299, -1.643],
            [-0.2567, -0.9807, -0.1732], [-1.2894, 0.0207, -0.0379], [-0.3043, -1.0479, -0.3962],
            [-1.0913, -1.3552, 0.2248], [-1.1093, 1.1703, 0.7166], [-1.9978, 0.2721, -1.1017],
            [0.0331, 0.0436, -1.9884], [-0.2334, -0.2558, 0.962], [-1.1814, 0.738, -1.099],
            [-0.3313, -0.8405, 1.4487], [0.5682, 2.4317, 0.6419], [0.845, 0.8407, -0.6066],
            [-0.07, 1.3504, -0.3966], [0.1888, -0.0212, 0.6092], [-0.3649, -0.1524, 0.2424],
            [0.103, -0.865, 0.8958], [-1.2985, -1.2011, -1.2825], [0.967, -0.3606, -0.971],
            [-1.136, 0.4211, -1.0548], [-1.2721, 0.614, -1.1967], [-0.3224, -0.0068, -0.4453],
            [-0.0541, 1.3388, -0.5169], [-1.2593, -1.8367, -0.2048], [-0.3523, 0.2651, -0.4642],
            [-0.4786, -0.7213, -0.5198], [0.1602, -0.3804, 0.1004], [1.9012, 0.4791, -1.5761],
            [1.7335, 0.3478, -0.9414], [0.907, 0.0177, -0.6152], [-0.6335, -0.9934, 0.0481],
            [1.0688, -0.3251, 0.4208], [1.8756, -1.2146, 0.2575], [-0.3064, -1.0593, -1.0258],
            [-0.0153, 0.4339, -0.5316], [0.0544, 0.7222, 0.2966], [0.8687, 0.4614, 0.488],
            [1.8266, 0.6232, 0.1295], [0.7099, -0.9191, -0.3377], [0.7932, 0.6308, 1.5484],
            [0.0105, -1.4623, 1.9472], [1.0929, -1.0587, 1.3758], [0.0324, -1.8139, -0.4204],
            [-0.5089, 1.5908, -0.7921], [-0.2536, -0.2768, -0.379], [-0.9141, 0.2191, 1.0768],
            [0.624, -0.9275, -1.1498], [0.119, -0.7066, -0.6302], [-1.6797, 1.9505, 0.9166],
            [-0.9739, 0.9082, 1.3425], [-2.3896, -0.5489, -0.388], [0.6483, -0.1215, -0.2304],
        ]
    )
    labels = np.array(
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0,
         0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0,
         0, 1]
    )
    expected_predictions = np.array(
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0,
         0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1,
         0, 1]
    )
    model = gaussian_nb_fit(input, labels)
    predictions = gaussian_nb_predict(model, input)
    assert np.array_equal(predictions, expected_predictions)
