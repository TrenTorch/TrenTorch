"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/06-ab-testing-rollback/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
assign_variant = _module.assign_variant
evaluate_ab_test = _module.evaluate_ab_test
decide_rollback = _module.decide_rollback


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_same_user_always_gets_the_same_variant():
    decisions = [assign_variant("user-42", ["control", "treatment"], [50, 50]) for _ in range(10)]
    assert len(set(decisions)) == 1


def test_02_significantly_worse_treatment_triggers_rollback():
    z, p = evaluate_ab_test(500, 1000, 400, 1000)  # treatment clearly worse
    assert decide_rollback(z, p, alpha=0.05) is True


# --- General-case coverage --------------------------------------------


def test_03_significantly_better_treatment_does_not_roll_back():
    z, p = evaluate_ab_test(400, 1000, 500, 1000)  # treatment clearly better
    assert decide_rollback(z, p, alpha=0.05) is False


def test_04_no_significant_difference_does_not_roll_back():
    z, p = evaluate_ab_test(500, 1000, 505, 1000)  # essentially identical
    assert decide_rollback(z, p, alpha=0.05) is False


def test_05_variant_traffic_split_roughly_matches_the_requested_weights():
    n = 5000
    counts = {"A": 0, "B": 0}
    for i in range(n):
        counts[assign_variant(f"user-{i}", ["A", "B"], [70, 30])] += 1
    fraction_a = counts["A"] / n
    assert 0.62 < fraction_a < 0.78  # generous tolerance around the true 70%


# --- Parameter handling -------------------------------------------------


def test_06_assign_variant_only_ever_returns_a_known_variant_name():
    for i in range(200):
        result = assign_variant(f"user-{i}", ["A", "B", "C"], [1, 1, 1])
        assert result in {"A", "B", "C"}


def test_07_rollback_boundary_respects_alpha():
    z, p = evaluate_ab_test(500, 1000, 400, 1000)
    assert decide_rollback(z, p, alpha=1.0) is True  # p always < alpha=1.0
    assert decide_rollback(z, p, alpha=0.0) is False  # p never < alpha=0.0


# --- Edge cases ---------------------------------------------------------


def test_08_two_equal_weights_split_roughly_in_half():
    n = 4000
    counts = {"A": 0, "B": 0}
    for i in range(n):
        counts[assign_variant(f"user-{i}", ["A", "B"], [1, 1])] += 1
    assert 0.4 < counts["A"] / n < 0.6


def test_09_evaluate_ab_test_returns_two_values():
    result = evaluate_ab_test(100, 500, 110, 500)
    assert len(result) == 2


# --- Independent correctness oracle -----------------------------------


def test_10_rollback_never_triggers_from_significance_alone_direction_matters():
    # Directly targets a mutant that rolls back on ANY significant
    # result, regardless of direction (e.g. checking `abs(z) > 0`
    # instead of `z > 0`) -- a significantly BETTER treatment must
    # never be rolled back, even though the difference IS significant.
    z, p = evaluate_ab_test(400, 1000, 500, 1000)  # treatment significantly better
    assert p < 0.05  # confirm this genuinely is a significant result
    assert decide_rollback(z, p, alpha=0.05) is False
