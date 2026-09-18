"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/01-mixture-of-experts/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
moe_gate = _module.moe_gate
moe_ffn_forward = _module.moe_ffn_forward

feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer


def _random_expert(rng, d_model, d_ff):
    return dict(
        weight1=rng.randn(d_ff, d_model),
        bias1=rng.randn(d_ff),
        weight2=rng.randn(d_model, d_ff),
        bias2=rng.randn(d_model),
    )


def test_gate_selects_exactly_top_k_experts():
    rng = np.random.RandomState(0)
    num_tokens, d_model, num_experts, top_k = 5, 8, 6, 2
    x = rng.randn(num_tokens, d_model)
    gate_weight = rng.randn(num_experts, d_model)
    top_indices, top_weights = moe_gate(x, gate_weight, top_k)
    assert top_indices.shape == (num_tokens, top_k)
    assert top_weights.shape == (num_tokens, top_k)


def test_gate_weights_sum_to_one_per_token():
    rng = np.random.RandomState(1)
    num_tokens, d_model, num_experts, top_k = 4, 6, 5, 3
    x = rng.randn(num_tokens, d_model)
    gate_weight = rng.randn(num_experts, d_model)
    _, top_weights = moe_gate(x, gate_weight, top_k)
    assert np.allclose(top_weights.sum(axis=-1), 1.0, atol=1e-6)


def test_gate_selects_the_highest_scoring_experts():
    d_model, num_experts, top_k = 3, 5, 2
    x = np.array([[1.0, 0.0, 0.0]])
    # Make expert 0's score dominate, expert 1 second, rest much lower.
    gate_weight = np.array(
        [[10.0, 0.0, 0.0], [5.0, 0.0, 0.0], [-5.0, 0.0, 0.0], [-5.0, 0.0, 0.0], [-5.0, 0.0, 0.0]]
    )
    top_indices, _ = moe_gate(x, gate_weight, top_k)
    selected = set(top_indices[0].tolist())
    assert selected == {0, 1}


def test_moe_ffn_output_shape_matches_input_shape():
    rng = np.random.RandomState(2)
    num_tokens, d_model, d_ff, num_experts, top_k = 4, 6, 12, 4, 2
    x = rng.randn(num_tokens, d_model)
    gate_weight = rng.randn(num_experts, d_model)
    expert_params = [_random_expert(rng, d_model, d_ff) for _ in range(num_experts)]

    output = moe_ffn_forward(x, gate_weight, expert_params, top_k)
    assert output.shape == x.shape


def test_top_k_equal_num_experts_uses_every_expert_with_softmax_weights():
    rng = np.random.RandomState(3)
    num_tokens, d_model, d_ff, num_experts = 2, 4, 8, 3
    x = rng.randn(num_tokens, d_model)
    gate_weight = rng.randn(num_experts, d_model)
    expert_params = [_random_expert(rng, d_model, d_ff) for _ in range(num_experts)]

    output = moe_ffn_forward(x, gate_weight, expert_params, top_k=num_experts)

    gate_logits = x @ gate_weight.T
    exp_logits = np.exp(gate_logits - gate_logits.max(axis=-1, keepdims=True))
    weights = exp_logits / exp_logits.sum(axis=-1, keepdims=True)

    expected = np.zeros_like(x)
    for e in range(num_experts):
        expert_out = feedforward_sublayer(
            x, expert_params[e]["weight1"], expert_params[e]["bias1"], expert_params[e]["weight2"], expert_params[e]["bias2"]
        )
        expected += weights[:, e : e + 1] * expert_out
    assert np.allclose(output, expected, atol=1e-6)


def test_zeroing_a_non_selected_experts_weights_does_not_change_the_output():
    # Directly targets a mutant that routes through ALL experts instead
    # of only the selected top-k.
    d_model, d_ff, num_experts, top_k = 4, 8, 3, 1
    rng = np.random.RandomState(4)
    x = np.array([[10.0, 0.0, 0.0, 0.0]])  # strongly favors expert 0 via gate_weight below
    gate_weight = np.array([[10.0, 0.0, 0.0, 0.0], [-10.0, 0.0, 0.0, 0.0], [-10.0, 0.0, 0.0, 0.0]])
    expert_params = [_random_expert(rng, d_model, d_ff) for _ in range(num_experts)]

    output_before = moe_ffn_forward(x, gate_weight, expert_params, top_k)

    # Corrupt experts 1 and 2 (not selected for this token) drastically.
    expert_params[1]["weight1"] *= 1000.0
    expert_params[2]["weight2"] *= 1000.0
    output_after = moe_ffn_forward(x, gate_weight, expert_params, top_k)

    assert np.allclose(output_before, output_after, atol=1e-4)
