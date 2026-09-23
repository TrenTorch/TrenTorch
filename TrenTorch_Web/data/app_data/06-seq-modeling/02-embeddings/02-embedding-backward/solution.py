import numpy as np


def embedding_backward(grad_output: np.ndarray, token_ids: np.ndarray, vocab_size: int) -> np.ndarray:
    embed_dim = grad_output.shape[-1]
    grad_table = np.zeros((vocab_size, embed_dim))

    flat_ids = token_ids.reshape(-1)
    flat_grad = grad_output.reshape(-1, embed_dim)

    np.add.at(grad_table, flat_ids, flat_grad)

    return grad_table
