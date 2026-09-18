"""
pytest data/app_data/11-production-ml/03-monitoring-and-drift/03-model-degradation-retrain-trigger/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/03-monitoring-and-drift/{Path(__file__).resolve().parent.name}")
has_model_degraded = _module.has_model_degraded
predicted_future_metric = _module.predicted_future_metric
days_until_degraded = _module.days_until_degraded
should_retrain_now = _module.should_retrain_now


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_has_model_degraded_true_when_drop_exceeds_tolerance():
    assert has_model_degraded(current_metric=0.80, baseline_metric=0.90, tolerance=0.05) is True


def test_02_has_model_degraded_false_within_tolerance():
    assert has_model_degraded(current_metric=0.88, baseline_metric=0.90, tolerance=0.05) is False


# --- General-case coverage --------------------------------------------


def test_03_predicted_future_metric_matches_hand_computation():
    assert math.isclose(predicted_future_metric(0.9, degradation_rate_per_day=0.01, days_ahead=10), 0.8)


def test_04_days_until_degraded_matches_hand_computation():
    # budget = 0.9 - (0.9 - 0.05) = 0.05; days = 0.05 / 0.01 = 5
    assert math.isclose(days_until_degraded(0.9, 0.9, tolerance=0.05, degradation_rate_per_day=0.01), 5.0)


def test_05_days_until_degraded_is_zero_when_already_degraded():
    assert math.isclose(days_until_degraded(0.80, 0.90, tolerance=0.05, degradation_rate_per_day=0.01), 0.0)


# --- Parameter handling -------------------------------------------------


def test_06_should_retrain_now_matches_has_model_degraded():
    assert should_retrain_now(0.80, 0.90, tolerance=0.05) == has_model_degraded(0.80, 0.90, tolerance=0.05)
    assert should_retrain_now(0.89, 0.90, tolerance=0.05) == has_model_degraded(0.89, 0.90, tolerance=0.05)


def test_07_zero_degradation_rate_never_predicted_to_degrade():
    assert days_until_degraded(0.9, 0.9, tolerance=0.05, degradation_rate_per_day=0.0) == math.inf


# --- Edge cases ---------------------------------------------------------


def test_08_tolerance_boundary_is_exclusive():
    # Uses integer-friendly values to land exactly on the boundary
    # without floating-point representation noise (0.90 - 0.85 is
    # actually 0.050000000000000044 in binary floating point, which
    # would make this assertion flaky for the wrong reason).
    assert has_model_degraded(current_metric=80, baseline_metric=90, tolerance=10) is False


def test_09_negative_degradation_rate_treated_as_never_degrading():
    assert days_until_degraded(0.9, 0.9, tolerance=0.05, degradation_rate_per_day=-0.01) == math.inf


# --- Independent correctness oracle -----------------------------------


def test_10_days_until_degraded_scales_inversely_with_rate():
    # Directly targets a mutant that multiplies instead of divides by
    # the degradation rate (which would make faster degradation
    # predict MORE days remaining -- backwards).
    slow = days_until_degraded(0.9, 0.9, tolerance=0.1, degradation_rate_per_day=0.01)
    fast = days_until_degraded(0.9, 0.9, tolerance=0.1, degradation_rate_per_day=0.05)
    assert fast < slow
    assert math.isclose(slow, 10.0)
    assert math.isclose(fast, 2.0)
