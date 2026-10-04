import math


def flops_for_training(num_params: float, num_tokens: float) -> float:
    """
    The standard approximation for a Transformer's total training
    compute: `6 * N * D`, `N` the parameter count, `D` the number of
    training tokens (`6` accounts for one forward pass being roughly
    `2*N` FLOPs per token, and backpropagation costing roughly twice the
    forward pass, `2N + 4N = 6N` per token).
    """
    pass


def chinchilla_optimal_allocation(compute_budget_flops: float) -> tuple[float, float]:
    """
    The Chinchilla (Hoffmann et al. 2022) finding, simplified: for a
    FIXED compute budget `C = 6*N*D`, loss is minimized when `N` and `D`
    are scaled roughly EQUALLY with `C`, both proportional to `sqrt(C)`.
    Returns `(n_optimal, d_optimal)`, both equal to `sqrt(C / 6)` (chosen
    so `flops_for_training(n_optimal, d_optimal) == compute_budget_flops`
    exactly).
    """
    pass
