"""
pytest data/app_data/12-research-papers/07-agentic-systems/05-self-consistency/01-majority-vote/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sc-majority-vote")
majority_vote = _module.majority_vote


def test_1_most_common_answer_wins():
    assert majority_vote(["a", "b", "a"]) == "a"


def test_2_tie_goes_to_the_first_seen():
    assert majority_vote(["a", "b"]) == "a"


def test_3_single_answer_is_returned():
    assert majority_vote(["only"]) == "only"


def test_4_tie_at_top_goes_to_earliest_top_answer():
    assert majority_vote(["b", "a", "a", "b", "c"]) == "b"


def test_5_works_with_numbers():
    assert majority_vote([3, 3, 4]) == 3


def test_6_does_not_mutate_input():
    xs = ["a", "b"]
    majority_vote(xs)
    assert xs == ["a", "b"]

