"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

trim_messages = _module.trim_messages


def msg(role, n):
    return {"role": role, "content": " ".join(["w"] * n)}


def test_1_everything_fits():
    msgs = [msg("system", 2), msg("user", 3), msg("assistant", 4)]
    assert trim_messages(msgs, 100) == msgs


def test_2_oldest_messages_are_dropped_first():
    msgs = [msg("system", 2), msg("user", 5), msg("assistant", 5), msg("user", 3)]
    out = trim_messages(msgs, 10)
    assert out == [msgs[0], msgs[2], msgs[3]]


def test_3_system_message_is_never_dropped_even_if_it_is_old():
    msgs = [msg("system", 4), msg("user", 6), msg("user", 6)]
    assert trim_messages(msgs, 10)[0]["role"] == "system"


def test_4_kept_history_is_a_contiguous_suffix():
    # the newest message is big; an older small message must not be kept instead
    msgs = [msg("system", 1), msg("user", 1), msg("user", 9)]
    out = trim_messages(msgs, 5)
    assert out == [msgs[0]]


def test_5_system_messages_over_budget_raise():
    with pytest.raises(ValueError):
        trim_messages([msg("system", 10)], 5)


def test_6_original_order_with_system_message_in_the_middle():
    msgs = [msg("user", 1), msg("system", 1), msg("user", 1)]
    assert trim_messages(msgs, 3) == msgs


def test_7_input_untouched_and_total_within_budget():
    msgs = [msg("system", 2)] + [msg("user", 3) for _ in range(6)]
    snap = [dict(m) for m in msgs]
    out = trim_messages(msgs, 12)
    assert sum(len(m["content"].split()) for m in out) <= 12 and msgs == snap
