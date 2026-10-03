"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
advance = _module.advance
allowed_token_ids = _module.allowed_token_ids
mask_logits = _module.mask_logits

DIGITS = "0123456789"
INT = {("start", c): "digits" for c in DIGITS}
INT.update({("digits", c): "digits" for c in DIGITS})
VOCAB = ["1", "12", "a", "1a", "", "007", "-"]


def test_1_advance_through_a_valid_token():
    assert advance(INT, "start", "123") == "digits"


def test_2_advance_returns_none_on_any_invalid_character():
    assert advance(INT, "start", "1a") is None and advance(INT, "start", "a1") is None


def test_3_empty_token_leaves_the_state_alone():
    assert advance(INT, "start", "") == "start"


def test_4_allowed_ids_hand_computed():
    assert allowed_token_ids(INT, "start", VOCAB) == [0, 1, 5]


def test_5_machine_state_changes_what_is_allowed():
    machine = {("s", "a"): "t", ("t", "b"): "s"}
    vocab = ["a", "b", "ab", "ba"]
    assert allowed_token_ids(machine, "s", vocab) == [0, 2]
    assert allowed_token_ids(machine, "t", vocab) == [1, 3]


def test_6_mask_logits_hand_computed():
    out = mask_logits(np.array([1.0, 2.0, 3.0]), [0, 2])
    assert out[0] == 1.0 and out[2] == 3.0 and out[1] == -np.inf


def test_7_masked_softmax_never_picks_a_disallowed_token_and_input_untouched():
    logits = np.array([5.0, 9.0, 0.0, 9.5, 1.0, 2.0, 7.0])
    snap = logits.copy()
    out = mask_logits(logits, allowed_token_ids(INT, "start", VOCAB))
    p = np.exp(out - out.max())
    p /= p.sum()
    assert p[2] == p[3] == p[4] == p[6] == 0.0 and np.isclose(p.sum(), 1.0)
    assert np.array_equal(logits, snap)
