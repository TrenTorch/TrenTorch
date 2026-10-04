"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
modified_precision = _module.modified_precision
bleu = _module.bleu

REF = "the cat is on the mat".split()


def test_1_clipping_the_classic_example():
    assert np.isclose(modified_precision("the the the the the the the".split(), [REF], 1), 2 / 7)


def test_2_bigram_precision_hand_computed():
    cand = "the cat the cat on the mat".split()
    # bigrams: the cat, cat the, the cat, cat on, on the, the mat
    # ref has: the cat, cat is, is on, on the, the mat -> matches: the cat (clip 1), on the, the mat
    assert np.isclose(modified_precision(cand, [REF], 2), 3 / 6)


def test_3_identical_sentence_scores_one():
    assert np.isclose(bleu(REF, [REF]), 1.0)


def test_4_brevity_penalty():
    ref = "a b c d e f g h".split()
    cand = "a b c d".split()
    # all n-gram precisions are 1, BP = exp(1 - 8/4)
    assert np.isclose(bleu(cand, [ref], max_n=2), np.exp(1 - 8 / 4))


def test_5_zero_precision_gives_zero():
    assert bleu("x y z w".split(), [REF]) == 0.0


def test_6_multiple_references_use_best_clip_and_closest_length():
    refs = ["a b c".split(), "a b c d e f".split()]
    cand = "a b c d e".split()
    # closest ref length to 5 is 6 -> BP = exp(1 - 6/5); unigram precision uses ref 2
    assert np.isclose(modified_precision(cand, refs, 1), 1.0)
    assert np.isclose(bleu(cand, refs, max_n=1), np.exp(1 - 6 / 5))


def test_7_matches_independent_computation_and_inputs_untouched():
    cand = "the cat sat on the mat".split()
    refs = ["the cat is on the mat".split()]
    cs, rs = list(cand), [list(refs[0])]
    # unigrams matching: the cat on the mat (5 of 6); bigrams: the cat, on the, the mat (3 of 5)
    # trigrams: the cat sat, cat sat on, sat on the, on the mat -> only 'on the mat' matches (1 of 4)
    p = [5 / 6, 3 / 5, 1 / 4, 0.0]
    assert bleu(cand, refs) == 0.0
    assert np.isclose(bleu(cand, refs, max_n=3), np.exp(np.mean(np.log(p[:3]))))
    assert cand == cs and refs == rs
