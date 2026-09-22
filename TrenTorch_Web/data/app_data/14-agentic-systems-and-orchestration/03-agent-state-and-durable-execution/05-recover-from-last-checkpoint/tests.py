"""
pytest data/app_data/14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/05-recover-from-last-checkpoint/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

find_recovery_checkpoint = load_solution(
    f"14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/{Path(__file__).resolve().parent.name}"
).find_recovery_checkpoint


def test_1_picks_the_latest_checkpoint_before_the_crash():
    checkpoints = [(1, {"a": 1}), (3, {"a": 3}), (5, {"a": 5})]
    assert find_recovery_checkpoint(checkpoints, crash_step=4) == {"a": 3}


def test_2_exact_match_on_crash_step_is_used():
    checkpoints = [(1, {"a": 1}), (4, {"a": 4})]
    assert find_recovery_checkpoint(checkpoints, crash_step=4) == {"a": 4}


def test_3_no_checkpoint_before_crash_returns_none():
    checkpoints = [(5, {"a": 5}), (10, {"a": 10})]
    assert find_recovery_checkpoint(checkpoints, crash_step=2) is None


def test_4_checkpoints_given_out_of_order_still_found_correctly():
    checkpoints = [(10, {"a": 10}), (2, {"a": 2}), (6, {"a": 6})]
    assert find_recovery_checkpoint(checkpoints, crash_step=7) == {"a": 6}


def test_5_single_checkpoint_qualifies():
    checkpoints = [(3, {"a": 3})]
    assert find_recovery_checkpoint(checkpoints, crash_step=100) == {"a": 3}


def test_6_empty_checkpoint_list_returns_none():
    assert find_recovery_checkpoint([], crash_step=5) is None


def test_7_many_checkpoints_only_the_latest_qualifying_one_wins():
    checkpoints = [(1, {"v": 1}), (2, {"v": 2}), (3, {"v": 3}), (4, {"v": 4})]
    assert find_recovery_checkpoint(checkpoints, crash_step=3) == {"v": 3}
