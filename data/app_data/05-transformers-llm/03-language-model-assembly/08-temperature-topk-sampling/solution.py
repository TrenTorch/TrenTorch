import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax_last_axis = load_solution("04-seq-modeling/04-attention/03-softmax-last-axis").softmax_last_axis
full_lm_forward = load_solution("05-transformers-llm/03-language-model-assembly/04-full-forward-pass").full_lm_forward
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def scale_and_filter_logits(logits_row: np.ndarray, temperature: float, top_k: int | None) -> np.ndarray:
    scaled = logits_row / temperature
    if top_k is not None and top_k < scaled.shape[-1]:
        threshold = np.sort(scaled)[-top_k]
        scaled = np.where(scaled >= threshold, scaled, -np.inf)
    return scaled


def sample_next_token(logits_row: np.ndarray, temperature: float, top_k: int | None, rng: np.random.RandomState) -> int:
    filtered_logits = scale_and_filter_logits(logits_row, temperature, top_k)
    probs = softmax_last_axis(filtered_logits)
    return int(rng.choice(len(probs), p=probs))


def sample_decode(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None,
    num_new_tokens: int,
    temperature: float,
    top_k: int | None,
    rng: np.random.RandomState,
) -> np.ndarray:
    for _ in range(num_new_tokens):
        seq_len = token_ids.shape[-1]
        mask = build_causal_mask(seq_len)
        logits = full_lm_forward(
            token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask=mask
        )
        next_token_logits = logits[0, -1, :]
        next_token = sample_next_token(next_token_logits, temperature, top_k, rng)
        token_ids = np.concatenate([token_ids, np.array([[next_token]])], axis=-1)

    return token_ids
