"""pytest data/app_data/15-reliability-safety-and-evaluation/03-agent-observability/05-replay-until-failure/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

replay_until_failure = load_solution(
    f"15-reliability-safety-and-evaluation/03-agent-observability/{Path(__file__).resolve().parent.name}"
).replay_until_failure


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
