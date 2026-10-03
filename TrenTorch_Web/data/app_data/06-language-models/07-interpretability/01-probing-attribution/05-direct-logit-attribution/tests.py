"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
direct_logit_attribution = _module.direct_logit_attribution
attribution_total = _module.attribution_total


def test_1_hand_computed():
    comps = np.array([[1.0, 0.0], [0.0, 2.0]])
    W_U = np.array([[3.0, 1.0], [0.0, 4.0]])  # columns are token vectors
    # direction = W_U[:,0] - W_U[:,1] = [2, -4]
    out = direct_logit_attribution(comps, W_U, 0, 1, 1.0)
    assert np.allclose(out, [2.0, -8.0])


def test_2_scale_divides_every_contribution():
    comps = np.array([[2.0, 2.0]])
    W_U = np.eye(2)
    assert np.allclose(direct_logit_attribution(comps, W_U, 0, 1, 4.0), [0.0])
    a = direct_logit_attribution(np.array([[4.0, 0.0]]), W_U, 0, 1, 2.0)
    assert np.allclose(a, [2.0])


def test_3_contributions_sum_to_the_full_logit_difference():
    rng = np.random.RandomState(0)
    comps, W_U = rng.randn(7, 6), rng.randn(6, 10)
    scale = 2.5
    contrib = direct_logit_attribution(comps, W_U, 3, 8, scale)
    final = comps.sum(axis=0) / scale
    logits = final @ W_U
    assert np.isclose(attribution_total(contrib), logits[3] - logits[8])


def test_4_a_component_orthogonal_to_the_direction_contributes_nothing():
    W_U = np.array([[1.0, 0.0], [0.0, 1.0]])
    comps = np.array([[1.0, 1.0]])  # direction is [1, -1], dot = 0
    assert np.allclose(direct_logit_attribution(comps, W_U, 0, 1, 1.0), [0.0])


def test_5_swapping_the_answers_flips_the_sign():
    rng = np.random.RandomState(1)
    comps, W_U = rng.randn(4, 5), rng.randn(5, 6)
    a = direct_logit_attribution(comps, W_U, 1, 2, 1.0)
    b = direct_logit_attribution(comps, W_U, 2, 1, 1.0)
    assert np.allclose(a, -b)


def test_6_shape_and_total_type():
    out = direct_logit_attribution(np.ones((9, 3)), np.ones((3, 4)), 0, 1, 1.0)
    assert out.shape == (9,)
    assert isinstance(attribution_total(out), float)


def test_7_inputs_not_modified():
    rng = np.random.RandomState(2)
    comps, W_U = rng.randn(3, 4), rng.randn(4, 5)
    s1, s2 = comps.copy(), W_U.copy()
    direct_logit_attribution(comps, W_U, 0, 4, 1.7)
    assert np.array_equal(comps, s1) and np.array_equal(W_U, s2)
