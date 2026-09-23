"""
pytest data/app_data/14-agentic-systems-and-orchestration/01-the-agent-loop/05-detect-repeating-action/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

detect_repeating_action = load_solution(
    f"14-agentic-systems-and-orchestration/01-the-agent-loop/{Path(__file__).resolve().parent.name}"
).detect_repeating_action


def test_1_same_action_three_times_in_a_row():
    actions = [("search", "x"), ("search", "x"), ("search", "x")]
    assert detect_repeating_action(actions, window=5, repeat_threshold=3) == 3


def test_2_different_inputs_never_count_as_the_same_action():
    actions = [("search", "x"), ("search", "y"), ("search", "z")]
    assert detect_repeating_action(actions, window=5, repeat_threshold=2) is None


def test_3_repeat_falls_outside_the_window_never_detected():
    actions = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4"), ("a", "1")]
    # window=2 means only the last 2 steps are ever considered -- the
    # two ("a", "1") calls are 4 apart, never both inside a window of 2.
    assert detect_repeating_action(actions, window=2, repeat_threshold=2) is None


def test_4_threshold_of_one_trips_immediately():
    actions = [("search", "x")]
    assert detect_repeating_action(actions, window=5, repeat_threshold=1) == 1


def test_5_repeats_interleaved_with_other_actions_within_window():
    actions = [("a", "1"), ("b", "2"), ("a", "1"), ("c", "3"), ("a", "1")]
    assert detect_repeating_action(actions, window=5, repeat_threshold=3) == 5


def test_6_window_smaller_than_repeat_threshold_can_never_trip():
    actions = [("a", "1")] * 10
    assert detect_repeating_action(actions, window=2, repeat_threshold=3) is None


def test_7_returns_first_step_where_threshold_is_reached_not_last():
    actions = [("a", "1"), ("a", "1"), ("a", "1"), ("a", "1")]
    assert detect_repeating_action(actions, window=10, repeat_threshold=2) == 2
