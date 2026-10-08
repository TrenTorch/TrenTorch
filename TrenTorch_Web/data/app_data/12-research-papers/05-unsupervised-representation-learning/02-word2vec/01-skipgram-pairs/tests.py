"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/02-word2vec/01-skipgram-pairs/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-w2v-skipgram-pairs")
skipgram_pairs = _module.skipgram_pairs


def test_1_window_one_on_three_words_gives_four_pairs():
    assert len(skipgram_pairs(["a", "b", "c"], 1)) == 4


def test_2_pairs_match_a_hand_case():
    assert skipgram_pairs(["a", "b", "c"], 1) == [("a", "b"), ("b", "a"), ("b", "c"), ("c", "b")]


def test_3_zero_window_gives_no_pairs():
    assert skipgram_pairs(["a", "b"], 0) == []


def test_4_large_window_pairs_every_distinct_pair():
    assert len(skipgram_pairs(["a", "b", "c"], 5)) == 6


def test_5_a_word_is_never_its_own_context():
    assert all(c != x for c, x in skipgram_pairs(["a", "b", "c"], 2))


def test_6_does_not_mutate_tokens():
    t = ["a", "b"]
    skipgram_pairs(t, 1)
    assert t == ["a", "b"]

