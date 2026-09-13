"""
pytest data/app_data/07-vision/06-vision-transformer/01-patchify/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

patchify = load_solution(f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}").patchify


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape():
    rng = np.random.default_rng(0)
    image = rng.normal(size=(3, 8, 8))
    out = patchify(image, patch_size=4)
    assert out.shape == (4, 3 * 4 * 4)  # (8/4)^2 = 4 patches, each 3*4*4=48 long


def test_02_single_patch_covering_the_whole_image():
    image = np.arange(2 * 4 * 4, dtype=float).reshape(2, 4, 4)
    out = patchify(image, patch_size=4)
    assert out.shape == (1, 32)
    assert np.array_equal(out[0], image.reshape(-1))


# --- Shape / general-case coverage -----------------------------------


def test_03_patch_content_matches_the_correct_image_region():
    image = np.zeros((1, 4, 4))
    image[0, 0:2, 0:2] = 1.0  # top-left patch
    image[0, 0:2, 2:4] = 2.0  # top-right patch
    image[0, 2:4, 0:2] = 3.0  # bottom-left patch
    image[0, 2:4, 2:4] = 4.0  # bottom-right patch
    out = patchify(image, patch_size=2)
    assert np.allclose(out[0], 1.0)
    assert np.allclose(out[1], 2.0)
    assert np.allclose(out[2], 3.0)
    assert np.allclose(out[3], 4.0)


def test_04_patch_order_is_row_major_left_to_right_then_top_to_bottom():
    image = np.zeros((1, 6, 6))
    for row in range(3):
        for col in range(3):
            image[0, row * 2 : row * 2 + 2, col * 2 : col * 2 + 2] = row * 3 + col
    out = patchify(image, patch_size=2)
    for idx in range(9):
        assert np.allclose(out[idx], float(idx))


# --- Parameter handling -------------------------------------------------


def test_05_multi_channel_patches_keep_all_channels_together_per_patch():
    rng = np.random.default_rng(1)
    image = rng.normal(size=(3, 4, 4))
    out = patchify(image, patch_size=2)
    assert out.shape == (4, 3 * 2 * 2)
    manual_patch0 = image[:, 0:2, 0:2].reshape(-1)
    assert np.allclose(out[0], manual_patch0)


# --- Edge cases ---------------------------------------------------------


def test_06_smallest_possible_patch_size_of_1():
    image = np.arange(1 * 2 * 2, dtype=float).reshape(1, 2, 2)
    out = patchify(image, patch_size=1)
    assert out.shape == (4, 1)
    assert np.array_equal(out.flatten(), image.flatten())


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_input():
    rng = np.random.default_rng(2)
    image = rng.normal(size=(2, 4, 4))
    image_copy = image.copy()
    patchify(image, patch_size=2)
    assert np.array_equal(image, image_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_unfold_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   image = torch.randn(2, 4, 4)
    #   unfold = torch.nn.Unfold(kernel_size=2, stride=2)
    #   patches = unfold(image[None])[0].T   # (num_patches, C*p*p)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image = np.array(
        [
            [
                [-1.9309, 0.9058, -0.0324, -1.4994],
                [1.2536, -1.4941, 0.9652, -0.7688],
                [0.9444, -1.3868, -1.1291, -1.3752],
                [-1.0605, 0.9124, 1.8890, 1.1681],
            ],
            [
                [-1.3471, -0.2563, -0.1939, -1.3477],
                [1.8719, -0.4934, 0.8213, 0.0107],
                [-1.9334, 0.1366, 0.4488, -0.7572],
                [0.8189, 0.7191, -0.1887, 1.7471],
            ],
        ]
    )
    expected = np.array(
        [
            [-1.9309, 0.9058, 1.2536, -1.4941, -1.3471, -0.2563, 1.8719, -0.4934],
            [-0.0324, -1.4994, 0.9652, -0.7688, -0.1939, -1.3477, 0.8213, 0.0107],
            [0.9444, -1.3868, -1.0605, 0.9124, -1.9334, 0.1366, 0.8189, 0.7191],
            [-1.1291, -1.3752, 1.8890, 1.1681, 0.4488, -0.7572, -0.1887, 1.7471],
        ]
    )

    out = patchify(image, patch_size=2)
    assert np.allclose(out, expected, atol=1e-3)
