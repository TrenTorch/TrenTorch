import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

transformer_block_forward = load_solution(
    "05-transformers-llm/01-transformer-block/06-assemble-full-block"
).transformer_block_forward


def vit_encoder_block(
    sequence: np.ndarray,
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
) -> np.ndarray:
    """
    sequence: shape (seq_len, d_model) -- the CLS token + patch
        embeddings + position embeddings sequence from 03-cls-token-
        position-embedding, with NO batch dimension

    This is the entire point of the Vision Transformer: once an image
    has been turned into a sequence of embeddings, the transformer
    block from 05-transformers-llm/01-transformer-block/06-assemble-
    full-block needs ZERO modification to process it -- it has no idea,
    and no way to tell, whether its input sequence came from patchified
    pixels or from word tokens. This function only handles one
    bookkeeping detail: `transformer_block_forward` expects a batch
    dimension (shape (batch, seq_len, d_model)), so a single image's
    sequence needs to be temporarily wrapped into a batch of size 1 and
    unwrapped afterward.
    """
    # TODO: add a batch dimension of size 1 to `sequence` (e.g.
    # `sequence[None, :, :]`), call transformer_block_forward with all
    # the given parameters, then remove the batch dimension from the
    # result (e.g. `result[0]`) before returning it.
    pass
