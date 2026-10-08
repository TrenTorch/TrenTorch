"""
pytest data/app_data/12-research-papers/07-agentic-systems/05-self-consistency/02-agreement-rate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sc-agreement-rate")
agreement_rate = _module.agreement_rate


def test_1_full_agreement_gives_one():
    assert agreement_rate(["x", "x", "x"]) == 1.0


def test_2_all_different_gives_one_over_n():
    assert abs(agreement_rate(["a", "b", "c", "d"]) - 0.25) < 1e-12


def test_3_majority_fraction():
    assert abs(agreement_rate(["a", "a", "a", "b"]) - 0.75) < 1e-12


def test_4_single_answer_gives_one():
    assert agreement_rate(["z"]) == 1.0


def test_5_returns_a_float():
    assert isinstance(agreement_rate(["a", "b"]), float)


def test_6_matches_the_majority_vote_count():
    xs = ["a", "b", "a"]
    assert abs(agreement_rate(xs) - 2 / 3) < 1e-12

