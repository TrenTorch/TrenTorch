"""
pytest data/app_data/07-vision/02-pooling/03-adaptive-average-pooling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

adaptive_avg_pool2d = load_solution(
    f"07-vision/02-pooling/{Path(__file__).resolve().parent.name}"
).adaptive_avg_pool2d


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_global_pool_matches_full_channel_mean():
    image = np.random.default_rng(0).normal(size=(3, 5, 5))
    out = adaptive_avg_pool2d(image, output_size=(1, 1))
    assert out.shape == (3, 1, 1)
    assert np.allclose(out[:, 0, 0], image.mean(axis=(1, 2)))


def test_02_output_size_equal_to_input_size_is_identity():
    image = np.random.default_rng(1).normal(size=(2, 4, 4))
    out = adaptive_avg_pool2d(image, output_size=(4, 4))
    assert np.allclose(out, image)


# --- Shape / general-case coverage -----------------------------------


def test_03_evenly_dividing_output_size_matches_plain_average_pooling():
    # When H is evenly divisible by out_h (and W by out_w), adaptive
    # pooling's variable windows all come out the same fixed size --
    # must match plain fixed-window average pooling exactly.
    avg_pool2d = load_solution("07-vision/02-pooling/02-average-pooling").avg_pool2d
    image = np.random.default_rng(2).normal(size=(2, 6, 6))
    adaptive_out = adaptive_avg_pool2d(image, output_size=(3, 3))
    fixed_out = avg_pool2d(image, kernel_size=2)
    assert np.allclose(adaptive_out, fixed_out)


def test_04_non_dividing_output_size_still_produces_correct_shape():
    image = np.random.default_rng(3).normal(size=(2, 7, 5))
    out = adaptive_avg_pool2d(image, output_size=(3, 2))
    assert out.shape == (2, 3, 2)


# --- Edge cases ---------------------------------------------------------


def test_05_output_size_1x1_uses_every_pixel_exactly_once():
    # Sum of all output-cell means, weighted by cell size, must recover
    # the true global mean regardless of how unevenly the regions split.
    image = np.random.default_rng(4).normal(size=(1, 7, 7))
    out = adaptive_avg_pool2d(image, output_size=(1, 1))
    assert np.isclose(out[0, 0, 0], image.mean())


def test_06_single_channel_image():
    image = np.random.default_rng(5).normal(size=(1, 5, 5))
    out = adaptive_avg_pool2d(image, output_size=(2, 2))
    assert out.shape == (1, 2, 2)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_input():
    image = np.random.default_rng(6).normal(size=(2, 6, 6))
    image_copy = image.copy()
    adaptive_avg_pool2d(image, output_size=(2, 2))
    assert np.array_equal(image, image_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_adaptive_avg_pool2d_on_baked_reference_cases():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(6)
    #   image = torch.randn(2, 5, 5)
    #   out_11 = torch.nn.functional.adaptive_avg_pool2d(image[None], output_size=(1, 1))[0]
    #   out_22 = torch.nn.functional.adaptive_avg_pool2d(image[None], output_size=(2, 2))[0]
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [-1.2113, 0.6304, -1.4713, -1.3352, -0.4897],
                [0.1317, 0.3295, 0.3264, -0.4806, 1.1032],
                [2.5485, 0.3006, -0.5432, -1.0841, 1.4612],
                [-1.6279, -1.4801, -1.0631, 0.363, 0.3995],
                [0.1457, -0.7345, -0.9873, 1.8512, -1.3437],
            ],
            [
                [0.8535, 0.8811, -0.6522, 0.581, 0.3561],
                [0.016, 0.4019, 1.9538, -0.446, -1.1083],
                [-0.6452, -1.7871, 0.695, -0.5825, -0.1926],
                [-0.6734, -1.2061, -0.2808, 0.8701, -1.7344],
                [-1.4347, -0.0628, -0.5595, 0.2804, -1.254],
            ],
        ]
    )
    expected_11 = np.array([[[-0.170444]], [[-0.229228]]])
    expected_22 = np.array(
        [
            [[0.1157, -0.279256], [-0.382367, -0.105167]],
            [[0.190756, 0.067144], [-0.661622, -0.306478]],
        ]
    )
    out_11 = adaptive_avg_pool2d(image, output_size=(1, 1))
    out_22 = adaptive_avg_pool2d(image, output_size=(2, 2))
    assert np.allclose(out_11, expected_11, atol=1e-3)
    assert np.allclose(out_22, expected_22, atol=1e-3)
