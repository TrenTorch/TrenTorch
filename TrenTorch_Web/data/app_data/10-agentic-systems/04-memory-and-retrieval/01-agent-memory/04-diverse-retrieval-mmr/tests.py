"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
mmr_select = _module.mmr_select
DOCS = [[1.0, 0.0], [0.99, 0.14], [0.0, 1.0]]
Q = [1.0, 0.3]


def test_1_lambda_one_is_plain_top_k_relevance():
    assert mmr_select(Q, DOCS, 2, 1.0) == [1, 0]


def test_2_diversity_prefers_a_different_document_over_a_duplicate():
    out = mmr_select(Q, DOCS, 2, 0.5)
    assert out[0] == 1 and out[1] == 2


def test_3_first_pick_is_the_most_relevant():
    assert mmr_select(Q, DOCS, 1, 0.1)[0] == 1


def test_4_k_larger_than_corpus_returns_everything_once():
    out = mmr_select(Q, DOCS, 10, 0.5)
    assert sorted(out) == [0, 1, 2]


def test_5_pure_diversity_ends_with_the_most_redundant():
    out = mmr_select([1.0, 0.0], [[1.0, 0.0], [1.0, 0.01], [0.0, 1.0]], 3, 0.0)
    assert out == [0, 2, 1]


def test_6_ties_prefer_lower_index():
    assert mmr_select([1.0], [[1.0], [1.0]], 2, 1.0) == [0, 1]


def test_7_empty_and_inputs_untouched():
    assert mmr_select([1.0], [], 3, 0.5) == []
    docs = [[1.0, 2.0], [3.0, 4.0]]
    snap = [list(d) for d in docs]
    mmr_select([1.0, 1.0], docs, 2, 0.5)
    assert docs == snap
