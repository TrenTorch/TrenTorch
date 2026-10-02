"""pytest tests.py"""

from _load import load_solution

replay_until_failure = load_solution(__file__).replay_until_failure


def test_1_all_steps_succeed_returns_all_names():
    steps = [("plan", True), ("search", True), ("respond", True)]
    assert replay_until_failure(steps) == ["plan", "search", "respond"]


def test_2_stops_at_first_failure_inclusive():
    steps = [("plan", True), ("search", False), ("respond", True)]
    assert replay_until_failure(steps) == ["plan", "search"]


def test_3_failure_on_first_step():
    steps = [("plan", False), ("search", True)]
    assert replay_until_failure(steps) == ["plan"]


def test_4_empty_steps_returns_empty_list():
    assert replay_until_failure([]) == []


def test_5_multiple_failures_stops_at_the_first_one():
    steps = [("a", True), ("b", False), ("c", False), ("d", True)]
    assert replay_until_failure(steps) == ["a", "b"]
