import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax_last_axis = load_solution("04-seq-modeling/04-attention/03-softmax-last-axis").softmax_last_axis
full_lm_forward = load_solution("05-transformers-llm/03-language-model-assembly/04-full-forward-pass").full_lm_forward
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def scale_and_filter_logits(logits_row: np.ndarray, temperature: float, top_k: int | None) -> np.ndarray:
    """
    Divides `logits_row` by `temperature` (`[02-modern-transformer-architecture/10-logit-scaling]`'s
    style of scaling, but user-controlled here rather than fixed by
    `d_model`: temperature < 1 sharpens the distribution, > 1 flattens
    it), then, if `top_k` is given, masks every logit OUTSIDE the `top_k`
    highest-scoring positions to `-inf` (so they get exactly `0`
    probability after softmax).
    """
    pass


def sample_next_token(logits_row: np.ndarray, temperature: float, top_k: int | None, rng: np.random.RandomState) -> int:
    """
    Applies `scale_and_filter_logits`, converts to a probability
    distribution via `[04-seq-modeling/04-attention/03-softmax-last-axis]`'s
    `softmax_last_axis`, and draws ONE token id from that distribution
    using `rng.choice`.
    """
    pass


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
    """
    `[07-greedy-decoding]`'s autoregressive generation loop, with
    `sample_next_token` in place of `argmax`. Assumes `token_ids` has
    batch size `1` (shape `(1, seq_len)`).
    """
    pass
