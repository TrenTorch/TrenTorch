"""
pytest data/app_data/12-research-papers/07-agentic-systems/07-voyager/03-next-task/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-voyager-next-task")
next_task = _module.next_task


def test_1_skips_completed_tasks():
    assert next_task({"a"}, ["a", "b", "c"]) == "b"


def test_2_all_done_returns_none():
    assert next_task({"a", "b"}, ["a", "b"]) is None


def test_3_nothing_done_returns_the_first():
    assert next_task(set(), ["x", "y"]) == "x"


def test_4_empty_candidates_return_none():
    assert next_task(set(), []) is None


def test_5_curriculum_order_is_respected():
    assert next_task({"b"}, ["c", "a", "b"]) == "c"


def test_6_does_not_mutate_done():
    done = {"a"}
    next_task(done, ["a", "b"])
    assert done == {"a"}

