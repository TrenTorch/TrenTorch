"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
conv2d_same = _module.conv2d_same
inception_forward = _module.inception_forward


def params(rng, C=3, o1=2, r2=2, o2=3, r3=2, o3=2, o4=1):
    return {
        "b1": rng.randn(o1, C, 1, 1), "b2a": rng.randn(r2, C, 1, 1), "b2b": rng.randn(o2, r2, 3, 3),
        "b3a": rng.randn(r3, C, 1, 1), "b3b": rng.randn(o3, r3, 5, 5), "b4": rng.randn(o4, C, 1, 1),
    }


def test_1_one_by_one_conv_is_a_per_pixel_matrix_product():
    rng = np.random.RandomState(0)
    x, w = rng.randn(3, 4, 4), rng.randn(5, 3, 1, 1)
    assert np.allclose(conv2d_same(x, w), np.einsum("oc,chw->ohw", w[:, :, 0, 0], x))


def test_2_identity_kernel_reproduces_the_input():
    x = np.random.RandomState(1).randn(1, 5, 5)
    w = np.zeros((1, 1, 3, 3))
    w[0, 0, 1, 1] = 1.0
    assert np.allclose(conv2d_same(x, w), x)


def test_3_conv_hand_computed_with_zero_padding():
    x = np.ones((1, 3, 3))
    w = np.ones((1, 1, 3, 3))
    out = conv2d_same(x, w)[0]
    assert out[1, 1] == 9.0 and out[0, 0] == 4.0 and out[0, 1] == 6.0


def test_4_output_channels_are_the_sum_of_branch_channels_and_size_is_kept():
    rng = np.random.RandomState(2)
    p = params(rng)
    out = inception_forward(rng.randn(3, 6, 6), p)
    assert out.shape == (2 + 3 + 2 + 1, 6, 6)


def test_5_first_channels_are_the_one_by_one_branch():
    rng = np.random.RandomState(3)
    x, p = rng.randn(3, 5, 5), params(rng)
    out = inception_forward(x, p)
    assert np.allclose(out[:2], np.maximum(conv2d_same(x, p["b1"]), 0))


def test_6_outputs_are_non_negative_because_every_branch_ends_in_relu():
    rng = np.random.RandomState(4)
    assert (inception_forward(rng.randn(3, 5, 5), params(rng)) >= 0).all()


def test_7_pooling_branch_matches_a_max_filter_oracle_and_input_untouched():
    rng = np.random.RandomState(5)
    x = rng.randn(2, 4, 4)
    snap = x.copy()
    p = params(rng, C=2)
    p["b4"] = np.ones((1, 2, 1, 1))
    out = inception_forward(x, p)
    pooled = np.zeros_like(x)
    xp = np.pad(x, ((0, 0), (1, 1), (1, 1)), constant_values=-np.inf)
    for c in range(2):
        for i in range(4):
            for j in range(4):
                pooled[c, i, j] = xp[c, i:i + 3, j:j + 3].max()
    assert np.allclose(out[-1], np.maximum(pooled.sum(axis=0), 0)) and np.array_equal(x, snap)
