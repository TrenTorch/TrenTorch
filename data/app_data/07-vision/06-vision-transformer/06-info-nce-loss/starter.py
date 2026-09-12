import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax
cce_loss = load_solution("01-classical-ml/02-classification/06-softmax-cce").cce_loss


def info_nce_loss(image_embeds: np.ndarray, text_embeds: np.ndarray, temperature: float = 0.07) -> float:
    """
    image_embeds: shape (N, D) -- N images' embeddings (e.g. from a
        ViT's CLS token, before the classification head)
    text_embeds: shape (N, D) -- N captions' embeddings, where row i is
        the CAPTION THAT MATCHES image i (a "batch of correct pairs")
    temperature: scales similarity scores before softmax; smaller values
        make the distribution sharper (more confident)

    CLIP-style contrastive training: given a batch of N (image, caption)
    pairs, treat it as an N-way classification problem in BOTH
    directions at once -- "which of the N captions matches this image?"
    and "which of the N images matches this caption?" -- where the
    correct answer for row i is always column i (the matching pair).
    """
    # TODO:
    # 1. L2-normalize both image_embeds and text_embeds along axis=1
    #    (divide each row by its own norm) -- this makes the dot product
    #    below equivalent to cosine similarity.
    # 2. Compute the (N, N) similarity matrix: normalized image_embeds
    #    @ normalized text_embeds.T, divided by temperature.
    # 3. The correct match for row i is always column i, so labels =
    #    np.arange(N).
    # 4. Compute cce_loss(softmax(logits), labels) for the image-to-text
    #    direction, and cce_loss(softmax(logits.T), labels) for the
    #    text-to-image direction.
    # 5. Return the average of the two directions' losses, as a float.
    pass
