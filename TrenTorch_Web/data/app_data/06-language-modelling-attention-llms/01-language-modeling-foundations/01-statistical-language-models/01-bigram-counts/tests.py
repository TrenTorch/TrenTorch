"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
bigram_counts = _module.bigram_counts


def test_1_symbol_list():
    _, itos = bigram_counts(["ba", "ab"])
    assert itos == [".", "a", "b"]


def test_2_hand_computed_counts():
    counts, itos = bigram_counts(["ab", "ba"])
    # .ab. gives .a ab b. ; .ba. gives .b ba a.
    expected = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    assert np.array_equal(counts, expected)


def test_3_repeated_letter_is_counted_each_time():
    counts, itos = bigram_counts(["aaa"])
    i = itos.index("a")
    assert counts[i, i] == 2 and counts[0, i] == 1 and counts[i, 0] == 1


def test_4_total_is_sum_of_length_plus_one():
    words = ["emma", "olivia", "ava", "mia"]
    counts, _ = bigram_counts(words)
    assert counts.sum() == sum(len(w) + 1 for w in words)


def test_5_matches_independent_pair_oracle():
    from collections import Counter

    words = ["anna", "hannah", "nan", "ann", "a"]
    counts, itos = bigram_counts(words)
    oracle = Counter()
    for w in words:
        s = "." + w + "."
        for k in range(len(s) - 1):
            oracle[(s[k], s[k + 1])] += 1
    for (a, b), n in oracle.items():
        assert counts[itos.index(a), itos.index(b)] == n
    assert counts.sum() == sum(oracle.values())


def test_6_row_zero_is_start_statistics_and_column_zero_is_end():
    counts, itos = bigram_counts(["ab", "ab", "ba"])
    assert counts[0, itos.index("a")] == 2 and counts[0, itos.index("b")] == 1
    assert counts[itos.index("b"), 0] == 2 and counts[itos.index("a"), 0] == 1


def test_7_input_not_modified_and_integer_dtype():
    words = ["ab", "ba"]
    snapshot = list(words)
    counts, _ = bigram_counts(words)
    assert words == snapshot
    assert np.issubdtype(counts.dtype, np.integer)
