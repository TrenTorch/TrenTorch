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
    """
    The TOTAL log-probability the model assigns to `token_ids` under
    next-token prediction: the sum, over every position, of the log
    probability assigned to the token that actually comes next (the
    exact opposite sign of `[03-next-token-cross-entropy]`'s loss, which
    averages NEGATIVE log-probabilities instead of summing positive
    ones).
    """
    pass


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
    """
    Beam search: maintains `beam_width` candidate sequences (a "beam")
    simultaneously, instead of `[07-greedy-decoding]`'s single running
    sequence. At every step, expands EVERY current beam by its own top
    `beam_width` next-token candidates, pools ALL of those expansions
    together, and keeps only the globally top `beam_width` by CUMULATIVE
    log-probability, before expanding again. Returns the single
    highest-scoring completed sequence after `num_new_tokens` steps.

    `beam_width=1` must reduce EXACTLY to `[07-greedy-decoding]`'s
    `greedy_decode` (only one beam ever survives, and it must always be
    the single highest-scoring continuation, i.e. the argmax).
    """
    pass
