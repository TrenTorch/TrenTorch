"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
content_loss = _module.content_loss
style_loss = _module.style_loss
total_loss = _module.total_loss


def feats(seed, shapes=((2, 3, 3), (3, 2, 2))):
    rng = np.random.RandomState(seed)
    return [rng.randn(*s) for s in shapes]


def test_1_identical_inputs_give_zero():
    f = feats(0)
    assert content_loss(f[0], f[0]) == 0.0 and style_loss(f, f, [1.0, 1.0]) == 0.0


def test_2_content_loss_hand_computed():
    assert np.isclose(content_loss(np.array([1.0, 2.0]), np.array([0.0, 4.0])), (1 + 4) / 2)


def test_3_style_loss_hand_computed_single_layer():
    g = np.array([[[1.0, 1.0]]])  # C=1: gram = 2/2 = 1
    s = np.array([[[2.0, 2.0]]])  # gram = 8/2 = 4
    assert np.isclose(style_loss([g], [s], [0.5]), 0.5 * 9.0)


def test_4_style_loss_ignores_spatial_rearrangement():
    f = feats(1, ((3, 4, 4),))[0]
    perm = np.random.RandomState(2).permutation(16)
    shuffled = f.reshape(3, -1)[:, perm].reshape(3, 4, 4)
    ref = feats(3, ((3, 4, 4),))
    assert np.isclose(style_loss([f], ref, [1.0]), style_loss([shuffled], ref, [1.0]))
    assert content_loss(f, shuffled) > 0


def test_5_layer_weights_scale_the_terms():
    g, s = feats(4), feats(5)
    a = style_loss(g, s, [1.0, 0.0])
    b = style_loss(g, s, [1.0, 1.0])
    assert b > a and np.isclose(style_loss(g, s, [2.0, 0.0]), 2 * a)


def test_6_total_loss_weighted_sum():
    assert np.isclose(total_loss(1.0, 2.0, 3.0, 10.0, 100.0, 1000.0), 10 + 200 + 3000)


def test_7_inputs_untouched():
    g, s = feats(6), feats(7)
    snap = [a.copy() for a in g]
    style_loss(g, s, [1.0, 1.0])
    content_loss(g[0], s[0])
    assert all(np.array_equal(a, b) for a, b in zip(g, snap))
