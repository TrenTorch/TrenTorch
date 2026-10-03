"""
pytest tests.py
"""

import math
from _load import load_solution

_module = load_solution(__file__)
distinct_n = _module.distinct_n
corpus_distinct_n = _module.corpus_distinct_n


def test_1_hand_computed():
    assert math.isclose(distinct_n("a b a b a".split(), 1), 2 / 5)


def test_2_bigrams_hand_computed():
    # bigrams: ab, ba, ab, ba -> 2 unique of 4
    assert math.isclose(distinct_n("a b a b a".split(), 2), 2 / 4)


def test_3_no_repetition_gives_one():
    assert distinct_n("a b c d".split(), 2) == 1.0


def test_4_too_short_for_n_gives_zero():
    assert distinct_n(["a"], 2) == 0.0 and distinct_n([], 1) == 0.0


def test_5_pooled_diversity_is_low_when_samples_repeat_each_other():
    same = [["a", "b", "c"]] * 4
    diff = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"], ["j", "k", "l"]]
    assert math.isclose(corpus_distinct_n(same, 1), 3 / 12)
    assert corpus_distinct_n(diff, 1) == 1.0


def test_6_ngrams_do_not_span_sample_boundaries():
    # if they did, "b c" would appear as a bigram across ["a b"] and ["c d"]
    samples = [["a", "b"], ["c", "d"]]
    assert corpus_distinct_n(samples, 2) == 1.0 and len({("b", "c")} & set()) == 0
    assert math.isclose(corpus_distinct_n([["b", "c"], ["b", "c"]], 2), 1 / 2)


def test_7_corpus_of_one_sample_equals_distinct_n_and_inputs_untouched():
    s = "to be or not to be".split()
    snap = list(s)
    assert math.isclose(corpus_distinct_n([s], 2), distinct_n(s, 2))
    assert s == snap
