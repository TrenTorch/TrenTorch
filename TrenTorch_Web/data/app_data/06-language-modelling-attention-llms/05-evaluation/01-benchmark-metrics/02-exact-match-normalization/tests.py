"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
normalize_answer = _module.normalize_answer
exact_match = _module.exact_match
token_f1 = _module.token_f1


def test_1_normalization_steps():
    assert normalize_answer("  The Eiffel   Tower! ") == "eiffel tower"
    assert normalize_answer("A cat, an apple & the dog.") == "cat apple dog"


def test_2_articles_only_removed_as_whole_words():
    assert normalize_answer("theatre and another") == "theatre and another"


def test_3_exact_match_ignores_case_punctuation_and_articles():
    assert exact_match("The Moon.", ["moon"]) == 1.0
    assert exact_match("sun", ["moon"]) == 0.0


def test_4_exact_match_accepts_any_reference():
    assert exact_match("USA", ["United States", "usa"]) == 1.0


def test_5_f1_hand_computed():
    # pred tokens: big red apple (3); gold: red apple (2); overlap 2
    p, r = 2 / 3, 1.0
    assert np.isclose(token_f1("the big red apple", "red apple"), 2 * p * r / (p + r))


def test_6_f1_edge_cases():
    assert token_f1("", "") == 1.0
    assert token_f1("", "x") == 0.0 and token_f1("x", "") == 0.0
    assert token_f1("cat", "dog") == 0.0
    assert token_f1("Paris", "paris.") == 1.0


def test_7_repeated_tokens_do_not_inflate_overlap():
    # pred has 'yes' three times, gold once: overlap 1, P=1/3, R=1
    assert np.isclose(token_f1("yes yes yes", "yes"), 2 * (1 / 3) * 1 / (1 / 3 + 1))
