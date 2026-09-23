import numpy as np


def compute_output_logits(
    hidden_states: np.ndarray,
    embedding_table: np.ndarray,
    tied: bool,
    output_weight: np.ndarray | None = None,
) -> np.ndarray:
    """
    Computes vocabulary logits either TIED (reusing `embedding_table` as
    the output projection, `output_weight` ignored/unused) or UNTIED
    (using the separate `output_weight` matrix), matching
    `[02-modern-transformer-architecture/09-untied-embeddings]`'s two
    functions, unified behind one `tied` flag.
    """
    pass


def count_output_head_parameters(vocab_size: int, d_model: int, tied: bool) -> int:
    """
    Number of ADDITIONAL parameters the output head introduces beyond the
    input embedding table: `0` when tied (no separate matrix at all),
    `vocab_size * d_model` when untied.
    """
    pass
