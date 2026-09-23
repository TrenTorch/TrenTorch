"""
pytest data/app_data/14-agentic-systems-and-orchestration/01-the-agent-loop/04-self-reflection-critique-last-step/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

find_abandon_point = load_solution(
    f"14-agentic-systems-and-orchestration/01-the-agent-loop/{Path(__file__).resolve().parent.name}"
).find_abandon_point


def test_1_two_consecutive_failures_trigger_abandon():
    observations = ["error: timeout", "error: timeout"]
    assert find_abandon_point(observations, ["error"], 2) == 2


def test_2_a_success_in_between_resets_the_streak():
    observations = ["error: timeout", "success: got data", "error: timeout"]
    assert find_abandon_point(observations, ["error"], 2) is None


def test_3_never_reaches_threshold_returns_none():
    observations = ["ok", "ok", "ok"]
    assert find_abandon_point(observations, ["error"], 3) is None


def test_4_threshold_of_one_trips_on_first_failure():
    observations = ["all good", "error: failed"]
    assert find_abandon_point(observations, ["error"], 1) == 2


def test_5_multiple_keywords_any_one_counts():
    observations = ["timeout occurred", "connection refused", "success"]
    assert find_abandon_point(observations, ["timeout", "refused"], 2) == 2


def test_6_streak_spanning_more_than_the_threshold_stops_at_threshold_not_the_end():
    observations = ["error", "error", "error", "error"]
    assert find_abandon_point(observations, ["error"], 2) == 2


def test_7_case_sensitive_matching():
    observations = ["ERROR: failed", "ERROR: failed"]
    assert find_abandon_point(observations, ["error"], 2) is None


def test_8_streak_resets_and_rebuilds_before_finally_tripping():
    observations = ["error", "ok", "error", "error"]
    assert find_abandon_point(observations, ["error"], 2) == 4
