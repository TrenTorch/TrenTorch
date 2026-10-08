"""
pytest data/app_data/12-research-papers/07-agentic-systems/10-self-refine/03-refine-prompt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-selfrefine-prompt")
build_refine_prompt = _module.build_refine_prompt


def test_1_contains_the_task():
    assert "Task: write haiku" in build_refine_prompt("write haiku", "d", "f")


def test_2_contains_the_draft():
    assert "DRAFT_TEXT" in build_refine_prompt("t", "DRAFT_TEXT", "f")


def test_3_contains_the_feedback():
    assert "Feedback: too long" in build_refine_prompt("t", "d", "too long")


def test_4_ends_with_the_rewrite_instruction():
    assert build_refine_prompt("t", "d", "f").endswith("address the feedback.")


def test_5_task_comes_before_draft():
    out = build_refine_prompt("TASKX", "DRAFTX", "f")
    assert out.index("TASKX") < out.index("DRAFTX")


def test_6_returns_a_string():
    assert isinstance(build_refine_prompt("a", "b", "c"), str)

