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
    """
    images: shape (N, C, H, W) -- a batch of images
    kernels: list of conv kernels, passed to 03-stack-multiple-blocks
    fc_weight: shape (num_classes, flattened_feature_dim)
    fc_bias: shape (num_classes,)
    labels: optional shape (N,) int array of true class indices

    Returns `probs` (shape (N, num_classes)) if labels is None,
    otherwise `(probs, loss)`.
    """
    # TODO: For each image, run it through the CNN backbone
    # (03-stack-multiple-blocks) then flatten (01-flatten), stack the
    # batch into one matrix, feed it through the final Linear layer
    # (linear) and softmax (softmax). If labels are given, also compute
    # cce_loss.
    pass
