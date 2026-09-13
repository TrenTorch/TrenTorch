"""
pytest data/app_data/07-vision/05-cnn-architecture-history/06-feature-pyramid-merge/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}")
nearest_upsample_2x = _module.nearest_upsample_2x
fpn_merge = _module.fpn_merge
pointwise_conv = load_solution("07-vision/04-modern-cnn-concepts/03-1x1-convolution").pointwise_conv


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_nearest_upsample_doubles_both_spatial_dims():
    x = np.arange(2 * 3 * 3, dtype=float).reshape(2, 3, 3)
    out = nearest_upsample_2x(x)
    assert out.shape == (2, 6, 6)


def test_02_fpn_merge_output_shape_matches_lower_res_channel_count():
    rng = np.random.default_rng(0)
    higher_res = rng.normal(size=(2, 6, 6))
    lower_res = rng.normal(size=(3, 3, 3))
    lateral_kernel = rng.normal(size=(3, 2, 1, 1))
    out = fpn_merge(higher_res, lower_res, lateral_kernel)
    assert out.shape == (3, 6, 6)


# --- Shape / general-case coverage -----------------------------------


def test_03_nearest_upsample_replicates_each_pixel_into_a_2x2_block():
    x = np.array([[[1.0, 2.0], [3.0, 4.0]]])
    out = nearest_upsample_2x(x)
    expected = np.array([[1.0, 1.0, 2.0, 2.0], [1.0, 1.0, 2.0, 2.0], [3.0, 3.0, 4.0, 4.0], [3.0, 3.0, 4.0, 4.0]])
    assert np.allclose(out[0], expected)


def test_04_fpn_merge_matches_manual_lateral_plus_upsample():
    rng = np.random.default_rng(1)
    higher_res = rng.normal(size=(3, 4, 4))
    lower_res = rng.normal(size=(2, 2, 2))
    lateral_kernel = rng.normal(size=(2, 3, 1, 1))
    out = fpn_merge(higher_res, lower_res, lateral_kernel)
    manual = pointwise_conv(higher_res, lateral_kernel) + nearest_upsample_2x(lower_res)
    assert np.allclose(out, manual)


# --- Parameter handling -------------------------------------------------


def test_05_zero_lateral_kernel_leaves_pure_upsampled_lower_res():
    rng = np.random.default_rng(2)
    higher_res = rng.normal(size=(3, 4, 4))
    lower_res = rng.normal(size=(2, 2, 2))
    lateral_kernel = np.zeros((2, 3, 1, 1))
    out = fpn_merge(higher_res, lower_res, lateral_kernel)
    assert np.allclose(out, nearest_upsample_2x(lower_res))


# --- Edge cases ---------------------------------------------------------


def test_06_single_channel_smallest_valid_case():
    higher_res = np.array([[[1.0, 2.0], [3.0, 4.0]]])
    lower_res = np.array([[[5.0]]])
    lateral_kernel = np.array([[[[1.0]]]])
    out = fpn_merge(higher_res, lower_res, lateral_kernel)
    assert out.shape == (1, 2, 2)
    assert np.allclose(out[0], higher_res[0] + 5.0)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(3)
    higher_res = rng.normal(size=(2, 4, 4))
    lower_res = rng.normal(size=(3, 2, 2))
    lateral_kernel = rng.normal(size=(3, 2, 1, 1))
    h_copy, l_copy, k_copy = higher_res.copy(), lower_res.copy(), lateral_kernel.copy()
    fpn_merge(higher_res, lower_res, lateral_kernel)
    assert np.array_equal(higher_res, h_copy)
    assert np.array_equal(lower_res, l_copy)
    assert np.array_equal(lateral_kernel, k_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_lateral_1x1_conv_plus_nearest_upsample_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   higher_res = torch.randn(2, 6, 6)
    #   lower_res = torch.randn(3, 3, 3)
    #   lateral_kernel = torch.randn(3, 2, 1, 1)
    #   lateral = torch.nn.functional.conv2d(higher_res[None], lateral_kernel)[0]
    #   upsampled = torch.nn.functional.interpolate(lower_res[None], scale_factor=2, mode='nearest')[0]
    #   merged = lateral + upsampled
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    higher_res = np.array(
        [
            [
                [-1.5405, -0.3515, -0.3186, -1.2221, 2.1723, -0.5020],
                [0.9029, -1.6458, 0.7199, 0.9037, 0.2337, -0.1412],
                [1.4302, 0.6298, -0.0863, 1.3132, -1.1905, 0.8380],
                [-0.7764, -0.1815, -0.0340, 0.4144, -0.6332, -0.2861],
                [-2.1916, -0.1575, 0.3276, -0.9119, -0.3281, 0.5212],
                [1.6852, 0.4301, 0.0280, 0.3196, -0.9579, 2.6285],
            ],
            [
                [-1.8652, 0.9344, 1.0118, -0.5055, -2.8440, -0.0912],
                [1.5258, -0.2799, -1.0172, 1.2744, 1.2412, -1.0133],
                [-0.6216, -0.3645, -0.3845, 0.5635, -0.6911, 0.4574],
                [-0.6132, -0.3457, 1.4870, 0.0396, 0.7685, -0.6631],
                [-0.9658, 0.3166, -0.8006, -0.0154, -0.3039, -0.1672],
                [-1.2107, 1.4709, -0.8776, 0.8210, 0.3380, 1.1078],
            ],
        ]
    )
    lower_res = np.array(
        [
            [[-1.2199, 1.6206, 0.6567], [-2.1026, -0.0410, 0.8357], [-1.7043, 2.4637, -0.9884]],
            [[0.4447, -1.1045, -0.5099], [0.3416, -0.1798, 1.6993], [-0.9074, 0.4727, 0.4439]],
            [[0.5401, -0.2608, 1.2874], [-0.5082, 0.5326, -1.1813], [-0.2623, -1.0114, -0.3043]],
        ]
    )
    lateral_kernel = np.array([1.0939, -0.7509, -0.0473, 1.8444, -0.7069, -0.5920]).reshape(3, 2, 1, 1)
    expected_channel0 = np.array(
        [
            [-1.5045, -2.3061, 0.5123, 0.6634, 5.1687, 0.1760],
            [-1.3780, -2.8101, 3.1720, 1.6522, -0.0198, 1.2632],
            [-0.0713, -1.1399, 0.1533, 0.9724, 0.0523, 1.4089],
            [-2.4915, -2.0415, -1.1948, 0.3826, -0.4341, 1.0206],
            [-3.3766, -2.1143, 3.4232, 1.4777, -1.1190, -0.2927],
            [1.0483, -2.3384, 3.1533, 2.1968, -2.2900, 1.0551],
        ]
    )

    out = fpn_merge(higher_res, lower_res, lateral_kernel)
    assert out.shape == (3, 6, 6)
    assert np.allclose(out[0], expected_channel0, atol=1e-2)
