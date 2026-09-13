import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

stack_cnn_blocks = load_solution("07-vision/03-cnn-architecture/03-stack-multiple-blocks").stack_cnn_blocks
flatten = load_solution("07-vision/03-cnn-architecture/01-flatten").flatten
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax
cce_loss = load_solution("01-classical-ml/02-classification/06-softmax-cce").cce_loss


def full_cnn_classifier(
    images: np.ndarray,
    kernels: list,
    fc_weight: np.ndarray,
    fc_bias: np.ndarray,
    labels: np.ndarray | None = None,
    pool_size: int = 2,
):
    flat_features = np.stack(
        [flatten(stack_cnn_blocks(image, kernels, pool_size=pool_size)) for image in images]
    )
    logits = linear(flat_features, fc_weight, fc_bias)
    probs = softmax(logits)

    if labels is None:
        return probs
    return probs, cce_loss(probs, labels)
