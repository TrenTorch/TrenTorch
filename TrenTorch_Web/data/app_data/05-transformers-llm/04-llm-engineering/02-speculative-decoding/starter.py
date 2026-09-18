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
    """
    Speculative decoding, one draft-and-verify round: a small, cheap
    "draft" model greedily proposes `num_draft_tokens` tokens
    (`[07-greedy-decoding]`), then a single forward pass of the larger
    "target" model VERIFIES every proposed token AT ONCE (one parallel
    forward pass over the whole draft, instead of `num_draft_tokens`
    separate autoregressive steps). Accepted tokens are exactly those
    where the target model's own greedy choice AGREES with the draft's
    proposal, in order, starting from the first proposed token; the
    first DISAGREEMENT is corrected to the target's own choice, and
    everything after it is discarded.

    Returns `(accepted_token_ids, num_accepted)`.
    """
    pass
