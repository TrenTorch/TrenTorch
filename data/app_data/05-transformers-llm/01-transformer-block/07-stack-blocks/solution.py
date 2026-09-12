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
    for params in blocks_params:
        x = transformer_block_forward(x, num_heads, mask=mask, eps=eps, **params)
    return x
