"""
pytest data/app_data/14-agentic-systems-and-orchestration/01-the-agent-loop/02-stop-loop-step-time-budget/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

find_loop_stop = load_solution(
    f"14-agentic-systems-and-orchestration/01-the-agent-loop/{Path(__file__).resolve().parent.name}"
).find_loop_stop


def test_1_natural_finish_before_any_budget_trips():
    steps = [(1.0, "search"), (2.0, "finish")]
    assert find_loop_stop(steps, max_steps=10, max_seconds=100.0) == (2, "FINISHED")


def test_2_step_budget_trips_first():
    steps = [(1.0, "search"), (2.0, "search"), (3.0, "search")]
    assert find_loop_stop(steps, max_steps=2, max_seconds=100.0) == (2, "STEP_BUDGET")


def test_3_time_budget_trips_first():
    steps = [(1.0, "search"), (50.0, "search")]
    assert find_loop_stop(steps, max_steps=10, max_seconds=40.0) == (2, "TIME_BUDGET")


def test_4_finish_wins_even_on_the_exact_step_budget_step():
    steps = [(1.0, "search"), (2.0, "finish")]
    assert find_loop_stop(steps, max_steps=2, max_seconds=100.0) == (2, "FINISHED")


def test_5_step_budget_checked_before_time_budget():
    # Both would trip on step 2 -- step budget wins per the priority order.
    steps = [(1.0, "search"), (999.0, "search")]
    assert find_loop_stop(steps, max_steps=2, max_seconds=500.0) == (2, "STEP_BUDGET")


def test_6_finish_on_the_very_first_step():
    steps = [(0.5, "finish")]
    assert find_loop_stop(steps, max_steps=10, max_seconds=100.0) == (1, "FINISHED")


def test_7_neither_budget_trips_until_the_last_logged_step():
    steps = [(1.0, "a"), (2.0, "b"), (3.0, "finish")]
    assert find_loop_stop(steps, max_steps=10, max_seconds=100.0) == (3, "FINISHED")


def test_8_time_budget_exactly_equal_counts_as_tripped():
    steps = [(10.0, "search")]
    assert find_loop_stop(steps, max_steps=10, max_seconds=10.0) == (1, "TIME_BUDGET")
