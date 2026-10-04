"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
trigram_next_distribution = _module.trigram_next_distribution

SENTENCES = [["a", "b"], ["a", "b"], ["a", "c"]]


def test_1_vocab_is_sorted_with_end_marker_and_no_start_marker():
    vocab, _ = trigram_next_distribution(SENTENCES, "<s>", "a")
    assert vocab == ["</s>", "a", "b", "c"]


def test_2_hand_computed_probabilities():
    _, probs = trigram_next_distribution(SENTENCES, "<s>", "a", alpha=1.0)
    # after (<s>, a): b twice, c once => counts [0, 0, 2, 1] + 1 over 3 + 4
    assert np.allclose(probs, np.array([1, 1, 3, 2]) / 7)


def test_3_end_marker_follows_last_token():
    vocab, probs = trigram_next_distribution(SENTENCES, "a", "b", alpha=0.5)
    # (a, b) is followed by </s> twice
    assert vocab[int(np.argmax(probs))] == "</s>"
    assert np.isclose(probs[0], (2 + 0.5) / (2 + 0.5 * 4))


def test_4_unseen_context_is_uniform():
    _, probs = trigram_next_distribution(SENTENCES, "c", "c", alpha=1.0)
    assert np.allclose(probs, 0.25)


def test_5_probabilities_sum_to_one():
    sentences = [["the", "cat", "sat"], ["the", "dog", "sat"], ["a", "cat"]]
    for ctx in [("<s>", "the"), ("the", "cat"), ("cat", "sat"), ("x", "y")]:
        _, probs = trigram_next_distribution(sentences, *ctx, alpha=0.3)
        assert np.isclose(probs.sum(), 1.0)


def test_6_context_changes_the_prediction():
    sentences = [["the", "cat", "sat"], ["the", "dog", "ran"]]
    v, p_cat = trigram_next_distribution(sentences, "the", "cat", alpha=0.01)
    _, p_dog = trigram_next_distribution(sentences, "the", "dog", alpha=0.01)
    assert v[int(np.argmax(p_cat))] == "sat" and v[int(np.argmax(p_dog))] == "ran"


def test_7_matches_independent_oracle_and_leaves_input_alone():
    sentences = [["x", "y", "x"], ["y", "x", "y"], ["x", "y"]]
    snapshot = [list(s) for s in sentences]
    vocab, probs = trigram_next_distribution(sentences, "x", "y", alpha=2.0)
    n = {t: 0 for t in vocab}
    for s in sentences:
        seq = ["<s>", "<s>"] + s + ["</s>"]
        for i in range(len(seq) - 2):
            if seq[i] == "x" and seq[i + 1] == "y":
                n[seq[i + 2]] += 1
    total = sum(n.values())
    for t, p in zip(vocab, probs):
        assert np.isclose(p, (n[t] + 2.0) / (total + 2.0 * len(vocab)))
    assert sentences == snapshot
