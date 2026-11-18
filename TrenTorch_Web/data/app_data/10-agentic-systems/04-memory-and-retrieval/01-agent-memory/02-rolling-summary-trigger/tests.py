"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

messages_to_summarize = _module.messages_to_summarize


def test_1_already_fits():
    assert messages_to_summarize([5, 5, 5], 20, 3, 1) == 0


def test_2_smallest_k_hand_computed():
    # total 40 > 25. k=1: 30+5=35 ; k=2: 20+5=25 -> fits
    assert messages_to_summarize([10, 10, 10, 10], 25, 5, 1) == 2


def test_3_one_big_old_message_needs_only_one_fold():
    assert messages_to_summarize([30, 2, 2, 2], 20, 4, 1) == 1


def test_4_recent_messages_are_protected():
    with pytest.raises(ValueError):
        messages_to_summarize([5, 50], 20, 3, 1)


def test_5_summary_must_be_smaller_than_what_it_replaces():
    with pytest.raises(ValueError):
        messages_to_summarize([4, 4, 4], 8, 5, 1)


def test_6_exactly_at_budget_after_folding():
    assert messages_to_summarize([10, 10, 10], 15, 5, 1) == 2


def test_7_returned_k_is_minimal_and_inputs_untouched():
    counts = [8, 3, 9, 4, 6, 2]
    snap = list(counts)
    k = messages_to_summarize(counts, 17, 2, 2)
    assert sum(counts[k:]) + 2 <= 17 and (k == 1 or sum(counts[k - 1:]) + 2 > 17) and counts == snap
