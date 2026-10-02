
import numpy as np

from _load import load_solution

transformer_block_forward = load_solution("txf-block-assemble-full-block").transformer_block_forward


def stack_transformer_blocks(
    x: np.ndarray,
    num_heads: int,
    blocks_params: list[dict],
    mask: np.ndarray | None = None,
    eps: float = 1e-5,
) -> np.ndarray:
    for params in blocks_params:
        x = transformer_block_forward(x, num_heads, mask=mask, eps=eps, **params)
    return x
