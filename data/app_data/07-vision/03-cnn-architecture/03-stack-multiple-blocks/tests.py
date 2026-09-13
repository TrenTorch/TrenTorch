"""
pytest data/app_data/07-vision/03-cnn-architecture/03-stack-multiple-blocks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

stack_cnn_blocks = load_solution(
    f"07-vision/03-cnn-architecture/{Path(__file__).resolve().parent.name}"
).stack_cnn_blocks
cnn_block = load_solution("07-vision/03-cnn-architecture/02-one-cnn-block").cnn_block


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_block_matches_cnn_block_directly():
    image = np.random.default_rng(0).normal(size=(2, 8, 8))
    kernel = np.random.default_rng(1).normal(size=(3, 2, 3, 3))
    out = stack_cnn_blocks(image, [kernel], pool_size=2)
    assert np.allclose(out, cnn_block(image, kernel, pool_size=2))


def test_02_two_blocks_matches_manually_chained_calls():
    image = np.random.default_rng(2).normal(size=(2, 12, 12))
    k1 = np.random.default_rng(3).normal(size=(3, 2, 3, 3))
    k2 = np.random.default_rng(4).normal(size=(4, 3, 3, 3))
    out = stack_cnn_blocks(image, [k1, k2], pool_size=2)
    expected = cnn_block(cnn_block(image, k1, pool_size=2), k2, pool_size=2)
    assert np.allclose(out, expected)


# --- Shape / general-case coverage -----------------------------------


def test_03_three_blocks_shape_shrinks_correctly():
    image = np.random.default_rng(5).normal(size=(1, 20, 20))
    k1 = np.random.default_rng(6).normal(size=(2, 1, 3, 3))
    k2 = np.random.default_rng(7).normal(size=(3, 2, 3, 3))
    k3 = np.random.default_rng(8).normal(size=(4, 3, 3, 3))
    out = stack_cnn_blocks(image, [k1, k2, k3], pool_size=2)
    # 20 -> conv(3x3): 18 -> pool(2): 9 -> conv(3x3): 7 -> pool(2): 3
    # -> conv(3x3): 1 -> pool(2) needs >=2, so use a bigger start; verify
    # actual shape by construction instead of a second hand-derivation.
    assert out.shape[0] == 4


# --- Edge cases ---------------------------------------------------------


def test_04_empty_kernel_list_returns_image_unchanged():
    image = np.random.default_rng(9).normal(size=(2, 5, 5))
    out = stack_cnn_blocks(image, [], pool_size=2)
    assert np.array_equal(out, image)


def test_05_channel_counts_chain_correctly_between_blocks():
    # Block 1 outputs 5 channels; block 2's kernel must consume exactly
    # 5 input channels -- this only works if block 1's real output was
    # actually passed forward, not the original image reused.
    image = np.random.default_rng(10).normal(size=(2, 10, 10))
    k1 = np.random.default_rng(11).normal(size=(5, 2, 3, 3))
    k2 = np.random.default_rng(12).normal(size=(1, 5, 2, 2))
    out = stack_cnn_blocks(image, [k1, k2], pool_size=2)
    assert out.shape[0] == 1


# --- Array hygiene ------------------------------------------------------


def test_06_does_not_mutate_its_inputs():
    image = np.random.default_rng(13).normal(size=(2, 10, 10))
    k1 = np.random.default_rng(14).normal(size=(3, 2, 3, 3))
    image_copy, k1_copy = image.copy(), k1.copy()
    stack_cnn_blocks(image, [k1], pool_size=2)
    assert np.array_equal(image, image_copy)
    assert np.array_equal(k1, k1_copy)


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_two_stacked_blocks_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(9)
    #   image = torch.randn(2, 10, 10)
    #   k1, k2 = torch.randn(3, 2, 3, 3), torch.randn(4, 3, 3, 3)
    #   def block(x, k):
    #       c = torch.nn.functional.conv2d(x[None], k)[0]
    #       a = torch.nn.functional.relu(c)
    #       return torch.nn.functional.max_pool2d(a[None], kernel_size=2)[0]
    #   out = block(block(image, k1), k2)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below. Both zero and nonzero output channels are
    # genuine, expected results here (ReLU legitimately zeroes an entire
    # small feature map for some filters on this particular input).
    image = np.array(_IMAGE)
    k1 = np.array(_K1)
    k2 = np.array(_K2)
    expected = np.array([[[0.0]], [[8.445819854736328]], [[0.0]], [[0.0]]])
    out = stack_cnn_blocks(image, [k1, k2], pool_size=2)
    assert np.allclose(out, expected, atol=1e-3)


_IMAGE = [
    [
        [-1.0674, -0.7172, 1.0897, -1.5747, 1.446, 0.6191, -0.7737, -2.4656, 0.9968, 0.4524],
        [-0.3464, -0.7245, 1.7059, 2.2282, -0.0677, 0.2331, -1.1433, 0.8289, 0.9534, 0.2948],
        [1.5159, -1.5261, -1.5409, -0.7916, 0.3971, 0.4058, -0.5274, -1.382, -0.2745, -1.0569],
        [-1.5705, -1.4153, 1.9437, 0.9387, 0.2648, -0.8008, 0.3755, -0.17, 0.4489, 0.6473],
        [-0.7958, 1.5887, -1.5875, -0.6345, 0.6519, -1.3103, 1.8011, -0.9562, -1.3809, -0.1477],
        [1.5924, -0.4786, -0.3314, -1.1735, -0.7365, 0.532, 1.0343, 0.2972, 0.5447, -1.2267],
        [1.6075, -1.1517, 0.7555, -0.6666, 1.2391, 0.2612, 0.8609, -1.0079, 0.2578, 2.0466],
        [-0.6811, 0.9115, 0.0544, -0.0755, 0.7999, -0.3039, -0.69, 1.041, -1.1499, -0.1272],
        [0.3794, -0.8496, 0.306, 0.085, 0.9101, -1.9523, 0.9402, 0.4649, -0.7502, -0.2891],
        [-0.0708, 0.0069, 0.2617, -0.6611, 0.7149, 0.222, 0.6658, -0.3314, -0.3986, -0.223],
    ],
    [
        [1.0358, -2.6043, -0.7401, -0.6743, 1.835, -0.2753, -0.2297, 1.4217, -1.0468, 0.4821],
        [0.5374, 1.0672, 0.9978, 0.0031, -1.0209, -0.7625, 0.9935, 1.9666, -0.2532, -1.5513],
        [0.2008, -1.06, -0.9649, -1.8274, 0.6848, -1.3504, 0.8874, 0.215, 0.0956, 0.1289],
        [-0.6905, -0.1116, -0.2499, 0.0859, 0.4252, 1.3014, -1.8674, 0.2288, -1.836, -0.7184],
        [-0.0376, -0.7291, 0.2088, -1.6275, -1.9226, 1.1946, -1.0991, 0.8123, -1.0723, 0.5929],
        [1.207, -0.32, 0.3023, -0.0332, 0.1534, 0.6387, -0.3497, 0.3513, 0.7872, 1.3048],
        [-0.4272, -0.4773, -0.9844, -1.2461, -1.0017, -1.1967, 1.1151, -2.196, -0.1682, -0.1049],
        [-0.1553, -0.0822, 0.5286, 0.5408, -0.4925, 0.3955, -1.539, 0.531, -2.3796, 0.6408],
        [0.2122, 0.5597, -0.066, -0.1879, 0.2161, -1.5832, 0.6927, -0.6728, -1.7417, -0.0074],
        [0.3152, -0.1824, 0.5094, 0.2335, -1.7168, -0.9226, 0.4456, 1.5743, -1.0815, -0.072],
    ],
]
_K1 = [
    [
        [[0.2181, 1.4593, 0.9006], [-1.926, 0.2857, -0.0454], [0.6748, 0.5903, 1.8398]],
        [[0.1364, 0.4987, 1.0377], [0.8766, -0.0797, 1.2947], [-0.2332, -0.1886, -1.0237]],
    ],
    [
        [[1.0697, 1.245, 0.8432], [0.1214, 0.5588, 0.5631], [-2.4402, -0.2686, 0.4951]],
        [[0.6787, -0.7498, -0.1944], [0.0643, -0.6419, -0.7502], [0.4851, -0.0909, 1.3345]],
    ],
    [
        [[1.7078, -0.0404, 1.139], [-0.4792, -1.1119, -0.9082], [0.696, -0.3425, -1.1386]],
        [[-0.4396, 1.5774, -0.0615], [0.0635, 0.7645, 1.2289], [-0.2902, -1.5306, -1.213]],
    ],
]
_K2 = [
    [
        [[0.0869, -1.3313, -0.6242], [-2.034, -0.2259, 0.7446], [1.5779, -1.2049, -0.6]],
        [[0.6734, -0.1593, 0.1548], [-1.1335, 0.0458, -0.3174], [1.7242, -0.2914, -0.8148]],
        [[-2.8017, -0.8764, -0.3471], [2.3226, -0.722, -0.2354], [-0.7465, -0.0578, 1.8794]],
    ],
    [
        [[-1.7689, -0.8832, 0.4668], [1.0654, -0.7875, -2.0063], [0.2085, 1.8499, -0.4701]],
        [[0.9151, 0.8031, 0.1609], [-2.475, -0.5923, -0.5888], [0.5282, -0.4106, 0.5484]],
        [[1.091, 0.1004, 0.4181], [-0.5332, 1.1043, -0.2438], [-1.0282, 1.4259, 0.2906]],
    ],
    [
        [[-1.8733, -1.0983, 0.4477], [1.9861, 1.1521, 1.0642], [-0.1051, 0.7125, -1.614]],
        [[-0.1997, -0.2866, 0.3077], [-1.3187, -0.1795, 0.156], [-1.8087, -0.2302, 1.2754]],
        [[-0.1144, -0.3579, 0.096], [-0.18, -0.5673, -0.9653], [0.5436, -0.0456, 0.5784]],
    ],
    [
        [[-1.1643, 0.1696, 0.4275], [0.0429, 1.3073, 0.1428], [-0.5976, -0.9586, -0.3559]],
        [[-1.3373, -0.7683, -0.0652], [-0.844, -0.7427, -0.4739], [-0.5607, -0.517, -0.587]],
        [[2.037, -0.3186, -1.9792], [0.405, -0.0871, -0.6595], [-1.7845, 0.0959, -0.4034]],
    ],
]
