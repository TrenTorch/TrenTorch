"""
pytest data/app_data/14-agentic-systems-and-orchestration/05-agent-learning-and-experience/01-store-trajectories/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

classify_and_store = load_solution(
    f"14-agentic-systems-and-orchestration/05-agent-learning-and-experience/{Path(__file__).resolve().parent.name}"
).classify_and_store


def test_1_mixed_successes_and_failures():
    trajectories = [("t1", True), ("t2", False), ("t3", True)]
    assert classify_and_store(trajectories) == (["t1", "t3"], ["t2"])


def test_2_all_successful():
    trajectories = [("t1", True), ("t2", True)]
    assert classify_and_store(trajectories) == (["t1", "t2"], [])


def test_3_all_failed():
    trajectories = [("t1", False), ("t2", False)]
    assert classify_and_store(trajectories) == ([], ["t1", "t2"])


def test_4_empty_input():
    assert classify_and_store([]) == ([], [])


def test_5_order_preserved_within_each_list():
    trajectories = [("a", False), ("b", True), ("c", False), ("d", True)]
    assert classify_and_store(trajectories) == (["b", "d"], ["a", "c"])


def test_6_single_trajectory():
    assert classify_and_store([("only", True)]) == (["only"], [])
