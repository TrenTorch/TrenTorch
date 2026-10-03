"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
char_ngrams = _module.char_ngrams
subword_embedding = _module.subword_embedding


def test_1_ngrams_of_where():
    assert char_ngrams("where", 3, 3) == ["<wh", "whe", "her", "ere", "re>", "<where>"]


def test_2_ordering_by_n_then_position():
    assert char_ngrams("ab", 2, 3) == ["<a", "ab", "b>", "<ab", "ab>", "<ab>"]


def test_3_whole_word_not_duplicated_when_in_range():
    grams = char_ngrams("a", 3, 3)
    assert grams == ["<a>"]


def test_4_short_word_with_large_n_only_has_the_whole_word():
    assert char_ngrams("hi", 5, 6) == ["<hi>"]


def test_5_embedding_is_the_mean_of_known_ngrams():
    table = {"<a": np.array([1.0, 0.0]), "ab": np.array([0.0, 1.0]), "zz": np.array([9.0, 9.0])}
    assert np.allclose(subword_embedding("ab", table, 2, 2, 2), [0.5, 0.5])


def test_6_unknown_word_with_no_known_ngrams_is_zero():
    assert np.allclose(subword_embedding("qq", {"zz": np.ones(3)}, 2, 3, 3), np.zeros(3))


def test_7_related_unseen_words_share_vectors_and_input_untouched():
    rng = np.random.RandomState(0)
    table = {g: rng.randn(8) for g in char_ngrams("happiness", 3, 4)}
    snap = {k: v.copy() for k, v in table.items()}
    a = subword_embedding("happiness", table, 3, 4, 8)
    b = subword_embedding("happily", table, 3, 4, 8)  # never seen, shares "<ha", "hap", "app", "<hap", "happ"
    cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
    assert cos > 0.3 and all(np.array_equal(table[k], snap[k]) for k in table)
