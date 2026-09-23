"""
pytest data/app_data/14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/04-pause-and-resume-agent-run/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

compute_remaining_steps = load_solution(
    f"14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/{Path(__file__).resolve().parent.name}"
).compute_remaining_steps


def test_1_clean_resume_partway_through():
    full_plan = ["fetch_data", "clean_data", "train_model", "report"]
    completed = ["fetch_data", "clean_data"]
    assert compute_remaining_steps(full_plan, completed) == ["train_model", "report"]


def test_2_nothing_completed_yet():
    full_plan = ["a", "b", "c"]
    assert compute_remaining_steps(full_plan, []) == ["a", "b", "c"]


def test_3_everything_already_completed():
    full_plan = ["a", "b"]
    assert compute_remaining_steps(full_plan, ["a", "b"]) == []


def test_4_mismatch_wrong_step_at_a_position():
    full_plan = ["a", "b", "c"]
    completed = ["a", "x"]
    assert compute_remaining_steps(full_plan, completed) == "STATE_MISMATCH"


def test_5_mismatch_completed_longer_than_plan():
    full_plan = ["a", "b"]
    completed = ["a", "b", "c"]
    assert compute_remaining_steps(full_plan, completed) == "STATE_MISMATCH"


def test_6_mismatch_completed_steps_out_of_order():
    full_plan = ["a", "b", "c"]
    completed = ["b", "a"]
    assert compute_remaining_steps(full_plan, completed) == "STATE_MISMATCH"


def test_7_single_step_plan_fully_completed():
    assert compute_remaining_steps(["only"], ["only"]) == []
