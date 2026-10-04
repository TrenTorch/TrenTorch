
import numpy as np

from _load import load_solution

full_lm_forward = load_solution("txf-lm-full-forward-pass").full_lm_forward
build_causal_mask = load_solution("seq-attention-causal-mask").build_causal_mask


def greedy_decode(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None,
    num_new_tokens: int,
) -> np.ndarray:
    """
    Autoregressive greedy generation: repeatedly run `[04-full-forward-pass]`'s
    `full_lm_forward` on the sequence SO FAR (with a causal mask, since
    generation must never "see" a token before appending it), take the
    single MOST LIKELY next token (`argmax`) at the last position, append
    it, and repeat `num_new_tokens` times.
    """
    pass
