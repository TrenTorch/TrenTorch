import numpy as np


def newton_schulz_orthogonalize(G: np.ndarray, steps: int = 5, eps: float = 1e-7) -> np.ndarray:
    """
    Approximately ORTHOGONALIZES a matrix: pushes every one of its
    singular values toward 1 (without changing its singular VECTORS,
    only rescaling along each of them), using a fixed-coefficient
    quintic iteration, cheap (only matrix multiplies) and NOT run to
    full convergence, a handful of steps gets most singular values
    much closer to 1 than they started, which is all Muon's update
    needs (see Theory for why "closer to 1", not "exactly 1", is fine).

    `G` may be any 2D shape (tall, wide, or square): normalize by its
    Frobenius norm first (`np.linalg.norm(G)`), transpose to work on
    the "tall" orientation internally if `G` is wide (more columns
    than rows), then transpose back before returning, so the output
    always matches `G`'s original shape.
    """
    pass


def muon_step(
    param: np.ndarray, grad: np.ndarray, momentum_buf: np.ndarray, lr: float, momentum: float = 0.95
) -> tuple[np.ndarray, np.ndarray]:
    """
    Muon's update: accumulate momentum exactly like SGD + Momentum
    (`new_buf = momentum * momentum_buf + grad`), but instead of
    stepping directly opposite that momentum, first run it through
    `newton_schulz_orthogonalize` (already provided above), and step
    opposite THAT instead.

    Returns (new_param, new_momentum_buf).
    """
    pass
