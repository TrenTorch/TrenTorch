import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

layer_norm_forward = load_solution("05-transformers-llm/01-transformer-block/01-layer-normalization-forward").layer_norm_forward
residual_connection = load_solution("05-transformers-llm/01-transformer-block/03-residual-connection").residual_connection
feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
multi_head_attention = load_solution("04-seq-modeling/04-attention/05-mha-concat-output-projection").multi_head_attention


def transformer_block_forward(
    x: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
    ffn_weight1: np.ndarray,
    ffn_bias1: np.ndarray,
    ffn_weight2: np.ndarray,
    ffn_bias2: np.ndarray,
    gamma1: np.ndarray,
    beta1: np.ndarray,
    gamma2: np.ndarray,
    beta2: np.ndarray,
    mask: np.ndarray | None = None,
    eps: float = 1e-5,
) -> np.ndarray:
    normed1 = layer_norm_forward(x, gamma1, beta1, eps)
    attn_out, _ = multi_head_attention(normed1, normed1, normed1, num_heads, weight_o, bias_o, mask=mask)
    x = residual_connection(x, attn_out)

    normed2 = layer_norm_forward(x, gamma2, beta2, eps)
    ffn_out = feedforward_sublayer(normed2, ffn_weight1, ffn_bias1, ffn_weight2, ffn_bias2)
    x = residual_connection(x, ffn_out)

    return x
