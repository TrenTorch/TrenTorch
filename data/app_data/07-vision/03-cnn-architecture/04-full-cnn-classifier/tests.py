"""
pytest data/app_data/07-vision/03-cnn-architecture/04-full-cnn-classifier/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

full_cnn_classifier = load_solution(
    f"07-vision/03-cnn-architecture/{Path(__file__).resolve().parent.name}"
).full_cnn_classifier
stack_cnn_blocks = load_solution("07-vision/03-cnn-architecture/03-stack-multiple-blocks").stack_cnn_blocks
flatten = load_solution("07-vision/03-cnn-architecture/01-flatten").flatten
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_manually_assembled_pipeline_no_labels():
    rng = np.random.default_rng(0)
    images = rng.normal(size=(3, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    fc_weight = rng.normal(size=(4, 8))
    fc_bias = rng.normal(size=4)

    probs = full_cnn_classifier(images, [kernel], fc_weight, fc_bias)

    manual_flat = np.stack([flatten(stack_cnn_blocks(img, [kernel])) for img in images])
    manual_probs = softmax(linear(manual_flat, fc_weight, fc_bias))
    assert np.allclose(probs, manual_probs)


def test_02_probabilities_sum_to_one_per_sample():
    rng = np.random.default_rng(1)
    images = rng.normal(size=(4, 1, 8, 8))
    kernel = rng.normal(size=(3, 1, 3, 3))
    fc_weight = rng.normal(size=(5, 27))
    fc_bias = rng.normal(size=5)
    probs = full_cnn_classifier(images, [kernel], fc_weight, fc_bias)
    assert probs.shape == (4, 5)
    assert np.allclose(probs.sum(axis=1), 1.0)


# --- Shape / general-case coverage -----------------------------------


def test_03_multi_channel_input_and_multiple_blocks():
    rng = np.random.default_rng(2)
    images = rng.normal(size=(2, 3, 12, 12))
    k1 = rng.normal(size=(4, 3, 3, 3))
    k2 = rng.normal(size=(2, 4, 3, 3))
    fc_weight = rng.normal(size=(3, 2))
    fc_bias = rng.normal(size=3)
    probs = full_cnn_classifier(images, [k1, k2], fc_weight, fc_bias)
    assert probs.shape == (2, 3)


# --- Parameter handling -------------------------------------------------


def test_04_labels_given_also_returns_a_scalar_loss():
    rng = np.random.default_rng(3)
    images = rng.normal(size=(3, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    fc_weight = rng.normal(size=(2, 8))
    fc_bias = rng.normal(size=2)
    labels = np.array([0, 1, 0])
    probs, loss = full_cnn_classifier(images, [kernel], fc_weight, fc_bias, labels=labels)
    assert probs.shape == (3, 2)
    assert isinstance(loss, float)
    assert loss > 0


def test_05_no_labels_returns_only_probs_not_a_tuple():
    rng = np.random.default_rng(4)
    images = rng.normal(size=(2, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    fc_weight = rng.normal(size=(2, 8))
    fc_bias = rng.normal(size=2)
    result = full_cnn_classifier(images, [kernel], fc_weight, fc_bias)
    assert isinstance(result, np.ndarray)


# --- Edge cases ---------------------------------------------------------


def test_06_single_image_batch():
    rng = np.random.default_rng(5)
    images = rng.normal(size=(1, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    fc_weight = rng.normal(size=(3, 8))
    fc_bias = rng.normal(size=3)
    probs = full_cnn_classifier(images, [kernel], fc_weight, fc_bias)
    assert probs.shape == (1, 3)


def test_07_perfectly_confident_correct_predictions_give_near_zero_loss():
    # Construct fc weights that make the model extremely confident and
    # correct for every sample -- loss should be very small.
    rng = np.random.default_rng(6)
    images = rng.normal(size=(2, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    flat_dim = flatten(stack_cnn_blocks(images[0], [kernel])).shape[0]
    labels = np.array([0, 1])
    # Huge positive weight row for the true class, huge negative for the other.
    fc_weight = np.zeros((2, flat_dim))
    fc_bias = np.array([1000.0, -1000.0])  # class 0 always wins regardless of features
    fc_bias_flipped = np.array([-1000.0, 1000.0])
    probs0, loss0 = full_cnn_classifier(images[:1], [kernel], fc_weight, fc_bias, labels=labels[:1])
    probs1, loss1 = full_cnn_classifier(images[1:], [kernel], fc_weight, fc_bias_flipped, labels=labels[1:])
    assert loss0 < 1e-6
    assert loss1 < 1e-6


# --- Array hygiene ------------------------------------------------------


def test_08_does_not_mutate_its_inputs():
    rng = np.random.default_rng(7)
    images = rng.normal(size=(2, 1, 6, 6))
    kernel = rng.normal(size=(2, 1, 3, 3))
    fc_weight = rng.normal(size=(3, 8))
    fc_bias = rng.normal(size=3)
    images_copy, kernel_copy = images.copy(), kernel.copy()
    fc_weight_copy, fc_bias_copy = fc_weight.copy(), fc_bias.copy()
    full_cnn_classifier(images, [kernel], fc_weight, fc_bias)
    assert np.array_equal(images, images_copy)
    assert np.array_equal(kernel, kernel_copy)
    assert np.array_equal(fc_weight, fc_weight_copy)
    assert np.array_equal(fc_bias, fc_bias_copy)


# --- Independent correctness oracle -----------------------------------


def test_09_matches_real_pytorch_conv_relu_pool_flatten_linear_softmax_nll_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(10)
    #   images = torch.randn(2, 1, 6, 6)
    #   kernel = torch.randn(2, 1, 3, 3)
    #   fc_weight, fc_bias = torch.randn(3, 8), torch.randn(3)
    #   labels = torch.tensor([0, 2])
    #   outs = []
    #   for n in range(2):
    #       c = torch.nn.functional.conv2d(images[n][None], kernel)[0]
    #       a = torch.nn.functional.relu(c)
    #       p = torch.nn.functional.max_pool2d(a[None], kernel_size=2)[0]
    #       outs.append(torch.flatten(p))
    #   flat = torch.stack(outs)
    #   logits = torch.nn.functional.linear(flat, fc_weight, fc_bias)
    #   probs = torch.nn.functional.softmax(logits, dim=1)
    #   loss = torch.nn.functional.nll_loss(torch.log(probs), labels)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    images = np.array(
        [
            [
                [
                    [-0.8173, -0.5556, -0.8267, -1.297, -0.1974, -0.9643],
                    [-0.5133, 2.6278, -0.7465, 1.0051, -0.2568, 0.4765],
                    [-0.6652, -0.3627, -1.4504, -0.2496, 0.8298, 1.1209],
                    [0.9999, 1.1167, 1.0763, -0.0662, 0.1315, 0.1681],
                    [0.0562, 0.2456, 0.9535, 0.3553, 0.2121, -0.3378],
                    [-0.3536, -0.2729, 1.329, 1.1974, -1.2645, -0.4344],
                ]
            ],
            [
                [
                    [-2.1806, -1.1094, -2.041, 0.0334, -1.0805, -0.8832],
                    [0.9741, 0.5632, -1.1151, 0.149, -1.0923, -1.4551],
                    [-0.4811, -1.0823, 0.3177, 2.747, 0.369, 1.3373],
                    [-0.918, -0.9615, 0.2609, -0.6728, -0.0436, -0.9607],
                    [0.0948, -0.6164, -0.5421, 0.7038, 0.5735, 1.3399],
                    [-0.5526, -0.1727, -0.0442, 1.2828, 0.711, -0.047],
                ]
            ],
        ]
    )
    kernel = np.array(
        [
            [[[-0.1053, -0.4767, 0.6027], [-0.5403, -0.8977, -0.0979], [-0.9668, 0.8147, 1.6947]]],
            [[[-0.3067, -1.4181, 1.4855], [0.0709, 1.06, 1.2998], [-1.3373, -0.8349, -0.5937]]],
        ]
    )
    fc_weight = np.array(
        [
            [-0.4786, -0.8705, -1.42, -0.8545, 0.1413, 0.6676, -0.1746, 1.1172],
            [-1.8333, 0.7659, 0.3923, 0.4299, 0.1912, -1.17, 0.7612, 0.9091],
            [1.5246, 0.5246, -1.4257, -0.63, -0.1743, -0.5054, 0.1346, 0.6619],
        ]
    )
    fc_bias = np.array([-0.8426, -0.4609, 0.6346])
    labels = np.array([0, 2])
    expected_probs = np.array(
        [
            [0.03409, 0.031886, 0.934023],
            [0.0, 0.000001, 0.999999],
        ]
    )
    expected_loss = 1.6894

    probs, loss = full_cnn_classifier(images, [kernel], fc_weight, fc_bias, labels=labels)
    assert np.allclose(probs, expected_probs, atol=1e-3)
    assert abs(loss - expected_loss) < 1e-2
