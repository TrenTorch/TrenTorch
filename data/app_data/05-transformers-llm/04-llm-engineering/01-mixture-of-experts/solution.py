import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
softmax_last_axis = load_solution("04-seq-modeling/04-attention/03-softmax-last-axis").softmax_last_axis


def moe_gate(x: np.ndarray, gate_weight: np.ndarray, top_k: int) -> tuple[np.ndarray, np.ndarray]:
    gate_logits = x @ gate_weight.T
    num_experts = gate_weight.shape[0]

    top_indices = np.argsort(gate_logits, axis=-1)[..., -top_k:]
    top_logits = np.take_along_axis(gate_logits, top_indices, axis=-1)
    top_weights = softmax_last_axis(top_logits)

    return top_indices, top_weights


def moe_ffn_forward(
    x: np.ndarray,
    gate_weight: np.ndarray,
    expert_params: list[dict],
    top_k: int,
) -> np.ndarray:
    original_shape = x.shape
    d_model = original_shape[-1]
    flat_x = x.reshape(-1, d_model)

    top_indices, top_weights = moe_gate(flat_x, gate_weight, top_k)

    output = np.zeros_like(flat_x)
    for token_idx in range(flat_x.shape[0]):
        token_x = flat_x[token_idx : token_idx + 1]
        for k in range(top_k):
            expert_idx = int(top_indices[token_idx, k])
            weight = top_weights[token_idx, k]
            params = expert_params[expert_idx]
            expert_out = feedforward_sublayer(
                token_x, params["weight1"], params["bias1"], params["weight2"], params["bias2"]
            )
            output[token_idx] += weight * expert_out[0]

    return output.reshape(original_shape)
