
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear
softmax = load_solution("classification-softmax-cce").softmax


def classification_head(sequence: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    cls_output = sequence[0]
    logits = linear(cls_output[None, :], weight, bias)
    return softmax(logits)[0]
