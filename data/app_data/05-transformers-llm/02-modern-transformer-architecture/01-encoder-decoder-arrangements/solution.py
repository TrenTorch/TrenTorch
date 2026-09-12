import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask
multi_head_attention = load_solution("04-seq-modeling/04-attention/05-mha-concat-output-projection").multi_head_attention


def encoder_block_forward(x: np.ndarray, num_heads: int, **block_params) -> np.ndarray:
    return transformer_block_forward(x, num_heads, mask=None, **block_params)


def decoder_block_forward(x: np.ndarray, num_heads: int, **block_params) -> np.ndarray:
    seq_len = x.shape[-2]
    causal_mask = build_causal_mask(seq_len)
    return transformer_block_forward(x, num_heads, mask=causal_mask, **block_params)


def encoder_decoder_cross_attention(
    decoder_hidden: np.ndarray,
    encoder_output: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
) -> np.ndarray:
    output, _ = multi_head_attention(decoder_hidden, encoder_output, encoder_output, num_heads, weight_o, bias_o)
    return output
