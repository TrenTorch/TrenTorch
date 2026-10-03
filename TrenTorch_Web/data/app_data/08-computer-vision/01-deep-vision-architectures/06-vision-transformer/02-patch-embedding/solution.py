
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear


def patch_embedding(patches: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return linear(patches, weight, bias)
