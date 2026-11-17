import numpy as np


def clip_logits(img, txt, temp):
    """
    img: image embeddings, shape (N, d)
    txt: text embeddings, shape (N, d), where row i matches image i
    temp: temperature (positive)

    Returns:
        The N x N matrix of scaled cosine similarities between every image and every text.
    """
    # TODO: Normalize both sets of embeddings and compute all pairwise cosine similarities divided by temp (see Theory).
    pass
