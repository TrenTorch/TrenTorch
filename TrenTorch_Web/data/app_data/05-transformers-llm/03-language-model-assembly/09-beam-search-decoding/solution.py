import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

full_lm_forward = load_solution("05-transformers-llm/03-language-model-assembly/04-full-forward-pass").full_lm_forward
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def _log_softmax(logits_row: np.ndarray) -> np.ndarray:
    shifted = logits_row - np.max(logits_row)
    return shifted - np.log(np.sum(np.exp(shifted)))


def sequence_log_prob(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None,
) -> float:
    seq_len = token_ids.shape[-1]
    mask = build_causal_mask(seq_len)
    logits = full_lm_forward(token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask=mask)

    total = 0.0
    for t in range(seq_len - 1):
        log_probs = _log_softmax(logits[0, t, :])
        total += log_probs[token_ids[0, t + 1]]
    return float(total)


def beam_search_decode(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None,
    num_new_tokens: int,
    beam_width: int,
) -> np.ndarray:
    beams = [(token_ids[0].tolist(), 0.0)]

    for _ in range(num_new_tokens):
        candidates = []
        for sequence, score in beams:
            seq_array = np.array([sequence])
            seq_len = seq_array.shape[-1]
            mask = build_causal_mask(seq_len)
            logits = full_lm_forward(
                seq_array, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask=mask
            )
            log_probs = _log_softmax(logits[0, -1, :])

            top_indices = np.argsort(log_probs)[-beam_width:]
            for idx in top_indices:
                candidates.append((sequence + [int(idx)], score + float(log_probs[idx])))

        candidates.sort(key=lambda c: c[1], reverse=True)
        beams = candidates[:beam_width]

    best_sequence, _ = max(beams, key=lambda c: c[1])
    return np.array([best_sequence])
