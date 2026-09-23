import numpy as np


def add_cls_token_and_position_embedding(
    patch_embeddings: np.ndarray, cls_token: np.ndarray, position_embedding: np.ndarray
) -> np.ndarray:
    sequence = np.concatenate([cls_token, patch_embeddings], axis=0)
    return sequence + position_embedding
