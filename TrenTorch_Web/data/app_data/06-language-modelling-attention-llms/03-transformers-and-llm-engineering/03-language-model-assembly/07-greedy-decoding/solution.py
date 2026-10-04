
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
    for _ in range(num_new_tokens):
        seq_len = token_ids.shape[-1]
        mask = build_causal_mask(seq_len)
        logits = full_lm_forward(
            token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask=mask
        )
        next_token_logits = logits[..., -1, :]
        next_token = np.argmax(next_token_logits, axis=-1)
        token_ids = np.concatenate([token_ids, next_token[..., None]], axis=-1)

    return token_ids
