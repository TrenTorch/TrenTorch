
import numpy as np

from _load import load_solution

embedding_forward = load_solution("seq-embeddings-token-embedding-lookup").embedding_forward
sinusoidal_positional_encoding = load_solution("seq-embeddings-sinusoidal-positional-encoding").sinusoidal_positional_encoding
combine_embeddings = load_solution("seq-embeddings-combine-token-positional").combine_embeddings
stack_transformer_blocks = load_solution("txf-block-stack-blocks").stack_transformer_blocks
compute_output_logits = load_solution("txf-lm-weight-tying").compute_output_logits


def full_lm_forward(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None = None,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    A complete decoder-only language model's forward pass, assembled
    entirely from pieces already built earlier in this curriculum:

        token_ids -> token embeddings -> + positional encoding
                  -> N stacked Transformer blocks -> output projection -> logits

    `token_ids` must include a leading batch dimension, shape
    `(batch, seq_len)` (matching `[04-mha-split-heads]`'s requirement,
    since attention inside each Transformer block needs one).
    """
    pass
