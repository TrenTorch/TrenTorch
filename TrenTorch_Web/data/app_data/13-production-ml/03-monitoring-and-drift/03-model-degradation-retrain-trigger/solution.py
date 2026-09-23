import math


def has_model_degraded(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    return (baseline_metric - current_metric) > tolerance


def predicted_future_metric(current_metric: float, degradation_rate_per_day: float, days_ahead: float) -> float:
    return current_metric - degradation_rate_per_day * days_ahead


def days_until_degraded(
    current_metric: float, baseline_metric: float, tolerance: float, degradation_rate_per_day: float
) -> float:
    if degradation_rate_per_day <= 0:
        return math.inf
    degradation_budget = current_metric - (baseline_metric - tolerance)
    if degradation_budget <= 0:
        return 0.0
    return degradation_budget / degradation_rate_per_day


def should_retrain_now(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    return has_model_degraded(current_metric, baseline_metric, tolerance)
