"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
apply_penalties = _module.apply_penalties
Z = np.array([2.0, -1.0, 0.5, 3.0])


def test_1_repetition_hand_computed_sign_aware():
    out = apply_penalties(Z, [0, 1], rep=2.0)
    assert np.allclose(out, [1.0, -2.0, 0.5, 3.0])


def test_2_repetition_always_lowers_seen_logits():
    out = apply_penalties(Z, [0, 1, 2], rep=1.5)
    assert (out[:3] < Z[:3]).all() and out[3] == Z[3]


def test_3_frequency_scales_with_count():
    out = apply_penalties(Z, [3, 3, 3, 0], freq=0.5)
    assert np.allclose(out, [2.0 - 0.5, -1.0, 0.5, 3.0 - 1.5])


def test_4_presence_is_flat_once():
    out = apply_penalties(Z, [3, 3, 3], pres=1.0)
    assert np.isclose(out[3], 2.0) and out[0] == 2.0


def test_5_all_penalties_combine_in_the_stated_order():
    out = apply_penalties(np.array([4.0, 1.0]), [0, 0], rep=2.0, freq=0.5, pres=0.25)
    # 4/2 = 2 ; then - (0.5*2 + 0.25) = 0.75
    assert np.allclose(out, [0.75, 1.0])


def test_6_no_history_changes_nothing():
    assert np.array_equal(apply_penalties(Z, [], rep=2.0, freq=1.0, pres=1.0), Z)


def test_7_unity_rep_and_zero_penalties_are_identity_and_input_untouched():
    snap = Z.copy()
    assert np.array_equal(apply_penalties(Z, [0, 1, 1]), Z)
    apply_penalties(Z, [0], rep=3.0, freq=1.0, pres=1.0)
    assert np.array_equal(Z, snap)
