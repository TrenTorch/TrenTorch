import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

apply_rope = load_solution("04-seq-modeling/02-embeddings/06-rope").apply_rope


def compute_rope_angles_scaled(seq_len: int, dim: int, scale_factor: float) -> np.ndarray:
    """
    "Position Interpolation": `[04-seq-modeling/02-embeddings/06-rope]`'s
    `compute_rope_angles`, but with every position DIVIDED by
    `scale_factor` before computing angles, compressing an extended
    sequence length back down into the range of positions the model was
    actually trained on.

    `scale_factor = target_max_len / trained_max_len`: with this choice,
    position `target_max_len - 1` (the last position of the EXTENDED
    context) maps to angle-space position `trained_max_len - 1` (the
    last position the model actually saw during training).
    """
    pass
