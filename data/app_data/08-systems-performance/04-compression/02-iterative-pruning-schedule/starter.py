import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

magnitude_prune = load_solution("08-systems-performance/04-compression/01-magnitude-pruning").magnitude_prune


def cubic_sparsity_schedule(step: int, total_steps: int, target_sparsity: float) -> float:
    """
    step: which pruning step this is (1-indexed: step=total_steps is the
        final step, and should hit target_sparsity exactly)
    total_steps: how many pruning steps the whole schedule spans
    target_sparsity: the final sparsity the schedule should reach

    Returns the sparsity to prune TO at this step, following a cubic
    schedule: aggressive pruning early (when the network has the most
    redundant capacity to spare), tapering off as sparsity approaches
    the target (when remaining weights matter more).
    """
    # TODO: if step >= total_steps, return target_sparsity directly
    # (clamp the final step exactly, avoiding any floating-point
    # rounding surprise). Otherwise, progress = step / total_steps, and
    # return target_sparsity * (1 - (1 - progress)**3).
    pass


def iterative_prune(weight: np.ndarray, target_sparsity: float, num_steps: int) -> list[np.ndarray]:
    """
    Applies magnitude_prune repeatedly, once per step, at the
    cubic_sparsity_schedule's sparsity for that step.

    Returns a list of `num_steps` pruned arrays, one per step, ending
    at exactly target_sparsity.
    """
    # TODO: for step in range(1, num_steps + 1): compute this step's
    # sparsity via cubic_sparsity_schedule, call magnitude_prune(weight,
    # that_sparsity), and collect the results into a list.
    pass
