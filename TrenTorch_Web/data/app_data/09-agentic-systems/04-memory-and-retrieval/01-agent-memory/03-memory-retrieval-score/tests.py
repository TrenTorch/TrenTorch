"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

memory_scores = _module.memory_scores
top_memories = _module.top_memories


def mem(emb, imp, last):
    return {"embedding": emb, "importance": imp, "last_access": last}


def test_1_hand_computed_score():
    m = [mem([1.0, 0.0], 5, 8.0)]
    s = memory_scores(m, [1.0, 0.0], 10.0, 0.5, (1.0, 1.0, 1.0))
    assert math.isclose(s[0], 0.25 + 0.5 + 1.0)


def test_2_recency_decays_with_age():
    ms = [mem([1.0], 5, 10.0), mem([1.0], 5, 0.0)]
    s = memory_scores(ms, [1.0], 10.0, 0.9, (1.0, 0.0, 0.0))
    assert s[0] == 1.0 and s[1] < s[0]


def test_3_importance_dominates_when_only_it_is_weighted():
    ms = [mem([1.0], 2, 0.0), mem([1.0], 9, 0.0)]
    assert top_memories(ms, [1.0], 1.0, 1, 0.9, (0.0, 1.0, 0.0)) == [1]


def test_4_relevance_uses_cosine_and_handles_zero_vectors():
    ms = [mem([1.0, 0.0], 1, 0.0), mem([0.0, 1.0], 1, 0.0), mem([0.0, 0.0], 1, 0.0)]
    s = memory_scores(ms, [1.0, 0.0], 0.0, 1.0, (0.0, 0.0, 1.0))
    assert s == [1.0, 0.0, 0.0]


def test_5_top_k_ordering_and_tie_break():
    ms = [mem([1.0], 5, 0.0), mem([1.0], 5, 0.0), mem([1.0], 9, 0.0)]
    assert top_memories(ms, [1.0], 0.0, 3, 1.0, (0.0, 1.0, 0.0)) == [2, 0, 1]


def test_6_k_larger_than_memory_count():
    assert top_memories([mem([1.0], 1, 0.0)], [1.0], 0.0, 5, 1.0, (1.0, 1.0, 1.0)) == [0]


def test_7_input_untouched():
    ms = [mem([1.0, 2.0], 3, 4.0)]
    snap = [dict(m, embedding=list(m["embedding"])) for m in ms]
    q = [0.5, 0.5]
    top_memories(ms, q, 5.0, 1, 0.9, (1, 1, 1))
    assert ms == snap and q == [0.5, 0.5]
