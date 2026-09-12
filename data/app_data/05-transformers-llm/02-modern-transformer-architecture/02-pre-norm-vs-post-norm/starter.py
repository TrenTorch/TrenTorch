import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

layer_norm_forward = load_solution("05-transformers-llm/01-transformer-block/01-layer-normalization-forward").layer_norm_forward
residual_connection = load_solution("05-transformers-llm/01-transformer-block/03-residual-connection").residual_connection
feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
multi_head_attention = load_solution("04-seq-modeling/04-attention/05-mha-concat-output-projection").multi_head_attention
pre_norm_transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward


def post_norm_transformer_block_forward(
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
    """
    The ORIGINAL (2017) Transformer's arrangement: sublayer, THEN
    residual add, THEN normalize -- exactly the reverse order from
    `[01-transformer-block/06-assemble-full-block]`'s Pre-Norm block,
    where normalization happens BEFORE each sublayer instead.

        x1 = LayerNorm(x  + Attention(x),  gamma1, beta1)
        x2 = LayerNorm(x1 + FeedForward(x1), gamma2, beta2)
    """
    pass


def stack_pre_norm_blocks(x: np.ndarray, num_heads: int, block_params: dict, num_blocks: int) -> np.ndarray:
    """
    Runs `x` through `num_blocks` Pre-Norm blocks in a row, all sharing
    the SAME `block_params` (deliberately, to isolate the effect of
    depth alone from the effect of different learned weights per block).
    """
    pass


def stack_post_norm_blocks(x: np.ndarray, num_heads: int, block_params: dict, num_blocks: int) -> np.ndarray:
    """
    The Post-Norm equivalent of `stack_pre_norm_blocks`.
    """
    pass
