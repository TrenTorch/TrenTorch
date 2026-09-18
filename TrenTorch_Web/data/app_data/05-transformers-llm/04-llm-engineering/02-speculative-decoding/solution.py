import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

greedy_decode = load_solution("05-transformers-llm/03-language-model-assembly/07-greedy-decoding").greedy_decode
full_lm_forward = load_solution("05-transformers-llm/03-language-model-assembly/04-full-forward-pass").full_lm_forward
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def speculative_decode_step(
    token_ids: np.ndarray,
    draft_embedding_table: np.ndarray,
    draft_blocks_params: list[dict],
    draft_num_heads: int,
    draft_tied: bool,
    draft_output_weight: np.ndarray | None,
    target_embedding_table: np.ndarray,
    target_blocks_params: list[dict],
    target_num_heads: int,
    target_tied: bool,
    target_output_weight: np.ndarray | None,
    num_draft_tokens: int,
) -> tuple[np.ndarray, int]:
    seq_len = token_ids.shape[-1]

    draft_sequence = greedy_decode(
        token_ids, draft_embedding_table, draft_blocks_params, draft_num_heads, draft_tied, draft_output_weight,
        num_draft_tokens,
    )

    mask = build_causal_mask(draft_sequence.shape[-1])
    target_logits = full_lm_forward(
        draft_sequence, target_embedding_table, target_blocks_params, target_num_heads, target_tied,
        target_output_weight, mask=mask,
    )

    accepted = draft_sequence[:, :seq_len]
    num_accepted = 0

    for i in range(num_draft_tokens):
        draft_token = int(draft_sequence[0, seq_len + i])
        target_prediction = int(np.argmax(target_logits[0, seq_len - 1 + i, :]))

        if draft_token == target_prediction:
            accepted = np.concatenate([accepted, [[draft_token]]], axis=-1)
            num_accepted += 1
        else:
            accepted = np.concatenate([accepted, [[target_prediction]]], axis=-1)
            break

    return accepted, num_accepted
