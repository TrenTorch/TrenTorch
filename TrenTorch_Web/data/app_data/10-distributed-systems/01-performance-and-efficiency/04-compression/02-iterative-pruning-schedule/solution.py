
import numpy as np

from _load import load_solution

magnitude_prune = load_solution("systems-perf-magnitude-pruning").magnitude_prune


def cubic_sparsity_schedule(step: int, total_steps: int, target_sparsity: float) -> float:
    if step >= total_steps:
        return target_sparsity
    progress = step / total_steps
    return target_sparsity * (1.0 - (1.0 - progress) ** 3)


def iterative_prune(weight: np.ndarray, target_sparsity: float, num_steps: int) -> list[np.ndarray]:
    results = []
    for step in range(1, num_steps + 1):
        current_sparsity = cubic_sparsity_schedule(step, num_steps, target_sparsity)
        results.append(magnitude_prune(weight, current_sparsity))
    return results
