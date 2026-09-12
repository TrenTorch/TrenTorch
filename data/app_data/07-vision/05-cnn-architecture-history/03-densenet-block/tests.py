"""
pytest data/app_data/07-vision/05-cnn-architecture-history/03-densenet-block/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

dense_block = load_solution(
    f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}"
).dense_block
conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_channel_count_grows_by_each_layers_output_channels():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))  # in=2 -> out=2
    out = dense_block(x, [k1])
    assert out.shape == (4, 5, 5)  # 2 original + 2 new


def test_02_spatial_size_is_preserved():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 6, 6))
    k1 = rng.normal(size=(2, 3, 3, 3))
    out = dense_block(x, [k1])
    assert out.shape[1:] == (6, 6)


# --- Shape / general-case coverage -----------------------------------


def test_03_two_layers_growing_channel_count():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))  # in=2 -> out=2, running total becomes 4
    k2 = rng.normal(size=(2, 4, 3, 3))  # in=4 -> out=2, running total becomes 6
    out = dense_block(x, [k1, k2])
    assert out.shape == (6, 5, 5)


def test_04_first_channels_of_the_output_are_the_original_input_unchanged():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))
    out = dense_block(x, [k1])
    assert np.allclose(out[:2], x)


# --- Parameter handling -------------------------------------------------


def test_05_empty_kernel_list_returns_x_unchanged():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(2, 4, 4))
    out = dense_block(x, [])
    assert np.allclose(out, x)


# --- Edge cases ---------------------------------------------------------


def test_06_matches_manual_pad_conv_relu_concat_chain():
    rng = np.random.default_rng(5)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))
    k2 = rng.normal(size=(3, 4, 3, 3))
    out = dense_block(x, [k1, k2])

    feat0 = x
    c1 = np.maximum(0.0, conv2d_multi_filter(np.pad(feat0, ((0, 0), (1, 1), (1, 1))), k1))
    feat1 = np.concatenate([feat0, c1], axis=0)
    c2 = np.maximum(0.0, conv2d_multi_filter(np.pad(feat1, ((0, 0), (1, 1), (1, 1))), k2))
    feat2 = np.concatenate([feat1, c2], axis=0)
    assert np.allclose(out, feat2)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(6)
    x = rng.normal(size=(2, 5, 5))
    k1 = rng.normal(size=(2, 2, 3, 3))
    x_copy, k1_copy = x.copy(), k1.copy()
    dense_block(x, [k1])
    assert np.array_equal(x, x_copy)
    assert np.array_equal(k1, k1_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_two_layer_dense_concat_chain_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   x = torch.randn(2, 5, 5)
    #   k1, k2 = torch.randn(2, 2, 3, 3), torch.randn(2, 4, 3, 3)
    #   feat0 = x
    #   c1 = torch.relu(torch.nn.functional.conv2d(feat0[None], k1, padding=1)[0])
    #   feat1 = torch.cat([feat0, c1], dim=0)
    #   c2 = torch.relu(torch.nn.functional.conv2d(feat1[None], k2, padding=1)[0])
    #   feat2 = torch.cat([feat1, c2], dim=0)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    x = np.array(
        [
            [
                [-0.9012, 0.5656, -0.4882, 0.7507, 0.5893],
                [-0.4552, -0.8135, 0.2670, -0.5531, 0.6016],
                [-0.9271, 0.5655, -2.4451, -0.1605, 0.1804],
                [2.2347, -0.6774, 0.8949, 0.9096, 0.4260],
                [1.2886, -0.1708, -0.8564, -0.6576, -0.2041],
            ],
            [
                [0.1203, -0.6191, -0.6317, -0.5774, 0.5874],
                [0.1230, 0.0885, -0.8708, 1.3073, -0.1244],
                [-0.8531, 1.2268, -2.0151, 0.1955, -1.5921],
                [-1.4647, -0.4805, -0.7016, 0.1341, 1.9434],
                [1.0825, -1.5422, 0.6945, -0.2041, -0.6442],
            ],
        ]
    )
    k1 = np.array(
        [
            [
                [[1.1093, -0.1230, -0.6921], [1.2534, -0.3842, -0.8658], [-1.0148, 0.2670, -1.0066]],
                [[-0.4865, 0.1088, -1.0973], [1.9052, 0.3173, -1.4414], [-1.3833, -0.2568, -0.3576]],
            ],
            [
                [[-2.0254, 1.9583, 0.0840], [-0.7976, 0.0422, -0.5356], [2.1111, -2.3104, 0.0628]],
                [[-1.0054, 1.1311, 0.3852], [0.4561, 0.9089, 0.2372], [-1.1251, -0.9250, -0.8627]],
            ],
        ]
    )
    k2 = np.array(
        [
            [
                [[0.5201, 0.0946, -1.1309], [-2.4204, -0.2249, 0.5117], [-0.5261, -0.1928, 0.4203]],
                [[-1.6114, -2.9993, -1.8305], [-0.1778, -0.8701, 1.2481], [1.3345, 0.5914, 0.5201]],
                [[-1.1349, -1.1278, 0.7709], [0.4347, 1.8970, -0.6601], [0.5166, 2.7288, 2.3219]],
                [[1.0109, 0.2448, 1.5374], [-0.6068, -0.1129, 0.3482], [0.2761, -0.8972, 0.3715]],
            ],
            [
                [[-0.9210, 0.2394, -0.0824], [-0.4016, -1.0349, 0.6668], [0.3445, 1.1639, 1.0839]],
                [[-1.6749, -1.0779, 0.3747], [-0.9163, 0.4493, -1.6360], [0.0576, -1.7111, -0.9758]],
                [[2.1640, 0.2435, 0.8651], [0.1387, -0.3562, -0.8442], [-0.6643, -0.4708, -1.8949]],
                [[0.8131, -1.1518, -0.4788], [-2.3260, -1.1522, 0.0103], [1.7073, 0.1603, -0.9406]],
            ],
        ]
    )
    expected_channel4 = np.array(
        [
            [16.5370, 20.1891, 6.4607, 18.8646, 6.8494],
            [6.4536, 13.7699, 20.1438, 0.0000, 7.1002],
            [14.3962, 0.0000, 2.1996, 10.9007, 3.7924],
            [35.3956, 24.4734, 14.3404, 1.1268, 1.8198],
            [10.3156, 14.8459, 13.4423, 0.5144, 0.0000],
        ]
    )

    out = dense_block(x, [k1, k2])
    assert out.shape == (6, 5, 5)
    assert np.allclose(out[:2], x, atol=1e-3)  # original input preserved verbatim
    assert np.allclose(out[4], expected_channel4, atol=1e-2)
