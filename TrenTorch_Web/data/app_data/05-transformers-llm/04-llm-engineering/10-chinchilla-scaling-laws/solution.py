import math


def flops_for_training(num_params: float, num_tokens: float) -> float:
    return 6.0 * num_params * num_tokens


def chinchilla_optimal_allocation(compute_budget_flops: float) -> tuple[float, float]:
    optimal_value = math.sqrt(compute_budget_flops / 6.0)
    return optimal_value, optimal_value
