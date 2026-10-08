"""
pytest data/app_data/12-research-papers/07-agentic-systems/10-self-refine/01-refine-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-selfrefine-loop")
refine_loop = _module.refine_loop


def test_1_accepted_draft_is_returned_unchanged():
    assert refine_loop(lambda: "d", lambda y: "OK", lambda y, f: "new", 3) == "d"


def test_2_refines_until_feedback_is_ok():
    fb = lambda y: "OK" if y == "fixed" else "bad"
    assert refine_loop(lambda: "draft", fb, lambda y, f: "fixed", 3) == "fixed"


def test_3_stops_after_the_step_budget():
    out = refine_loop(lambda: 0, lambda y: "bad", lambda y, f: y + 1, 4)
    assert out == 4


def test_4_zero_steps_return_the_first_draft():
    assert refine_loop(lambda: "first", lambda y: "bad", lambda y, f: "x", 0) == "first"


def test_5_refine_receives_the_feedback():
    seen = []
    refine_loop(lambda: "d", lambda y: "please fix", lambda y, f: seen.append(f) or y, 1)
    assert seen == ["please fix"]


def test_6_feedback_on_latest_draft_is_used():
    out = refine_loop(lambda: 1, lambda y: "OK" if y >= 3 else "more", lambda y, f: y + 1, 10)
    assert out == 3

