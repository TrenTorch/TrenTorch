"""
pytest data/app_data/11-production-ml/03-monitoring-and-drift/04-retraining-strategies/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/03-monitoring-and-drift/{Path(__file__).resolve().parent.name}")
scheduled_retrain_due = _module.scheduled_retrain_due
triggered_retrain_due = _module.triggered_retrain_due
online_update_step = _module.online_update_step


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_scheduled_retrain_due_matches_the_interval():
    assert scheduled_retrain_due(days_since_last_retrain=30, schedule_interval_days=30) is True
    assert scheduled_retrain_due(days_since_last_retrain=29, schedule_interval_days=30) is False


def test_02_triggered_retrain_due_matches_degradation():
    assert triggered_retrain_due(current_metric=0.80, baseline_metric=0.90, tolerance=0.05) is True
    assert triggered_retrain_due(current_metric=0.89, baseline_metric=0.90, tolerance=0.05) is False


# --- General-case coverage --------------------------------------------


def test_03_online_update_reduces_the_squared_error():
    def loss(w, b, x, y):
        return (w * x + b - y) ** 2

    w, b, x, y, lr = 0.5, 0.1, 2.0, 3.0, 0.01
    new_w, new_b = online_update_step(w, b, x, y, lr)
    assert loss(new_w, new_b, x, y) < loss(w, b, x, y)


def test_04_online_update_matches_hand_computation():
    # w=0.5, b=0.1, x=2, y=3: pred=1.1, error=-1.9
    # grad_w = 2*2*-1.9 = -7.6, grad_b = 2*-1.9 = -3.8
    new_w, new_b = online_update_step(0.5, 0.1, 2.0, 3.0, learning_rate=0.01)
    assert math.isclose(new_w, 0.5 - 0.01 * -7.6)
    assert math.isclose(new_b, 0.1 - 0.01 * -3.8)


def test_05_repeated_online_updates_converge_toward_a_perfect_fit():
    w, b = 0.0, 0.0
    x, y = 2.0, 5.0
    for _ in range(500):
        w, b = online_update_step(w, b, x, y, learning_rate=0.01)
    assert math.isclose(w * x + b, y, abs_tol=0.05)


# --- Parameter handling -------------------------------------------------


def test_06_scheduled_retrain_never_due_before_the_interval_elapses():
    for days in range(29):
        assert scheduled_retrain_due(days, schedule_interval_days=30) is False


def test_07_triggered_and_scheduled_are_independent_signals():
    # A model well within tolerance but past its schedule interval
    # should still trigger the SCHEDULED strategy, even though the
    # TRIGGERED strategy sees no need to retrain at all.
    assert scheduled_retrain_due(days_since_last_retrain=100, schedule_interval_days=30) is True
    assert triggered_retrain_due(current_metric=0.90, baseline_metric=0.90, tolerance=0.05) is False


# --- Edge cases ---------------------------------------------------------


def test_08_zero_learning_rate_leaves_parameters_unchanged():
    new_w, new_b = online_update_step(1.0, 2.0, x=3.0, y=4.0, learning_rate=0.0)
    assert new_w == 1.0
    assert new_b == 2.0


def test_09_zero_days_since_retrain_is_never_due_for_a_positive_interval():
    assert scheduled_retrain_due(days_since_last_retrain=0, schedule_interval_days=7) is False


# --- Independent correctness oracle -----------------------------------


def test_10_online_update_gradient_matches_finite_differences():
    # Directly targets a mutant that drops the factor of 2 in the
    # gradient (a common, easy-to-miss error when differentiating a
    # squared term) -- cross-check the analytic gradient step's
    # direction and magnitude against a true finite-difference estimate.
    w, b, x, y, lr = 0.3, -0.2, 1.5, 2.0, 0.001

    def loss(w, b):
        return (w * x + b - y) ** 2

    eps = 1e-6
    numeric_grad_w = (loss(w + eps, b) - loss(w - eps, b)) / (2 * eps)
    numeric_grad_b = (loss(w, b + eps) - loss(w, b - eps)) / (2 * eps)

    new_w, new_b = online_update_step(w, b, x, y, lr)
    implied_grad_w = (w - new_w) / lr
    implied_grad_b = (b - new_b) / lr

    assert math.isclose(implied_grad_w, numeric_grad_w, rel_tol=1e-3)
    assert math.isclose(implied_grad_b, numeric_grad_b, rel_tol=1e-3)
