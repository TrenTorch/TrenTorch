"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
min_p_filter = _module.min_p_filter


def test_1_hand_computed():
    out = min_p_filter(np.array([0.6, 0.3, 0.07, 0.03]), 0.2)
    # threshold 0.12 keeps 0.6 and 0.3
    assert np.allclose(out, [0.6 / 0.9, 0.3 / 0.9, 0, 0])


def test_2_threshold_scales_with_the_top_probability():
    peaked = min_p_filter(np.array([0.8, 0.1, 0.05, 0.05]), 0.5)
    flat = min_p_filter(np.array([0.3, 0.3, 0.25, 0.15]), 0.5)
    assert (peaked > 0).sum() == 1 and (flat > 0).sum() == 4


def test_3_zero_min_p_keeps_everything():
    probs = np.array([0.7, 0.2, 0.1])
    assert np.allclose(min_p_filter(probs, 0.0), probs)


def test_4_min_p_one_keeps_only_the_maximum():
    assert np.allclose(min_p_filter(np.array([0.2, 0.5, 0.3]), 1.0), [0, 1, 0])


def test_5_ties_with_the_maximum_survive_together():
    assert np.allclose(min_p_filter(np.array([0.4, 0.4, 0.2]), 1.0), [0.5, 0.5, 0])


def test_6_boundary_is_inclusive():
    out = min_p_filter(np.array([0.5, 0.25, 0.25]), 0.5)
    assert np.allclose(out, [0.5, 0.25, 0.25])


def test_7_sums_to_one_and_input_untouched():
    probs = np.random.RandomState(1).dirichlet(np.ones(15))
    snap = probs.copy()
    assert np.isclose(min_p_filter(probs, 0.1).sum(), 1.0) and np.array_equal(probs, snap)
