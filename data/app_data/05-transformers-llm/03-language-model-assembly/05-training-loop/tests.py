"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/05-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
train_output_head_one_step = _module.train_output_head_one_step
train_output_head = _module.train_output_head

next_token_cross_entropy_loss = load_solution(
    "05-transformers-llm/03-language-model-assembly/03-next-token-cross-entropy"
).next_token_cross_entropy_loss
output_projection = load_solution("05-transformers-llm/03-language-model-assembly/01-output-projection").output_projection


def test_one_step_returns_a_weight_of_the_same_shape_and_a_scalar_loss():
    rng = np.random.RandomState(0)
    vocab_size, d_model, seq_len = 12, 6, 5
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model)

    new_weight, loss = train_output_head_one_step(hidden_states, token_ids, output_weight, lr=0.01)
    assert new_weight.shape == output_weight.shape
    assert np.isfinite(loss)
    assert loss >= 0


def test_reported_loss_matches_the_loss_before_the_update():
    rng = np.random.RandomState(1)
    vocab_size, d_model, seq_len = 10, 5, 4
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model)

    logits_before = output_projection(hidden_states, output_weight)
    expected_loss = next_token_cross_entropy_loss(logits_before, token_ids)

    _, reported_loss = train_output_head_one_step(hidden_states, token_ids, output_weight, lr=0.01)
    assert np.isclose(reported_loss, expected_loss, atol=1e-8)


def test_a_large_enough_lr_step_changes_the_weight():
    rng = np.random.RandomState(2)
    vocab_size, d_model, seq_len = 10, 5, 4
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model)

    new_weight, _ = train_output_head_one_step(hidden_states, token_ids, output_weight, lr=0.1)
    assert not np.allclose(new_weight, output_weight, atol=1e-6)


def test_zero_lr_leaves_the_weight_unchanged():
    rng = np.random.RandomState(3)
    vocab_size, d_model, seq_len = 10, 5, 4
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model)

    new_weight, _ = train_output_head_one_step(hidden_states, token_ids, output_weight, lr=0.0)
    assert np.allclose(new_weight, output_weight, atol=1e-10)


def test_loss_decreases_over_repeated_steps_on_the_same_batch():
    # A genuine gradient-descent step, run repeatedly on the same fixed
    # batch, should reduce the loss on that exact batch (the classic
    # "can it overfit one batch" sanity check).
    rng = np.random.RandomState(4)
    vocab_size, d_model, seq_len = 15, 8, 6
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model) * 0.1

    _, loss_history = train_output_head(hidden_states, token_ids, output_weight, lr=0.5, num_steps=50)
    assert len(loss_history) == 50
    assert loss_history[-1] < loss_history[0]


def test_gradient_direction_reduces_loss_not_increases_it():
    # Directly targets a mutant that adds instead of subtracts the
    # gradient (gradient ASCENT instead of descent), which would make
    # the loss increase instead of decrease.
    rng = np.random.RandomState(5)
    vocab_size, d_model, seq_len = 10, 5, 4
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model) * 0.1

    logits_before = output_projection(hidden_states, output_weight)
    loss_before = next_token_cross_entropy_loss(logits_before, token_ids)

    new_weight, _ = train_output_head_one_step(hidden_states, token_ids, output_weight, lr=0.1)
    logits_after = output_projection(hidden_states, new_weight)
    loss_after = next_token_cross_entropy_loss(logits_after, token_ids)

    assert loss_after < loss_before
