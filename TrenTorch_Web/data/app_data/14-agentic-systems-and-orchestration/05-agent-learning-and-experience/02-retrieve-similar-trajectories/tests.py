"""
pytest data/app_data/14-agentic-systems-and-orchestration/05-agent-learning-and-experience/02-retrieve-similar-trajectories/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

find_similar_trajectories = load_solution(
    f"14-agentic-systems-and-orchestration/05-agent-learning-and-experience/{Path(__file__).resolve().parent.name}"
).find_similar_trajectories


def test_1_ranked_by_overlap_count_descending():
    trajectories = [
        ("t1", {"booking", "flight"}),
        ("t2", {"booking", "flight", "hotel"}),
        ("t3", {"weather"}),
    ]
    query = {"booking", "flight", "hotel"}
    assert find_similar_trajectories(query, trajectories) == ["t2", "t1", "t3"]


def test_2_zero_overlap_still_included_at_the_end():
    trajectories = [("t1", {"a", "b"}), ("t2", {"z"})]
    assert find_similar_trajectories({"a", "b"}, trajectories) == ["t1", "t2"]


def test_3_exact_tie_broken_by_ascending_id():
    trajectories = [("z", {"a"}), ("a", {"a"}), ("m", {"a"})]
    assert find_similar_trajectories({"a"}, trajectories) == ["a", "m", "z"]


def test_4_empty_query_tags_gives_zero_overlap_for_everyone():
    trajectories = [("t2", {"x"}), ("t1", {"y"})]
    assert find_similar_trajectories(set(), trajectories) == ["t1", "t2"]


def test_5_no_stored_trajectories():
    assert find_similar_trajectories({"a"}, []) == []


def test_6_partial_overlap_ranks_between_full_and_none():
    trajectories = [
        ("full", {"a", "b", "c"}),
        ("partial", {"a", "x", "y"}),
        ("none", {"x", "y", "z"}),
    ]
    assert find_similar_trajectories({"a", "b", "c"}, trajectories) == [
        "full",
        "partial",
        "none",
    ]
