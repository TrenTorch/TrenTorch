"""
pytest data/app_data/12-research-papers/07-agentic-systems/08-generative-agents/01-recency/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ga-recency-score")
recency_score = _module.recency_score


def test_1_fresh_memory_scores_one():
    assert recency_score(0.0) == 1.0


def test_2_one_hour_multiplies_by_decay():
    assert abs(recency_score(1.0, 0.5) - 0.5) < 1e-12


def test_3_older_memories_score_lower():
    assert recency_score(10.0) < recency_score(1.0)


def test_4_decay_one_never_forgets():
    assert recency_score(100.0, 1.0) == 1.0


def test_5_returns_a_float():
    assert isinstance(recency_score(3.0), float)


def test_6_two_hours_compound():
    assert abs(recency_score(2.0, 0.5) - 0.25) < 1e-12

