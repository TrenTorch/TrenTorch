"""
pytest data/app_data/07-vision/04-modern-cnn-concepts/01-batch-normalization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

batch_norm2d = load_solution(
    f"07-vision/04-modern-cnn-concepts/{Path(__file__).resolve().parent.name}"
).batch_norm2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_matches_input_shape():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(4, 3, 5, 5))
    gamma = np.ones(3)
    beta = np.zeros(3)
    out = batch_norm2d(x, gamma, beta)
    assert out.shape == x.shape


def test_02_identity_gamma_beta_gives_zero_mean_unit_variance_per_channel():
    rng = np.random.default_rng(1)
    x = rng.normal(loc=5.0, scale=3.0, size=(8, 2, 4, 4))
    gamma = np.ones(2)
    beta = np.zeros(2)
    out = batch_norm2d(x, gamma, beta)
    for c in range(2):
        assert abs(out[:, c].mean()) < 1e-6
        assert abs(out[:, c].std() - 1.0) < 1e-3


# --- Shape / general-case coverage -----------------------------------


def test_03_gamma_beta_rescale_the_normalized_output():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(6, 3, 4, 4))
    gamma = np.array([2.0, 0.5, 3.0])
    beta = np.array([1.0, -1.0, 0.0])
    out = batch_norm2d(x, gamma, beta)
    for c in range(3):
        assert abs(out[:, c].mean() - beta[c]) < 1e-3
        assert abs(out[:, c].std() - abs(gamma[c])) < 1e-2


def test_04_each_channel_normalized_independently():
    rng = np.random.default_rng(3)
    x = np.zeros((2, 2, 3, 3))
    x[:, 0] = rng.normal(loc=100.0, scale=1.0, size=(2, 3, 3))
    x[:, 1] = rng.normal(loc=-50.0, scale=10.0, size=(2, 3, 3))
    gamma = np.ones(2)
    beta = np.zeros(2)
    out = batch_norm2d(x, gamma, beta)
    assert abs(out[:, 0].mean()) < 1e-6
    assert abs(out[:, 1].mean()) < 1e-6


# --- Edge cases ---------------------------------------------------------


def test_05_single_channel_single_sample_does_not_crash():
    x = np.array([[[[1.0, 2.0], [3.0, 4.0]]]])
    gamma = np.array([1.0])
    beta = np.array([0.0])
    out = batch_norm2d(x, gamma, beta)
    assert out.shape == (1, 1, 2, 2)


def test_06_constant_channel_relies_on_eps_to_avoid_divide_by_zero():
    x = np.full((3, 1, 2, 2), 7.0)
    gamma = np.array([1.0])
    beta = np.array([0.0])
    out = batch_norm2d(x, gamma, beta, eps=1e-5)
    assert np.all(np.isfinite(out))
    assert np.allclose(out, 0.0, atol=1e-2)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(3, 2, 4, 4))
    gamma = rng.normal(size=2)
    beta = rng.normal(size=2)
    x_copy, gamma_copy, beta_copy = x.copy(), gamma.copy(), beta.copy()
    batch_norm2d(x, gamma, beta)
    assert np.array_equal(x, x_copy)
    assert np.array_equal(gamma, gamma_copy)
    assert np.array_equal(beta, beta_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_batch_norm_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.tensor(...)  # shape (2, 3, 4, 4)
    #   gamma = torch.tensor([1.5, -0.5, 2.0])
    #   beta = torch.tensor([0.1, 0.2, -0.3])
    #   out = torch.nn.functional.batch_norm(
    #       x, running_mean=None, running_var=None,
    #       weight=gamma, bias=beta, training=True, eps=1e-5,
    #   )
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [
                [
                    [-0.5108, 1.0283, -0.3532, 0.1230],
                    [-0.1816, -1.4972, 0.1421, -0.5243],
                    [-0.2487, -0.5252, 2.8922, -0.5947],
                    [1.3118, 0.3522, -1.3151, -0.0080],
                ],
                [
                    [0.2479, 1.5727, -1.6395, -1.5925],
                    [-0.1546, -1.0964, 1.3666, 0.6893],
                    [-0.3935, 0.6171, 0.7528, 0.6023],
                    [2.0175, -1.1686, -1.3242, 1.1267],
                ],
                [
                    [-0.2255, 0.5218, -2.0598, 0.1383],
                    [0.4962, -0.6053, -0.8007, 0.1587],
                    [0.7128, -0.7438, 0.2801, 0.3735],
                    [2.9951, -0.2569, -0.6838, 1.0621],
                ],
            ],
            [
                [
                    [-0.0205, -0.6305, 0.5485, -1.5885],
                    [0.5281, 0.8964, 0.9975, -0.2156],
                    [1.3266, -0.1086, -1.0265, 0.0436],
                    [-0.9724, 0.2803, 0.5700, 1.4841],
                ],
                [
                    [-1.4556, 0.5582, -0.5062, 0.4655],
                    [-0.8604, -0.8528, 2.0163, 0.1693],
                    [-0.9030, -1.7102, -0.1362, 1.4530],
                    [0.5620, 1.1591, -1.7210, -0.0590],
                ],
                [
                    [0.8455, -0.1304, -0.3232, -0.7119],
                    [-0.2273, -2.5322, 0.3415, 1.1048],
                    [0.0957, -0.0299, 0.8553, -0.0249],
                    [2.2696, 0.8602, -1.6499, -0.0435],
                ],
            ],
        ]
    )
    gamma = np.array([1.5, -0.5, 2.0])
    beta = np.array([0.1, 0.2, -0.3])
    expected_first_row = np.array([-0.8257, 1.6322, -0.5739, 0.1865])
    expected_last_sample_last_channel_last_row = np.array([3.8498, 1.1975, -3.5261, -0.5031])

    out = batch_norm2d(x, gamma, beta, eps=1e-5)
    assert np.allclose(out[0, 0, 0], expected_first_row, atol=1e-2)
    assert np.allclose(out[1, 2, 3], expected_last_sample_last_channel_last_row, atol=1e-2)
