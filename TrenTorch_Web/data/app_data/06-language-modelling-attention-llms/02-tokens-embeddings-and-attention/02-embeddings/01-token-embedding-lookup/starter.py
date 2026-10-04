import numpy as np


def embedding_forward(token_ids: np.ndarray, embedding_table: np.ndarray) -> np.ndarray:
    """
    Looks up each token id's row in embedding_table (shape
    (vocab_size, embed_dim)). `token_ids` can be any shape (a single
    sequence, or a whole batch of sequences); the output has that SAME
    shape, plus an extra trailing embed_dim dimension.
    """
    pass
