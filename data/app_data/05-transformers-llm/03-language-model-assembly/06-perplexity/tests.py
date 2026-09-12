"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/06-perplexity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
perplexity = _module.perplexity
perplexity_from_logits = _module.perplexity_from_logits

next_token_cross_entropy_loss = load_solution(
    "05-transformers-llm/03-language-model-assembly/03-next-token-cross-entropy"
).next_token_cross_entropy_loss


def test_zero_loss_gives_perplexity_one():
    assert np.isclose(perplexity(0.0), 1.0, atol=1e-10)


def test_perplexity_is_exp_of_loss():
    for loss in [0.5, 1.0, 2.3, 5.0]:
        assert np.isclose(perplexity(loss), np.exp(loss), atol=1e-8)


def test_perplexity_is_monotonically_increasing_in_loss():
    assert perplexity(1.0) < perplexity(2.0) < perplexity(3.0)


def test_perplexity_is_always_at_least_one_for_nonnegative_loss():
    for loss in [0.0, 0.1, 10.0]:
        assert perplexity(loss) >= 1.0


def test_uniform_random_guessing_over_v_words_gives_perplexity_close_to_v():
    # A model assigning EQUAL probability to every one of V vocabulary
    # words has cross-entropy loss ln(V), so perplexity exp(ln(V)) = V,
    # the textbook interpretation of perplexity as "effective vocabulary
    # size the model is choosing uniformly among."
    vocab_size, seq_len = 20, 50
    rng = np.random.RandomState(0)
    uniform_logits = np.zeros((seq_len, vocab_size))  # softmax(uniform logits) is uniform
    token_ids = rng.randint(0, vocab_size, size=seq_len)

    result = perplexity_from_logits(uniform_logits, token_ids)
    assert np.isclose(result, vocab_size, atol=1e-6)


def test_perplexity_from_logits_matches_perplexity_of_the_loss():
    rng = np.random.RandomState(1)
    seq_len, vocab_size = 6, 10
    logits = rng.randn(seq_len, vocab_size)
    token_ids = rng.randint(0, vocab_size, size=seq_len)

    loss = next_token_cross_entropy_loss(logits, token_ids)
    expected = perplexity(loss)
    result = perplexity_from_logits(logits, token_ids)
    assert np.isclose(result, expected, atol=1e-8)


def test_confident_correct_predictions_give_perplexity_near_one():
    seq_len, vocab_size = 5, 6
    token_ids = np.array([0, 1, 2, 3, 4])
    logits = np.full((seq_len, vocab_size), -100.0)
    for t in range(seq_len - 1):
        logits[t, token_ids[t + 1]] = 100.0
    result = perplexity_from_logits(logits, token_ids)
    assert result < 1.001
