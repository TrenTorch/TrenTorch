"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/03-ci-cd-for-ml/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
run_model_tests = _module.run_model_tests
pass_rate = _module.pass_rate
gate_deployment = _module.gate_deployment


def _identity_model(x):
    return x


def _broken_model(x):
    raise RuntimeError("model exploded")


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_run_model_tests_reports_pass_and_fail():
    cases = [
        ("returns positive", 5, lambda out: out > 0),
        ("returns negative", 5, lambda out: out < 0),
    ]
    results = run_model_tests(_identity_model, cases)
    assert results[0]["passed"] is True
    assert results[1]["passed"] is False


def test_02_gate_deployment_blocks_when_below_threshold():
    results = [{"test_name": "a", "passed": True}, {"test_name": "b", "passed": False}]
    assert gate_deployment(results, min_pass_rate=0.9) is False


# --- General-case coverage --------------------------------------------


def test_03_pass_rate_matches_hand_computation():
    results = [{"passed": True}, {"passed": True}, {"passed": False}, {"passed": True}]
    assert math.isclose(pass_rate(results), 0.75)


def test_04_gate_deployment_allows_when_above_threshold():
    results = [{"passed": True}] * 9 + [{"passed": False}]
    assert gate_deployment(results, min_pass_rate=0.85) is True


def test_05_exceptions_during_a_test_count_as_a_failure_not_a_crash():
    cases = [("crashes", None, lambda out: True)]
    results = run_model_tests(_broken_model, cases)
    assert results[0]["passed"] is False


# --- Parameter handling -------------------------------------------------


def test_06_gate_deployment_boundary_is_inclusive():
    results = [{"passed": True}] * 8 + [{"passed": False}] * 2  # 0.8 pass rate
    assert gate_deployment(results, min_pass_rate=0.8) is True


def test_07_all_passing_gives_perfect_pass_rate():
    results = [{"passed": True}] * 5
    assert math.isclose(pass_rate(results), 1.0)


# --- Edge cases ---------------------------------------------------------


def test_08_empty_test_suite_is_vacuously_passing():
    assert math.isclose(pass_rate([]), 1.0)
    assert gate_deployment([], min_pass_rate=1.0) is True


def test_09_all_failing_gives_zero_pass_rate():
    results = [{"passed": False}] * 3
    assert math.isclose(pass_rate(results), 0.0)
    assert gate_deployment(results, min_pass_rate=0.01) is False


# --- Independent correctness oracle -----------------------------------


def test_10_gate_deployment_actually_derived_from_pass_rate():
    # Directly targets a mutant that hardcodes gate_deployment's
    # result (e.g. always True) instead of genuinely comparing
    # pass_rate against the threshold.
    results = [{"passed": True}] * 3 + [{"passed": False}] * 7  # 0.3 pass rate
    assert gate_deployment(results, min_pass_rate=0.5) is False
    assert gate_deployment(results, min_pass_rate=0.3) is True
    assert gate_deployment(results, min_pass_rate=0.2) is True
