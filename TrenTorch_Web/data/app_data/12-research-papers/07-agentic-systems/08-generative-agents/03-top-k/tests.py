"""
pytest data/app_data/12-research-papers/07-agentic-systems/08-generative-agents/03-top-k/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ga-top-k")
top_k_memories = _module.top_k_memories


def test_1_returns_the_best_names():
    assert top_k_memories([("a", 0.1), ("b", 0.9), ("c", 0.5)], 2) == ["b", "c"]


def test_2_k_larger_than_memory_returns_everything():
    assert top_k_memories([("a", 1.0)], 5) == ["a"]


def test_3_k_zero_returns_nothing():
    assert top_k_memories([("a", 1.0)], 0) == []


def test_4_output_is_best_first():
    assert top_k_memories([("x", 2.0), ("y", 3.0)], 2) == ["y", "x"]


def test_5_empty_memory_returns_empty():
    assert top_k_memories([], 3) == []


def test_6_does_not_mutate_input():
    m = [("a", 1.0), ("b", 2.0)]
    top_k_memories(m, 1)
    assert m == [("a", 1.0), ("b", 2.0)]

