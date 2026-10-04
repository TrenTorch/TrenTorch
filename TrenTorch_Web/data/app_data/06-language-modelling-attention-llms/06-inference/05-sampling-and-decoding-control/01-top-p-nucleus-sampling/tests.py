"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
top_p_filter = _module.top_p_filter


def test_1_hand_computed():
    out = top_p_filter(np.array([0.5, 0.3, 0.15, 0.05]), 0.8)
    assert np.allclose(out, [0.5 / 0.8, 0.3 / 0.8, 0, 0])


def test_2_exactly_reaching_p_stops_there():
    out = top_p_filter(np.array([0.6, 0.4, 0.0]), 0.6)
    assert np.allclose(out, [1.0, 0.0, 0.0])


def test_3_small_p_keeps_only_the_top_token():
    out = top_p_filter(np.array([0.2, 0.5, 0.3]), 0.01)
    assert np.allclose(out, [0, 1.0, 0])


def test_4_p_one_keeps_everything_with_nonzero_mass_unchanged():
    probs = np.array([0.1, 0.2, 0.3, 0.4])
    assert np.allclose(top_p_filter(probs, 1.0), probs)


def test_5_nucleus_adapts_to_confidence():
    sure = top_p_filter(np.array([0.95, 0.03, 0.01, 0.01]), 0.9)
    unsure = top_p_filter(np.array([0.3, 0.3, 0.2, 0.2]), 0.9)
    assert (sure > 0).sum() == 1 and (unsure > 0).sum() == 4


def test_6_ties_are_resolved_toward_lower_index():
    out = top_p_filter(np.array([0.25, 0.25, 0.25, 0.25]), 0.3)
    assert np.allclose(out, [0.5, 0.5, 0, 0])


def test_7_sums_to_one_and_input_untouched():
    rng = np.random.RandomState(0)
    raw = rng.rand(20)
    probs = raw / raw.sum()
    snap = probs.copy()
    out = top_p_filter(probs, 0.7)
    assert np.isclose(out.sum(), 1.0) and np.array_equal(probs, snap)
