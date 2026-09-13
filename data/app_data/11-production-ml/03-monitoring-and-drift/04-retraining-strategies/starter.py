import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

has_model_degraded = load_solution(
    "11-production-ml/03-monitoring-and-drift/03-model-degradation-retrain-trigger"
).has_model_degraded


def scheduled_retrain_due(days_since_last_retrain: int, schedule_interval_days: int) -> bool:
    """
    The simplest retraining strategy: retrain on a fixed calendar
    schedule, regardless of whether performance has actually degraded
    at all -- simple and predictable, but potentially wasteful (a
    model that hasn't drifted gets retrained anyway) or too slow (a
    model that drifts FAST has to wait for the next scheduled date).
    """
    # TODO: days_since_last_retrain >= schedule_interval_days
    pass


def triggered_retrain_due(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    """
    A smarter strategy: retrain only when 03-model-degradation's
    has_model_degraded actually says the model needs it -- retraining
    happens exactly when it's needed, no more, no less, at the cost of
    needing continuous performance monitoring in the first place.
    """
    # TODO: has_model_degraded(current_metric, baseline_metric, tolerance)
    pass


def online_update_step(weight: float, bias: float, x: float, y: float, learning_rate: float) -> tuple:
    """
    The third strategy: don't wait for a "retrain" event at all --
    continuously nudge the model's parameters after EVERY new labeled
    example, via a single step of gradient descent on that one
    example's squared error. Returns the updated (weight, bias).
    """
    # TODO: prediction = weight * x + bias. error = prediction - y.
    # grad_weight = 2 * x * error. grad_bias = 2 * error. Return
    # (weight - learning_rate * grad_weight, bias - learning_rate *
    # grad_bias).
    pass
