"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/07-gradient-accumulation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
compute_output_head_gradient = _module.compute_output_head_gradient
accumulate_gradients = _module.accumulate_gradients
train_with_gradient_accumulation = _module.train_with_gradient_accumulation


def test_accumulate_gradients_is_the_elementwise_mean():
    grads = [np.array([2.0, 4.0]), np.array([4.0, 8.0]), np.array([6.0, 12.0])]
    result = accumulate_gradients(grads)
    assert np.allclose(result, [4.0, 8.0], atol=1e-10)


def test_compute_output_head_gradient_returns_grad_and_loss():
    rng = np.random.RandomState(0)
    vocab_size, d_model, seq_len = 10, 5, 4
    hidden_states = rng.randn(1, seq_len, d_model)
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    output_weight = rng.randn(vocab_size, d_model)

    grad, loss = compute_output_head_gradient(hidden_states, token_ids, output_weight)
    assert grad.shape == output_weight.shape
    assert loss >= 0


def test_gradient_accumulation_over_equal_sized_microbatches_matches_the_full_batch_gradient():
    # The core correctness property: averaging N equal-sized micro-batches'
    # OWN mean gradients must equal the gradient computed directly on the
    # full concatenated batch (a nested average of equal-sized groups
    # equals the overall average).
    rng = np.random.RandomState(1)
    vocab_size, d_model, seq_len = 12, 6, 5
    output_weight = rng.randn(vocab_size, d_model)

    micro_batches = []
    all_hidden = []
    all_tokens = []
    for _ in range(3):
        hidden_states = rng.randn(1, seq_len, d_model)
        token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
        micro_batches.append((hidden_states, token_ids))
        all_hidden.append(hidden_states)
        all_tokens.append(token_ids)

    gradients = [compute_output_head_gradient(h, t, output_weight)[0] for h, t in micro_batches]
    accumulated = accumulate_gradients(gradients)

    full_hidden = np.concatenate(all_hidden, axis=0)
    full_tokens = np.concatenate(all_tokens, axis=0)
    full_grad, _ = compute_output_head_gradient(full_hidden, full_tokens, output_weight)

    assert np.allclose(accumulated, full_grad, atol=1e-6)


def test_train_with_gradient_accumulation_applies_exactly_one_update():
    rng = np.random.RandomState(2)
    vocab_size, d_model, seq_len = 10, 5, 4
    output_weight = rng.randn(vocab_size, d_model)

    micro_batches = [
        (rng.randn(1, seq_len, d_model), rng.randint(0, vocab_size, size=(1, seq_len))) for _ in range(4)
    ]
    updated_weight, mean_loss = train_with_gradient_accumulation(micro_batches, output_weight, lr=0.1)
    assert updated_weight.shape == output_weight.shape
    assert not np.allclose(updated_weight, output_weight, atol=1e-8)
    assert mean_loss >= 0


def test_gradient_accumulation_gives_the_same_update_as_one_big_batch_step():
    # End-to-end version of the correctness property: the WEIGHT UPDATE
    # from accumulating gradients over micro-batches should match the
    # update from a single training step on the concatenated full batch.
    rng = np.random.RandomState(3)
    vocab_size, d_model, seq_len = 10, 5, 4
    output_weight = rng.randn(vocab_size, d_model)
    lr = 0.2

    micro_batches = [
        (rng.randn(1, seq_len, d_model), rng.randint(0, vocab_size, size=(1, seq_len))) for _ in range(3)
    ]
    updated_weight, _ = train_with_gradient_accumulation(micro_batches, output_weight, lr)

    full_hidden = np.concatenate([h for h, _ in micro_batches], axis=0)
    full_tokens = np.concatenate([t for _, t in micro_batches], axis=0)
    full_grad, _ = compute_output_head_gradient(full_hidden, full_tokens, output_weight)
    expected_weight = output_weight - lr * full_grad

    assert np.allclose(updated_weight, expected_weight, atol=1e-6)


def test_uses_mean_not_sum_when_accumulating():
    # Directly targets a mutant that sums instead of averages the
    # micro-batch gradients, which would scale the effective learning
    # rate by the number of micro-batches, unintentionally.
    grads = [np.array([1.0]), np.array([1.0]), np.array([1.0])]
    result = accumulate_gradients(grads)
    assert np.isclose(result[0], 1.0, atol=1e-10)  # mean of [1,1,1] = 1, not sum = 3
