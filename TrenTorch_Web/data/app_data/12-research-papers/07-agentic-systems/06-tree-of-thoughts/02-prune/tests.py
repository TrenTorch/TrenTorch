"""
pytest data/app_data/12-research-papers/07-agentic-systems/06-tree-of-thoughts/02-prune/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tot-prune")
prune_below = _module.prune_below


def test_1_score_above_threshold_is_kept():
    assert prune_below(0.9, 0.5) is True


def test_2_score_below_threshold_is_pruned():
    assert prune_below(0.1, 0.5) is False


def test_3_equal_score_is_kept():
    assert prune_below(0.5, 0.5) is True


def test_4_negative_scores_work():
    assert prune_below(-1.0, -2.0) is True


def test_5_returns_a_bool():
    assert isinstance(prune_below(1.0, 0.0), bool)


def test_6_threshold_zero_keeps_nonnegative_scores():
    assert prune_below(0.0, 0.0) is True

