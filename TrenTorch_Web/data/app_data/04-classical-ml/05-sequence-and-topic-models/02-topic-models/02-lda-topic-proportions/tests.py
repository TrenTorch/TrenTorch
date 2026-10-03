"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
lda_estimates = _module.lda_estimates

DOC_TOPIC = np.array([[3.0, 1.0], [0.0, 0.0]])
TOPIC_WORD = np.array([[2.0, 0.0, 2.0], [1.0, 1.0, 0.0]])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_theta_hand_value_for_first_document():
    theta, _ = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1.0, beta=1.0)
    # Row (3, 1) with alpha = 1 gives ((3+1)/(4+2), (1+1)/(4+2)) = (2/3, 1/3).
    assert np.allclose(theta[0], [2 / 3, 1 / 3])


def test_theta_for_empty_document_is_uniform():
    theta, _ = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=0.5, beta=1.0)
    assert np.allclose(theta[1], [0.5, 0.5])


def test_phi_hand_value_for_first_topic():
    _, phi = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1.0, beta=1.0)
    # Row (2, 0, 2) with beta = 1 gives (3, 1, 3) / 7.
    assert np.allclose(phi[0], [3 / 7, 1 / 7, 3 / 7])


def test_theta_rows_sum_to_one():
    theta, _ = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=0.3, beta=0.1)
    assert np.allclose(theta.sum(axis=1), 1.0)


def test_phi_rows_sum_to_one():
    _, phi = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=0.3, beta=0.1)
    assert np.allclose(phi.sum(axis=1), 1.0)


def test_output_shapes():
    theta, phi = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1.0, beta=1.0)
    assert theta.shape == (2, 2) and phi.shape == (2, 3)


def test_no_zero_probabilities_even_for_unseen_pairs():
    _, phi = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1.0, beta=0.5)
    assert np.all(phi > 0)


def test_large_prior_pushes_theta_towards_uniform():
    theta, _ = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1e6, beta=1.0)
    assert np.allclose(theta[0], [0.5, 0.5], atol=1e-3)


def test_small_alpha_keeps_document_concentrated_on_dominant_topic():
    theta, _ = lda_estimates(DOC_TOPIC, TOPIC_WORD, alpha=1e-6, beta=1.0)
    assert theta[0, 0] > 0.7


def test_phi_uses_vocabulary_size_in_denominator():
    tw = np.array([[0.0, 0.0, 0.0, 0.0]])
    _, phi = lda_estimates(np.ones((1, 1)), tw, alpha=1.0, beta=2.0)
    assert np.allclose(phi, 0.25)


def test_negative_count_raises():
    bad = np.array([[-1.0, 1.0], [0.0, 0.0]])
    assert _raises_value_error(lda_estimates, bad, TOPIC_WORD, 1.0, 1.0)


def test_nonpositive_prior_raises():
    assert _raises_value_error(lda_estimates, DOC_TOPIC, TOPIC_WORD, 0.0, 1.0)


def test_topic_count_mismatch_raises():
    assert _raises_value_error(lda_estimates, np.ones((2, 3)), TOPIC_WORD, 1.0, 1.0)


def test_inputs_are_not_modified():
    doc = DOC_TOPIC.copy()
    tw = TOPIC_WORD.copy()
    lda_estimates(doc, tw, 1.0, 1.0)
    assert np.array_equal(doc, DOC_TOPIC) and np.array_equal(tw, TOPIC_WORD)
