"""
pytest data/app_data/14-agentic-systems-and-orchestration/01-the-agent-loop/03-decompose-goal-ordered-subtasks/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

order_subtasks = load_solution(
    f"14-agentic-systems-and-orchestration/01-the-agent-loop/{Path(__file__).resolve().parent.name}"
).order_subtasks


def test_1_already_consistent_order_unchanged():
    subtasks = ["A", "B", "C", "D"]
    deps = [("A", "C"), ("B", "C"), ("C", "D")]
    assert order_subtasks(subtasks, deps) == ["A", "B", "C", "D"]


def test_2_tie_break_follows_original_list_order_not_dependency_order():
    subtasks = ["D", "C", "B", "A"]
    deps = [("A", "C"), ("B", "C"), ("C", "D")]
    assert order_subtasks(subtasks, deps) == ["B", "A", "C", "D"]


def test_3_no_dependencies_returns_original_order():
    subtasks = ["x", "y", "z"]
    assert order_subtasks(subtasks, []) == ["x", "y", "z"]


def test_4_single_chain():
    subtasks = ["c", "b", "a"]
    deps = [("a", "b"), ("b", "c")]
    assert order_subtasks(subtasks, deps) == ["a", "b", "c"]


def test_5_single_subtask_no_deps():
    assert order_subtasks(["only"], []) == ["only"]


def test_6_diamond_dependency_shape():
    subtasks = ["start", "left", "right", "end"]
    deps = [("start", "left"), ("start", "right"), ("left", "end"), ("right", "end")]
    result = order_subtasks(subtasks, deps)
    assert result[0] == "start"
    assert result[-1] == "end"
    assert set(result[1:3]) == {"left", "right"}
    assert result.index("left") < result.index("end")
    assert result.index("right") < result.index("end")


def test_7_multiple_independent_chains_interleave_by_original_order():
    subtasks = ["a1", "b1", "a2", "b2"]
    deps = [("a1", "a2"), ("b1", "b2")]
    assert order_subtasks(subtasks, deps) == ["a1", "b1", "a2", "b2"]
