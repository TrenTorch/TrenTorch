import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def patch_embedding(patches: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return linear(patches, weight, bias)
