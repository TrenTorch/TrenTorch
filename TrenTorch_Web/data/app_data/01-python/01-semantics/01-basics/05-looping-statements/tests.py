"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
countdown_with_skip = _module.countdown_with_skip
find_first_negative = _module.find_first_negative
sum_with_index = _module.sum_with_index
manual_iteration_trace = _module.manual_iteration_trace


def test_countdown_with_skip_correct_sequence():
    assert countdown_with_skip(5) == [5, 4, 2, 1]


def test_countdown_with_skip_no_three_in_range():
    assert countdown_with_skip(2) == [2, 1]


def test_find_first_negative_finds_early_match_via_break():
    # -1 comes first; a later -99 must not be what's returned.
    assert find_first_negative([5, -1, 3, -99]) == -1


def test_find_first_negative_returns_none_via_loop_else():
    assert find_first_negative([1, 2, 3]) is None


def test_find_first_negative_edge_cases():
    assert find_first_negative([]) is None
    assert find_first_negative([-7]) == -7
    assert find_first_negative([7]) is None


def test_sum_with_index_correct_running_totals():
    assert sum_with_index([10, 20, 30]) == {0: 10, 1: 30, 2: 60}


def test_sum_with_index_empty_list():
    assert sum_with_index([]) == {}


def test_manual_iteration_trace_matches_for_loop_behavior():
    items = [1, 2, 3, "four", 5.0]
    assert manual_iteration_trace(items) == items


def test_manual_iteration_trace_handles_stop_iteration_correctly():
    assert manual_iteration_trace([]) == []
    assert manual_iteration_trace([42]) == [42]
