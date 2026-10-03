"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
rouge_n = _module.rouge_n
rouge_l = _module.rouge_l

REF = "police killed the gunman".split()


def test_1_rouge1_hand_computed():
    cand = "police kill the gunman".split()
    p, r, f = rouge_n(cand, REF, 1)
    assert np.isclose(p, 3 / 4) and np.isclose(r, 3 / 4) and np.isclose(f, 3 / 4)


def test_2_rouge2_hand_computed():
    cand = "the gunman police killed".split()
    # candidate bigrams: the gunman, gunman police, police killed ; ref: police killed, killed the, the gunman
    p, r, f = rouge_n(cand, REF, 2)
    assert np.isclose(p, 2 / 3) and np.isclose(r, 2 / 3)


def test_3_recall_and_precision_differ_for_unequal_lengths():
    p, r, _ = rouge_n("police".split(), REF, 1)
    assert np.isclose(p, 1.0) and np.isclose(r, 0.25)


def test_4_rouge_l_respects_order_not_adjacency():
    p, r, f = rouge_l("police the gunman killed".split(), REF)
    # LCS of [police the gunman killed] and [police killed the gunman] is "police the gunman" (3)
    assert np.isclose(p, 3 / 4) and np.isclose(r, 3 / 4)


def test_5_rouge_l_reversed_text_is_low():
    cand = list(reversed(REF))
    _, r, _ = rouge_l(cand, REF)
    assert np.isclose(r, 1 / 4)


def test_6_empty_inputs_are_safe():
    assert rouge_n([], REF, 1) == (0.0, 0.0, 0.0)
    assert rouge_l(REF, []) == (0.0, 0.0, 0.0)
    assert rouge_n("a".split(), "b".split(), 1) == (0.0, 0.0, 0.0)


def test_7_identical_text_scores_one_and_inputs_untouched():
    cand = list(REF)
    snap = list(cand)
    for fn in (lambda: rouge_n(cand, REF, 1), lambda: rouge_n(cand, REF, 2), lambda: rouge_l(cand, REF)):
        p, r, f = fn()
        assert np.isclose(p, 1.0) and np.isclose(r, 1.0) and np.isclose(f, 1.0)
    assert cand == snap
