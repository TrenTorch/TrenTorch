import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

embedding_forward = load_solution("04-seq-modeling/02-embeddings/01-token-embedding-lookup").embedding_forward
sinusoidal_positional_encoding = load_solution(
    "04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding"
).sinusoidal_positional_encoding
combine_embeddings = load_solution("04-seq-modeling/02-embeddings/05-combine-token-positional-embeddings").combine_embeddings
stack_transformer_blocks = load_solution("05-transformers-llm/01-transformer-block/07-stack-blocks").stack_transformer_blocks
compute_output_logits = load_solution("05-transformers-llm/03-language-model-assembly/02-weight-tying").compute_output_logits


def full_lm_forward(
    token_ids: np.ndarray,
    token_embedding_table: np.ndarray,
    blocks_params: list[dict],
    num_heads: int,
    tied: bool,
    output_weight: np.ndarray | None = None,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    seq_len = token_ids.shape[-1]
    d_model = token_embedding_table.shape[-1]

    token_embeddings = embedding_forward(token_ids, token_embedding_table)
    positional_embeddings = sinusoidal_positional_encoding(seq_len, d_model)
    x = combine_embeddings(token_embeddings, positional_embeddings)

    x = stack_transformer_blocks(x, num_heads, blocks_params, mask=mask)

    logits = compute_output_logits(x, token_embedding_table, tied, output_weight)
    return logits
