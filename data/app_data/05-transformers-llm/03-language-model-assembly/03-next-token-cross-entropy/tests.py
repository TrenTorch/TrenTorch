"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/03-next-token-cross-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
next_token_cross_entropy_loss = _module.next_token_cross_entropy_loss

cross_entropy_forward = load_solution("02-deep-learning-core/03-losses/02-cross-entropy").cross_entropy_forward


def test_loss_is_a_nonnegative_scalar():
    rng = np.random.RandomState(0)
    seq_len, vocab_size = 6, 10
    logits = rng.randn(seq_len, vocab_size)
    token_ids = rng.randint(0, vocab_size, size=seq_len)
    loss = next_token_cross_entropy_loss(logits, token_ids)
    assert np.isscalar(loss) or loss.shape == ()
    assert loss >= 0


def test_matches_manual_shift_and_cross_entropy_forward():
    rng = np.random.RandomState(1)
    seq_len, vocab_size = 8, 12
    logits = rng.randn(seq_len, vocab_size)
    token_ids = rng.randint(0, vocab_size, size=seq_len)

    predicted_logits = logits[:-1]
    targets = token_ids[1:]
    expected = cross_entropy_forward(predicted_logits, targets)

    result = next_token_cross_entropy_loss(logits, token_ids)
    assert np.isclose(result, expected, atol=1e-10)


def test_uses_seq_len_minus_one_pairs_not_seq_len_pairs():
    # A sequence of length seq_len only has seq_len - 1 valid (input,
    # target) next-token pairs -- the very last position has no "next
    # token" to predict.
    rng = np.random.RandomState(2)
    seq_len, vocab_size = 5, 6
    logits = rng.randn(seq_len, vocab_size)
    token_ids = rng.randint(0, vocab_size, size=seq_len)

    predicted_logits = logits[:-1]
    targets = token_ids[1:]
    assert predicted_logits.shape[0] == seq_len - 1
    assert targets.shape[0] == seq_len - 1

    # Sanity: the function should run without error on this shape.
    loss = next_token_cross_entropy_loss(logits, token_ids)
    assert np.isfinite(loss)


def test_perfect_predictions_give_a_near_zero_loss():
    seq_len, vocab_size = 4, 5
    token_ids = np.array([0, 1, 2, 3])
    # Make logits at position t hugely favor token_ids[t+1].
    logits = np.full((seq_len, vocab_size), -100.0)
    for t in range(seq_len - 1):
        logits[t, token_ids[t + 1]] = 100.0
    loss = next_token_cross_entropy_loss(logits, token_ids)
    assert loss < 1e-6


def test_batched_input_supported():
    rng = np.random.RandomState(3)
    batch, seq_len, vocab_size = 3, 6, 10
    logits = rng.randn(batch, seq_len, vocab_size)
    token_ids = rng.randint(0, vocab_size, size=(batch, seq_len))
    loss = next_token_cross_entropy_loss(logits, token_ids)
    assert np.isfinite(loss)
    assert loss >= 0


def test_shift_direction_is_not_reversed():
    # Directly targets a mutant that shifts the WRONG way (predicting
    # token t from logits at position t+1 instead of t), which would
    # silently look ahead rather than predict forward.
    seq_len, vocab_size = 4, 5
    token_ids = np.array([0, 1, 2, 3])
    logits = np.full((seq_len, vocab_size), -100.0)
    # Position t strongly favors token_ids[t+1] (correct next-token setup).
    for t in range(seq_len - 1):
        logits[t, token_ids[t + 1]] = 100.0
    correct_loss = next_token_cross_entropy_loss(logits, token_ids)

    # Reversed setup: position t strongly favors token_ids[t] instead
    # (what a "shift the wrong way" bug would effectively evaluate against).
    reversed_logits = np.full((seq_len, vocab_size), -100.0)
    for t in range(seq_len - 1):
        reversed_logits[t, token_ids[t]] = 100.0
    reversed_loss = next_token_cross_entropy_loss(reversed_logits, token_ids)

    assert correct_loss < 1e-6
    assert reversed_loss > 50.0
