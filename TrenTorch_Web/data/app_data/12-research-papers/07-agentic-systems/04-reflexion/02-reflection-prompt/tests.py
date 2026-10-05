"""
pytest data/app_data/12-research-papers/07-agentic-systems/04-reflexion/02-reflection-prompt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-reflexion-prompt")
build_reflection_prompt = _module.build_reflection_prompt


def test_1_contains_the_task():
    assert "Task: sort list" in build_reflection_prompt("sort list", "t", "f")


def test_2_contains_the_feedback():
    assert "Feedback: wrong order" in build_reflection_prompt("t", "x", "wrong order")


def test_3_contains_the_trajectory():
    assert "Search[a]" in build_reflection_prompt("t", "Search[a]", "f")


def test_4_ends_with_the_reflection_instruction():
    assert build_reflection_prompt("t", "x", "f").endswith("what to do differently.")


def test_5_fields_appear_in_order():
    out = build_reflection_prompt("T", "TRAJ", "FB")
    assert out.index("Task:") < out.index("TRAJ") < out.index("Feedback:")


def test_6_returns_a_string():
    assert isinstance(build_reflection_prompt("a", "b", "c"), str)

