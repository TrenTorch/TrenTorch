"""
pytest data/app_data/14-agentic-systems-and-orchestration/01-the-agent-loop/01-minimal-react-loop/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

run_react_loop = load_solution(
    f"14-agentic-systems-and-orchestration/01-the-agent-loop/{Path(__file__).resolve().parent.name}"
).run_react_loop


def test_1_basic_loop_to_finish():
    steps = [
        ("I need the weather", "get_weather", "Paris"),
        ("Got it", "finish", "It's sunny in Paris"),
    ]
    observations = {("get_weather", "Paris"): "sunny, 22C"}
    assert run_react_loop(steps, observations, 5) == [
        ("I need the weather", "get_weather", "Paris", "sunny, 22C"),
        ("Got it", "finish", "It's sunny in Paris", ""),
    ]


def test_2_step_budget_stops_before_finish():
    steps = [
        ("thought 1", "search", "x"),
        ("thought 2", "finish", "done"),
    ]
    observations = {("search", "x"): "result"}
    assert run_react_loop(steps, observations, 1) == [
        ("thought 1", "search", "x", "result"),
    ]


def test_3_finish_on_the_very_first_step():
    steps = [("already know the answer", "finish", "42")]
    assert run_react_loop(steps, {}, 5) == [("already know the answer", "finish", "42", "")]


def test_4_missing_observation_reported_explicitly():
    steps = [("guessing", "unregistered_tool", "y")]
    assert run_react_loop(steps, {}, 5) == [
        ("guessing", "unregistered_tool", "y", "NO_OBSERVATION_FOUND")
    ]


def test_5_budget_exactly_matches_step_count_no_finish():
    steps = [("t1", "a", "1"), ("t2", "b", "2")]
    observations = {("a", "1"): "o1", ("b", "2"): "o2"}
    assert run_react_loop(steps, observations, 2) == [
        ("t1", "a", "1", "o1"),
        ("t2", "b", "2", "o2"),
    ]


def test_6_multi_step_loop_before_finishing():
    steps = [
        ("t1", "search", "a"),
        ("t2", "search", "b"),
        ("t3", "finish", "answer"),
    ]
    observations = {("search", "a"): "oa", ("search", "b"): "ob"}
    result = run_react_loop(steps, observations, 10)
    assert len(result) == 3
    assert result[-1] == ("t3", "finish", "answer", "")


def test_7_finish_action_never_looked_up_in_observations():
    # A "finish" entry accidentally present in observations must never
    # be consulted -- finishing always short-circuits the lookup.
    steps = [("t1", "finish", "done")]
    observations = {("finish", "done"): "should never be seen"}
    assert run_react_loop(steps, observations, 5) == [("t1", "finish", "done", "")]
