import numpy as np


def add_cls_token_and_position_embedding(
    patch_embeddings: np.ndarray, cls_token: np.ndarray, position_embedding: np.ndarray
) -> np.ndarray:
    """
    patch_embeddings: shape (num_patches, d_model)
    cls_token: shape (1, d_model) -- a single learned vector, the SAME
        one on every forward pass, prepended to every image's sequence
    position_embedding: shape (num_patches + 1, d_model) -- one learned
        vector per sequence position (including the prepended CLS
        token's position)

    Two things patch embeddings alone are missing: (1) a dedicated
    position in the sequence whose final representation can be used for
    whole-image classification (the "CLS token" trick, borrowed
    directly from BERT), and (2) any notion of WHERE each patch sits in
    the image -- attention itself is permutation-invariant, so without
    an explicit position signal, shuffling every patch would produce an
    identical output.
    """
    # TODO: prepend cls_token to patch_embeddings along the sequence axis
    # (axis=0) with np.concatenate, giving a (num_patches+1, d_model)
    # sequence, then add position_embedding elementwise.
    pass
