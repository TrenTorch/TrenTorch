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
    """
    An "encoder" block is just `[06-assemble-full-block]`'s Transformer
    block run with NO mask: every position may attend to every other
    position, including ones that come AFTER it (bidirectional context).
    """
    pass


def decoder_block_forward(x: np.ndarray, num_heads: int, **block_params) -> np.ndarray:
    """
    A "decoder" block is the SAME Transformer block, run with a causal
    mask (`[04-seq-modeling/04-attention/02-causal-mask]`): a position
    may only attend to itself and earlier positions.
    """
    pass


def encoder_decoder_cross_attention(
    decoder_hidden: np.ndarray,
    encoder_output: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
) -> np.ndarray:
    """
    The third arrangement: an encoder-decoder model's decoder attends to
    the ENCODER's output, not (only) to itself. `query` comes from the
    decoder's own hidden states; `key`/`value` both come from the
    encoder's output, which may have a DIFFERENT sequence length than
    the decoder.
    """
    pass
