"""
pytest data/app_data/10-rl-alignment/04-benchmarking-and-capstone/03-capstone-report/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/04-benchmarking-and-capstone/{Path(__file__).resolve().parent.name}")
build_capstone_report = _module.build_capstone_report
compare_capstone_reports = _module.compare_capstone_reports


def _stats(median):
    return {"mean": median, "median": median, "min": median, "max": median, "std": 0.0}


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_report_passes_when_correct_and_faster():
    report = build_capstone_report("proj-a", _stats(10.0), _stats(2.0), correctness_verified=True)
    assert report["passed"] is True
    assert math.isclose(report["speedup_factor"], 5.0)


def test_02_report_fails_when_correctness_not_verified_even_if_faster():
    report = build_capstone_report("proj-b", _stats(10.0), _stats(1.0), correctness_verified=False)
    assert report["passed"] is False


# --- General-case coverage --------------------------------------------


def test_03_report_fails_when_optimized_is_actually_slower():
    report = build_capstone_report("proj-c", _stats(1.0), _stats(10.0), correctness_verified=True)
    assert report["passed"] is False
    assert report["speedup_factor"] < 1.0


def test_04_summary_mentions_the_project_name():
    report = build_capstone_report("my-cool-project", _stats(4.0), _stats(2.0), correctness_verified=True)
    assert "my-cool-project" in report["summary"]


def test_05_compare_reports_picks_the_highest_speedup_among_passing():
    reports = [
        build_capstone_report("slow-but-correct", _stats(10.0), _stats(8.0), True),
        build_capstone_report("fast-and-correct", _stats(10.0), _stats(1.0), True),
    ]
    result = compare_capstone_reports(reports)
    assert result["best_project"] == "fast-and-correct"


# --- Parameter handling -------------------------------------------------


def test_06_a_broken_but_impressive_looking_speedup_never_wins():
    reports = [
        build_capstone_report("broken-super-fast", _stats(10.0), _stats(0.01), correctness_verified=False),
        build_capstone_report("correct-modest", _stats(10.0), _stats(5.0), correctness_verified=True),
    ]
    result = compare_capstone_reports(reports)
    assert result["best_project"] == "correct-modest"


def test_07_num_passing_counts_correctly():
    reports = [
        build_capstone_report("a", _stats(10.0), _stats(5.0), True),
        build_capstone_report("b", _stats(10.0), _stats(5.0), False),
        build_capstone_report("c", _stats(10.0), _stats(2.0), True),
    ]
    result = compare_capstone_reports(reports)
    assert result["num_passing"] == 2


# --- Edge cases ---------------------------------------------------------


def test_08_no_passing_reports_returns_none():
    reports = [build_capstone_report("only-one", _stats(10.0), _stats(5.0), correctness_verified=False)]
    result = compare_capstone_reports(reports)
    assert result["best_project"] is None
    assert result["num_passing"] == 0


def test_09_exactly_one_x_speedup_does_not_pass():
    report = build_capstone_report("no-improvement", _stats(5.0), _stats(5.0), correctness_verified=True)
    assert report["passed"] is False


# --- Independent correctness oracle -----------------------------------


def test_10_best_project_selection_is_based_on_speedup_not_submission_order():
    # Directly targets a mutant that just returns the first (or last)
    # passing report instead of genuinely comparing speedup factors.
    reports = [
        build_capstone_report("first-submitted", _stats(10.0), _stats(9.0), True),
        build_capstone_report("last-submitted", _stats(10.0), _stats(9.5), True),
        build_capstone_report("actually-best", _stats(10.0), _stats(0.5), True),
    ]
    result = compare_capstone_reports(reports)
    assert result["best_project"] == "actually-best"
    assert math.isclose(result["best_speedup_factor"], 20.0)
