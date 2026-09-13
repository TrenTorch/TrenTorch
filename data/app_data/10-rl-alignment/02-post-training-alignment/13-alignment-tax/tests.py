"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/13-alignment-tax/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
alignment_tax = _module.alignment_tax
per_benchmark_regression = _module.per_benchmark_regression
has_net_alignment_tax = _module.has_net_alignment_tax


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_positive_tax_when_aligned_model_is_uniformly_worse():
    base = [0.8, 0.7, 0.9]
    aligned = [0.7, 0.6, 0.85]
    tax = alignment_tax(base, aligned)
    assert tax > 0.0
    assert math.isclose(tax, np.mean([0.1, 0.1, 0.05]))


def test_02_zero_tax_when_scores_are_identical():
    scores = [0.5, 0.6, 0.7]
    assert math.isclose(alignment_tax(scores, scores), 0.0)


# --- General-case coverage --------------------------------------------


def test_03_negative_tax_when_aligned_model_is_uniformly_better():
    base = [0.5, 0.5]
    aligned = [0.6, 0.6]
    assert alignment_tax(base, aligned) < 0.0


def test_04_per_benchmark_regression_matches_elementwise_difference():
    base = np.array([0.9, 0.4, 0.7])
    aligned = np.array([0.85, 0.5, 0.6])
    result = per_benchmark_regression(base, aligned)
    assert np.allclose(result, [0.05, -0.1, 0.1])


def test_05_alignment_tax_is_the_mean_of_per_benchmark_regression():
    base = [0.9, 0.4, 0.7, 0.2]
    aligned = [0.85, 0.5, 0.6, 0.3]
    per_bench = per_benchmark_regression(base, aligned)
    assert math.isclose(alignment_tax(base, aligned), per_bench.mean())


# --- Parameter handling -------------------------------------------------


def test_06_has_net_alignment_tax_true_case():
    base = [0.9, 0.9]
    aligned = [0.5, 0.5]
    assert has_net_alignment_tax(base, aligned) is True


def test_07_has_net_alignment_tax_false_case():
    base = [0.5, 0.5]
    aligned = [0.9, 0.9]
    assert has_net_alignment_tax(base, aligned) is False


# --- Edge cases ---------------------------------------------------------


def test_08_mixed_benchmarks_can_still_net_to_zero():
    base = [0.5, 0.5]
    aligned = [0.6, 0.4]  # one benchmark improves, one regresses by the same amount
    assert math.isclose(alignment_tax(base, aligned), 0.0)


def test_09_single_benchmark_case():
    assert math.isclose(alignment_tax([0.9], [0.7]), 0.2)


# --- Independent correctness oracle -----------------------------------


def test_10_regression_direction_is_base_minus_aligned_not_reversed():
    # Directly targets a mutant that swaps the subtraction order
    # (aligned - base instead of base - aligned), which would report
    # a CAPABILITY GAIN as a tax and vice versa -- the exact opposite
    # of the intended meaning.
    base = [0.9, 0.6]
    aligned = [0.7, 0.5]
    result = per_benchmark_regression(base, aligned)
    assert np.allclose(result, [0.2, 0.1])
    assert not np.allclose(result, [-0.2, -0.1])
