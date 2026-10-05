"""pytest tests.py"""

from _load import load_solution

find_cancel_point = load_solution(__file__).find_cancel_point


def test_1_cancel_in_the_middle():
    events = [("chunk", "Hel"), ("chunk", "lo"), ("cancel", ""), ("chunk", "world")]
    assert find_cancel_point(events) == 2


def test_2_no_cancel_returns_none():
    events = [("chunk", "Hel"), ("chunk", "lo"), ("done", "")]
    assert find_cancel_point(events) is None


def test_3_cancel_is_first_event():
    events = [("cancel", ""), ("chunk", "never shown")]
    assert find_cancel_point(events) == 0


def test_4_tool_call_events_are_not_mistaken_for_cancel():
    events = [("chunk", "a"), ("tool_call", "search"), ("chunk", "b"), ("cancel", "")]
    assert find_cancel_point(events) == 3


def test_5_empty_events_returns_none():
    assert find_cancel_point([]) is None
