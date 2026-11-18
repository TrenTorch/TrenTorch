"""
pytest tests.py
"""

from _load import load_solution

classify_and_store = load_solution(__file__).classify_and_store


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
