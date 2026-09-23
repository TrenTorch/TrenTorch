import math


def has_model_degraded(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    """
    Whether a model's CURRENT performance has fallen more than
    `tolerance` below its established baseline -- the direct,
    performance-based version of 02-concept-drift's
    detect_concept_drift, but for a single current reading instead of
    a whole history of windows.
    """
    # TODO: (baseline_metric - current_metric) > tolerance
    pass


def predicted_future_metric(current_metric: float, degradation_rate_per_day: float, days_ahead: float) -> float:
    """
    A simple linear extrapolation: if the metric has been degrading at
    a roughly constant rate per day, what would it be `days_ahead`
    days from now?
    """
    # TODO: current_metric - degradation_rate_per_day * days_ahead
    pass


def days_until_degraded(
    current_metric: float, baseline_metric: float, tolerance: float, degradation_rate_per_day: float
) -> float:
    """
    Given the SAME linear degradation assumption, how many days remain
    before the model crosses into "degraded" territory (as
    has_model_degraded would define it)? Returns math.inf if the
    degradation rate is zero or negative (never degrading), and 0.0 if
    the model has ALREADY crossed the threshold.
    """
    # TODO: if degradation_rate_per_day <= 0, return math.inf.
    # degradation_budget = current_metric - (baseline_metric - tolerance)
    # (how much room is left before crossing the threshold). If that
    # budget is already <= 0, return 0.0. Otherwise return
    # degradation_budget / degradation_rate_per_day.
    pass


def should_retrain_now(current_metric: float, baseline_metric: float, tolerance: float) -> bool:
    """
    The actual retraining decision, built directly on top of
    has_model_degraded -- kept as its own function so a real system's
    retraining LOGIC stays decoupled from the degradation DEFINITION,
    even though today they're identical.
    """
    # TODO: has_model_degraded(current_metric, baseline_metric, tolerance)
    pass
