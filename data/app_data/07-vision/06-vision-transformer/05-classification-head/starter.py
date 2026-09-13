import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax


def classification_head(sequence: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    sequence: shape (seq_len, d_model) -- the transformer block's output
        sequence from 04-vit-encoder-block
    weight: shape (num_classes, d_model)
    bias: shape (num_classes,)

    After the whole sequence has passed through the transformer, the CLS
    token (position 0) is the ONLY position used for classification --
    it was specifically designed, back in 03-cls-token-position-
    embedding, to have absorbed a summary of the entire image through
    attention. Every other position's final output is simply discarded.

    Returns shape (num_classes,): class probabilities, summing to 1.
    """
    # TODO: pull out sequence[0] (the CLS token's final representation),
    # run it through `linear` to get class logits, then `softmax` to
    # turn those logits into probabilities. `linear` and `softmax` both
    # expect a 2D (batch, features) input, so you'll need to add and
    # then remove a batch dimension of size 1 around the single CLS
    # vector.
    pass
