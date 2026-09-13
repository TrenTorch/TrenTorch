"""
pytest data/app_data/07-vision/05-cnn-architecture-history/02-vgg-small-conv-stack/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

vgg_stack = load_solution(
    f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}"
).vgg_stack
conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_layer_preserves_spatial_size():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(2, 6, 6))
    kernel = rng.normal(size=(2, 2, 3, 3))
    out = vgg_stack(x, [kernel])
    assert out.shape == (2, 6, 6)


def test_02_stacking_layers_still_preserves_spatial_size():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 5, 5))
    k1 = rng.normal(size=(3, 3, 3, 3))
    k2 = rng.normal(size=(3, 3, 3, 3))
    k3 = rng.normal(size=(3, 3, 3, 3))
    out = vgg_stack(x, [k1, k2, k3])
    assert out.shape == (3, 5, 5)


# --- Shape / general-case coverage -----------------------------------


def test_03_matches_manual_pad_conv_relu_chain():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(2, 6, 6))
    k1 = rng.normal(size=(2, 2, 3, 3))
    k2 = rng.normal(size=(2, 2, 3, 3))
    out = vgg_stack(x, [k1, k2])
    a1 = np.maximum(0.0, conv2d_multi_filter(np.pad(x, ((0, 0), (1, 1), (1, 1))), k1))
    a2 = np.maximum(0.0, conv2d_multi_filter(np.pad(a1, ((0, 0), (1, 1), (1, 1))), k2))
    assert np.allclose(out, a2)


def test_04_empty_kernel_list_returns_x_unchanged():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(2, 4, 4))
    out = vgg_stack(x, [])
    assert np.allclose(out, x)


# --- Parameter handling -------------------------------------------------


def test_05_output_never_negative_after_relu():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(2, 5, 5))
    kernel = rng.normal(size=(2, 2, 3, 3))
    out = vgg_stack(x, [kernel, kernel])
    assert np.all(out >= 0.0)


# --- Edge cases ---------------------------------------------------------


def test_06_single_channel_smallest_case():
    x = np.array([[[1.0, -2.0, 3.0], [-1.0, 0.5, -0.5], [2.0, -3.0, 1.0]]])
    kernel = np.zeros((1, 1, 3, 3))
    out = vgg_stack(x, [kernel])
    assert out.shape == (1, 3, 3)
    assert np.allclose(out, 0.0)  # zero kernel -> relu(0) everywhere


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(5)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))
    k2 = rng.normal(size=(2, 2, 3, 3))
    x_copy, k1_copy, k2_copy = x.copy(), k1.copy(), k2.copy()
    vgg_stack(x, [k1, k2])
    assert np.array_equal(x, x_copy)
    assert np.array_equal(k1, k1_copy)
    assert np.array_equal(k2, k2_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_two_layer_3x3_same_padded_conv_relu_stack_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(2, 6, 6)
    #   k1, k2 = torch.randn(2, 2, 3, 3), torch.randn(2, 2, 3, 3)
    #   a1 = torch.relu(torch.nn.functional.conv2d(x[None], k1, padding=1)[0])
    #   a2 = torch.relu(torch.nn.functional.conv2d(a1[None], k2, padding=1)[0])
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [
                [0.3920, 0.0734, -0.0045, -0.0535, -0.0589, 0.6002],
                [2.0421, 1.3273, -0.8703, -1.5555, -0.8620, -0.1290],
                [1.4632, 0.2698, -1.3583, -0.7568, -0.4102, 0.2939],
                [-0.0538, -0.9547, -1.3138, 0.4306, -1.3356, 1.1686],
                [0.9662, -1.7636, -1.9802, -0.0056, 0.8050, 0.7928],
                [-0.6498, 0.0352, -1.1281, 0.8134, 0.2734, -0.3833],
            ],
            [
                [1.1319, -0.1240, -0.6294, -0.5749, -0.8881, 0.7359],
                [0.6198, 0.3908, 1.0492, 0.3543, 0.0289, -1.0003],
                [-0.6858, 2.0945, 0.7393, -0.0455, -1.7682, -0.1843],
                [-1.3310, 0.5904, -0.1553, -1.9891, -0.7289, 0.5800],
                [2.6280, 1.8364, -0.2666, -0.4687, -0.3512, 0.4390],
                [-1.8193, 1.1163, 0.7859, 2.6835, -0.0801, 1.3936],
            ],
        ]
    )
    k1 = np.array(
        [
            [
                [[1.2642, -1.6138, 0.6943], [-0.3317, -0.8901, -0.5309], [0.2726, 0.4209, 0.3279]],
                [[-0.2489, 0.5272, -0.7679], [-0.4534, 1.9083, 0.1863], [0.7673, 1.1733, 1.4428]],
            ],
            [
                [[0.8873, 0.9089, -0.7886], [0.8581, -0.4342, 0.6588], [0.1169, -0.4490, -0.4022]],
                [[0.4632, -0.6400, 1.3269], [0.1426, 0.5611, -1.3239], [-1.6464, 0.2511, -2.1333]],
            ],
        ]
    )
    k2 = np.array(
        [
            [
                [[-0.3334, -0.5092, 0.1089], [-0.7180, -0.4168, 1.7441], [2.1370, 0.6025, 1.2311]],
                [[0.8989, 0.0091, 0.5026], [0.1593, 1.0669, -0.2227], [0.3894, 0.8661, -0.8454]],
            ],
            [
                [[1.6114, 0.1142, -0.5220], [0.3986, 0.0819, 0.1093], [0.4498, 0.9590, 0.4958]],
                [[1.3353, -1.0348, 0.6593], [-1.7815, -0.3361, -0.6571], [-0.7755, 1.8049, -1.1590]],
            ],
        ]
    )
    expected = np.array(
        [
            [
                [6.2968, 8.2232, 6.7880, 10.6347, 1.3725, 1.4244],
                [0.0000, 9.2065, 7.5091, 4.1137, 1.7130, 1.8644],
                [9.8620, 12.4858, 20.6543, 4.3093, 3.3015, 1.5507],
                [24.3116, 25.0811, 23.8127, 30.7530, 6.3593, 12.4374],
                [19.6220, 19.0622, 9.1037, 11.9374, 4.5958, 0.0000],
                [13.9465, 0.0000, 0.0000, 0.0000, 0.2472, 0.0000],
            ],
            [
                [3.2549, 8.2840, 4.7922, 2.5473, 0.0000, 0.0000],
                [0.0000, 20.4153, 7.1695, 0.7403, 0.0000, 0.0000],
                [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.2609],
                [8.1157, 11.4233, 21.5759, 13.2029, 7.4054, 3.4295],
                [0.4491, 9.9821, 15.6221, 11.6305, 0.0000, 9.0956],
                [0.0000, 0.0000, 18.5610, 12.5667, 0.7974, 8.5386],
            ],
        ]
    )

    out = vgg_stack(x, [k1, k2])
    assert np.allclose(out, expected, atol=1e-2)
