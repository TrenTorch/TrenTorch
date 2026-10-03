"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
topic_conditional = _module.topic_conditional

TOPIC_WORD = np.array([[3.0, 0.0], [0.0, 0.0]])
TOTALS = np.array([3.0, 0.0])
ZERO_DOC = np.zeros(2)


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_matches_closed_form():
    # Unnormalized: topic 0 -> (0+1)(3+1)/(3+2) = 4/5, topic 1 -> (0+1)(0+1)/(0+2) = 1/2.
    p = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 1.0, 0)
    assert np.allclose(p, [8 / 13, 5 / 13])


def test_output_sums_to_one():
    p = topic_conditional(np.array([2.0, 1.0]), TOPIC_WORD, TOTALS, 0.5, 0.1, 0)
    assert np.isclose(p.sum(), 1.0)


def test_output_length_is_number_of_topics():
    p = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 1.0, 1)
    assert p.shape == (2,)


def test_document_counts_favour_topics_already_in_the_document():
    base = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 1.0, 0)
    skewed = topic_conditional(np.array([0.0, 5.0]), TOPIC_WORD, TOTALS, 1.0, 1.0, 0)
    assert skewed[1] > base[1]


def test_word_counts_favour_topics_that_use_the_word():
    p = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 1.0, 0)
    assert p[0] > p[1]


def test_word_unseen_in_every_topic_gives_uniform_word_factor():
    tw = np.array([[0.0, 0.0], [0.0, 0.0]])
    p = topic_conditional(ZERO_DOC, tw, np.zeros(2), 1.0, 1.0, 1)
    assert np.allclose(p, [0.5, 0.5])


def test_large_alpha_leaves_only_the_word_term():
    # The document factor becomes flat, so the conditional follows the word term alone: 4/5 vs 1/2.
    doc = np.array([10.0, 0.0])
    p_big = topic_conditional(doc, TOPIC_WORD, TOTALS, 1e6, 1.0, 0)
    assert np.allclose(p_big, [8 / 13, 5 / 13], atol=1e-3)


def test_beta_scales_the_word_term():
    small = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 0.01, 0)
    large = topic_conditional(ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 10.0, 0)
    assert small[0] > large[0]


def test_denominator_uses_vocabulary_size():
    tw = np.array([[1.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
    tot = np.array([3.0, 0.0])
    p = topic_conditional(np.zeros(2), tw, tot, 1.0, 1.0, 0)
    # Topic 0: (1+1)/(3 + 3) = 1/3. Topic 1: (0+1)/(0 + 3) = 1/3. Equal after normalization.
    assert np.allclose(p, [0.5, 0.5])


def test_probabilities_are_nonnegative():
    rng = np.random.default_rng(0)
    tw = rng.integers(0, 5, size=(4, 6)).astype(float)
    tot = tw.sum(axis=1)
    p = topic_conditional(rng.integers(0, 3, size=4).astype(float), tw, tot, 0.3, 0.1, 2)
    assert np.all(p >= 0) and np.isclose(p.sum(), 1.0)


def test_nonpositive_alpha_raises():
    assert _raises_value_error(topic_conditional, ZERO_DOC, TOPIC_WORD, TOTALS, 0.0, 1.0, 0)


def test_nonpositive_beta_raises():
    assert _raises_value_error(topic_conditional, ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, -0.1, 0)


def test_word_out_of_range_raises():
    assert _raises_value_error(topic_conditional, ZERO_DOC, TOPIC_WORD, TOTALS, 1.0, 1.0, 2)


def test_negative_count_raises():
    assert _raises_value_error(topic_conditional, np.array([-1.0, 0.0]), TOPIC_WORD, TOTALS, 1.0, 1.0, 0)


def test_shape_mismatch_raises():
    assert _raises_value_error(topic_conditional, np.zeros(3), TOPIC_WORD, TOTALS, 1.0, 1.0, 0)


def test_inputs_are_not_modified():
    doc = np.array([2.0, 1.0])
    tw = TOPIC_WORD.copy()
    topic_conditional(doc, tw, TOTALS, 1.0, 1.0, 0)
    assert np.array_equal(tw, TOPIC_WORD) and np.array_equal(doc, [2.0, 1.0])
