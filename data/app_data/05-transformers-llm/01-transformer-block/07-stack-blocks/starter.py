import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward


def stack_transformer_blocks(
    x: np.ndarray,
    num_heads: int,
    blocks_params: list[dict],
    mask: np.ndarray | None = None,
    eps: float = 1e-5,
) -> np.ndarray:
    """
    Runs `x` through a SEQUENCE of Transformer blocks, each block's
    output feeding directly into the next block's input.

    `blocks_params` is a list of dicts, one per block, each holding that
    block's OWN `weight_o`, `bias_o`, `ffn_weight1`, `ffn_bias1`,
    `ffn_weight2`, `ffn_bias2`, `gamma1`, `beta1`, `gamma2`, `beta2`
    (exactly the keyword arguments `transformer_block_forward` expects
    beyond `x`, `num_heads`, `mask`, and `eps`, which are shared across
    every block in the stack).
    """
    pass
