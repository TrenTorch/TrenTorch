"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/05-gaussian-processes/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
rbf_kernel = _module.rbf_kernel
gp_predict = _module.gp_predict


def test_rbf_kernel_of_identical_points_equals_variance():
    x = np.array([[1.0, 2.0]])
    result = rbf_kernel(x, x, length_scale=1.0, variance=3.0)
    assert np.isclose(result[0, 0], 3.0)


def test_rbf_kernel_matches_hand_computation():
    a = np.array([[0.0]])
    b = np.array([[2.0]])
    # variance=1, length_scale=1: exp(-0.5 * 4 / 1) = exp(-2)
    result = rbf_kernel(a, b, length_scale=1.0, variance=1.0)
    assert np.isclose(result[0, 0], np.exp(-2.0))


def test_rbf_kernel_decreases_with_distance():
    center = np.array([[0.0]])
    near = np.array([[1.0]])
    far = np.array([[5.0]])
    k_near = rbf_kernel(center, near, length_scale=1.0, variance=1.0)[0, 0]
    k_far = rbf_kernel(center, far, length_scale=1.0, variance=1.0)[0, 0]
    assert k_near > k_far


def test_gp_predict_nearly_interpolates_training_points_with_tiny_noise():
    input_train = np.array([[0.0], [1.0], [2.0], [3.0]])
    targets_train = np.array([0.0, 1.0, 0.0, -1.0])
    mean, variance = gp_predict(
        input_train, targets_train, input_train, length_scale=1.0, variance=1.0, noise=1e-6
    )
    assert np.allclose(mean, targets_train, atol=1e-3)
    assert np.all(variance < 1e-2)


def test_variance_grows_far_from_training_data():
    input_train = np.array([[0.0], [1.0], [2.0]])
    targets_train = np.array([0.0, 1.0, 0.0])
    input_test = np.array([[1.0], [50.0]])  # one near training data, one far away
    _, variance = gp_predict(
        input_train, targets_train, input_test, length_scale=1.0, variance=1.0, noise=0.01
    )
    assert variance[1] > variance[0]


def test_variance_output_is_never_negative():
    rng = np.random.default_rng(0)
    input_train = rng.normal(size=(10, 2))
    targets_train = rng.normal(size=10)
    input_test = rng.normal(size=(5, 2))
    _, variance = gp_predict(
        input_train, targets_train, input_test, length_scale=0.5, variance=2.0, noise=0.05
    )
    assert np.all(variance >= 0.0)


def test_noise_term_is_actually_added_to_the_training_diagonal():
    # Directly targets a mutant that forgets `noise * np.eye(n_train)`:
    # with duplicate training points (a singular kernel matrix without
    # the noise regularizer), an implementation with no noise term on
    # the diagonal will crash inverting the matrix, or (with a pinv
    # fallback) badly overfit and produce an unstable prediction at the
    # duplicated location. With the noise term present, this is
    # well-conditioned and stable.
    input_train = np.array([[1.0], [1.0], [1.0], [3.0]])  # three exact duplicates
    targets_train = np.array([0.5, 0.5, 0.5, 2.0])
    mean, variance = gp_predict(
        input_train, targets_train, np.array([[1.0]]), length_scale=1.0, variance=1.0, noise=0.1
    )
    assert np.isfinite(mean[0])
    assert np.isclose(mean[0], 0.5, atol=0.1)


def test_matches_real_sklearn_gaussian_process_regressor_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   kernel = ConstantKernel(1.0, constant_value_bounds='fixed') \
    #            * RBF(1.0, length_scale_bounds='fixed')
    #   gpr = GaussianProcessRegressor(kernel=kernel, alpha=0.01, optimizer=None)
    #   gpr.fit(X_train, y_train)
    #   mean, std = gpr.predict(X_test, return_std=True)
    #
    # This test needs no scikit-learn installed to run.
    input_train = np.array(
        [
            [-2.5149838566263867], [-1.9528331031358293], [-0.7410804937363649],
            [0.0679653168861698], [0.6441349919701778], [1.8114072419148437],
            [2.658336633434206], [2.857462234246225],
        ]
    )
    targets_train = np.array(
        [-0.6668105794087649, -0.9158186339561584, -0.6633163825839182, 0.14669430535479314,
         0.6163392367887893, 0.9967199105573544, 0.3900089617242623, 0.39295929812531516]
    )
    input_test = np.array([[-2.5], [0.0], [1.5], [2.9]])
    expected_mean = np.array([-0.67196668, 0.05988649, 1.03118065, 0.3333309])
    expected_variance = np.array([0.00905563, 0.00889264, 0.01522489, 0.0096563])

    mean, variance = gp_predict(
        input_train, targets_train, input_test, length_scale=1.0, variance=1.0, noise=0.01
    )
    assert np.allclose(mean, expected_mean, atol=1e-5)
    assert np.allclose(variance, expected_variance, atol=1e-5)
