import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

apply_rope = load_solution("04-seq-modeling/02-embeddings/06-rope").apply_rope


def compute_rope_angles_scaled(seq_len: int, dim: int, scale_factor: float) -> np.ndarray:
    position = np.arange(seq_len)[:, None] / scale_factor
    freq = 10000.0 ** (-np.arange(0, dim, 2) / dim)
    return position * freq
