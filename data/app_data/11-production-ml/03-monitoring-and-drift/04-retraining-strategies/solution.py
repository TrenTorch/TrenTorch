import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

has_model_degraded = load_solution(
    "11-production-ml/03-monitoring-and-drift/03-model-degradation-retrain-trigger"
).has_model_degraded


def scheduled_retrain_due(days_since_last_retrain: int, schedule_interval_days: int) -> bool:
    return days_since_last_retrain >= schedule_interval_days


def triggered_retrain_due(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    return has_model_degraded(current_metric, baseline_metric, tolerance)


def online_update_step(weight: float, bias: float, x: float, y: float, learning_rate: float) -> tuple:
    prediction = weight * x + bias
    error = prediction - y
    grad_weight = 2 * x * error
    grad_bias = 2 * error
    new_weight = weight - learning_rate * grad_weight
    new_bias = bias - learning_rate * grad_bias
    return new_weight, new_bias
