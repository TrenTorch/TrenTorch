import numpy as np


def output_projection_tied(hidden_states: np.ndarray, embedding_table: np.ndarray) -> np.ndarray:
    """
    Weight-tied output projection: project `hidden_states` to vocabulary
    logits by reusing `[04-seq-modeling/02-embeddings/01-token-embedding-lookup]`'s
    OWN embedding table, transposed, rather than a separate, independently
    learned matrix.
    """
    pass


def output_projection_untied(hidden_states: np.ndarray, output_weight: np.ndarray) -> np.ndarray:
    """
    Untied output projection: an ordinary linear layer with its OWN,
    independently-learned `output_weight`, entirely separate from
    whatever embedding table was used to look up the input tokens.
    """
    pass
