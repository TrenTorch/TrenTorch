"""
pytest data/app_data/07-vision/03-cnn-architecture/02-one-cnn-block/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cnn_block = load_solution(f"07-vision/03-cnn-architecture/{Path(__file__).resolve().parent.name}").cnn_block
conv2d_multi_filter = load_solution(
    "07-vision/01-convolutions/05-multiple-output-filters"
).conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward
max_pool2d = load_solution("07-vision/02-pooling/01-max-pooling").max_pool2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_manual_conv_relu_pool_chain():
    image = np.random.default_rng(0).normal(size=(2, 6, 6))
    kernel = np.random.default_rng(1).normal(size=(3, 2, 3, 3))
    out = cnn_block(image, kernel, pool_size=2)
    expected = max_pool2d(relu_forward(conv2d_multi_filter(image, kernel)), kernel_size=2)
    assert np.allclose(out, expected)


def test_02_output_shape():
    image = np.random.default_rng(2).normal(size=(1, 8, 8))
    kernel = np.random.default_rng(3).normal(size=(4, 1, 3, 3))
    out = cnn_block(image, kernel, pool_size=2)
    assert out.shape == (4, 3, 3)


# --- Shape / general-case coverage -----------------------------------


def test_03_different_pool_size():
    image = np.random.default_rng(4).normal(size=(1, 8, 8))
    kernel = np.random.default_rng(5).normal(size=(2, 1, 3, 3))
    out = cnn_block(image, kernel, pool_size=3)
    assert out.shape == (2, 2, 2)


# --- Edge cases ---------------------------------------------------------


def test_04_relu_zeroes_an_all_negative_result():
    # A block whose conv output is entirely negative must come out
    # entirely zero -- direct evidence ReLU actually ran somewhere in
    # the pipeline, not skipped.
    image = np.zeros((1, 5, 5))
    kernel = np.ones((1, 1, 3, 3))
    out = cnn_block(image, kernel, pool_size=2)
    assert np.allclose(out, 0.0)


def test_05_negative_conv_output_never_survives_into_the_final_result():
    # Every value feeding this block's conv is negative, so every conv
    # output is negative too (a negative times a positive kernel) --
    # after ReLU every value must be exactly 0, and max-pooling zeros
    # stays 0. A missing ReLU call would let the (negative) max through
    # unchanged instead.
    image = -np.abs(np.random.default_rng(9).normal(size=(2, 6, 6)))
    kernel = np.abs(np.random.default_rng(10).normal(size=(3, 2, 3, 3)))
    out = cnn_block(image, kernel, pool_size=2)
    assert np.allclose(out, 0.0)


# --- Array hygiene ------------------------------------------------------


def test_06_does_not_mutate_its_inputs():
    image = np.random.default_rng(6).normal(size=(2, 6, 6))
    kernel = np.random.default_rng(7).normal(size=(2, 2, 3, 3))
    image_copy, kernel_copy = image.copy(), kernel.copy()
    cnn_block(image, kernel)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(kernel, kernel_copy)


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_conv_relu_maxpool_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(8)
    #   image = torch.randn(2, 6, 6)
    #   kernel = torch.randn(3, 2, 3, 3)
    #   conv = torch.nn.functional.conv2d(image[None], kernel)[0]
    #   act = torch.nn.functional.relu(conv)
    #   out = torch.nn.functional.max_pool2d(act[None], kernel_size=2)[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [-1.1892, 1.3932, 2.1059, -0.3546, 0.371, 1.0957],
                [2.1414, 0.1317, -0.6388, 1.3384, -1.1908, -0.7601],
                [1.1422, 0.9312, 0.0262, -0.1051, 0.4414, 0.659],
                [-0.7585, -0.6001, -0.3948, -1.1318, 0.4173, -0.5685],
                [-1.7526, 0.392, 0.8295, 0.0908, -0.4689, 0.3834],
                [0.2277, 1.2106, 0.0459, 0.2513, -0.6428, 0.9222],
            ],
            [
                [-0.129, 1.6694, -0.1584, 0.141, -0.0657, -1.0195],
                [-0.5657, 2.2933, -1.0794, -0.4487, 0.0349, -1.0178],
                [-0.5491, -1.4182, 1.0285, 1.2822, -1.0551, 1.4991],
                [1.0125, -0.0757, -1.3633, 0.4639, -0.5726, -0.4216],
                [-0.19, 0.5473, 0.3417, -1.4044, -0.8025, 0.2755],
                [-0.1204, 0.7553, -0.3312, -0.6896, 0.9322, 0.6352],
            ],
        ]
    )
    kernel = np.array(
        [
            [
                [[1.3048, -0.4483, -0.1747], [0.7417, 0.1927, -2.1321], [-1.1529, 1.4764, -0.3215]],
                [[1.8455, 0.7988, -2.4385], [0.3622, -0.3619, -0.1919], [1.4459, 0.2265, -1.6831]],
            ],
            [
                [[-1.3731, -1.0252, -0.762], [0.0699, 1.4146, 0.2701], [0.4555, 1.0285, -0.4525]],
                [[0.5804, 0.0506, -0.0316], [-0.6328, -0.52, -0.1599], [-1.9666, -0.8256, -1.3963]],
            ],
            [
                [[-0.6051, -0.7665, -0.4348], [-0.706, 0.7242, -0.3099], [-0.3106, -1.1329, -1.4141]],
                [[0.4129, 1.1991, 0.8896], [-0.791, 0.5105, -1.1804], [1.6574, 0.0375, 0.0816]],
            ],
        ]
    )
    expected = np.array(
        [
            [[11.211308, 8.136438], [3.219894, 4.40215]],
            [[1.435332, 0.348396], [4.425268, 2.687511]],
            [[1.830902, 2.40752], [1.99956, 2.967707]],
        ]
    )
    out = cnn_block(image, kernel, pool_size=2)
    assert np.allclose(out, expected, atol=1e-3)
