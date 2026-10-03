
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear
softmax = load_solution("classification-softmax-cce").softmax


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
