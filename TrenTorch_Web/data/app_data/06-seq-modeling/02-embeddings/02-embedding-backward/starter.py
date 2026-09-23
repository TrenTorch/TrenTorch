import numpy as np


def embedding_backward(grad_output: np.ndarray, token_ids: np.ndarray, vocab_size: int) -> np.ndarray:
    """
    The backward pass of `[01-token-embedding-lookup]`'s embedding_forward.
    `grad_output` has the same shape as the forward pass's output
    (token_ids's shape, plus a trailing embed_dim). Returns grad_table,
    shape (vocab_size, embed_dim): the gradient with respect to the FULL
    embedding table, even though only the rows that were actually looked
    up receive any nonzero gradient.

    Crucially: if the SAME token id appears more than once in
    token_ids, that row's gradients must be SUMMED (accumulated), not
    overwritten, since that row was used more than once in the forward
    pass and each use contributed its own gradient.
    """
    embed_dim = grad_output.shape[-1]
    grad_table = np.zeros((vocab_size, embed_dim))
    pass
