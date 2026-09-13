"""
pytest data/app_data/08-systems-performance/04-compression/02-iterative-pruning-schedule/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/04-compression/{Path(__file__).resolve().parent.name}")
cubic_sparsity_schedule = _module.cubic_sparsity_schedule
iterative_prune = _module.iterative_prune


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_schedule_starts_at_zero_sparsity():
    assert cubic_sparsity_schedule(0, 10, 0.9) == 0.0


def test_02_schedule_reaches_target_exactly_at_the_final_step():
    assert cubic_sparsity_schedule(10, 10, 0.9) == 0.9


# --- Shape / general-case coverage -----------------------------------


def test_03_schedule_is_monotonically_increasing():
    values = [cubic_sparsity_schedule(s, 10, 0.9) for s in range(11)]
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def test_04_schedule_is_front_loaded_more_pruning_happens_early():
    # The cubic schedule should cover more than half the target sparsity
    # within the first half of the steps (aggressive early, tapering
    # off later) -- a linear schedule would hit exactly half at the
    # halfway point.
    halfway = cubic_sparsity_schedule(5, 10, 0.9)
    assert halfway > 0.45  # more than half of 0.9 reached by step 5 of 10


# --- Parameter handling -------------------------------------------------


def test_05_step_beyond_total_steps_is_clamped_to_target():
    assert cubic_sparsity_schedule(15, 10, 0.9) == 0.9


def test_06_iterative_prune_returns_one_array_per_step():
    w = np.random.default_rng(0).normal(size=20)
    result = iterative_prune(w, target_sparsity=0.8, num_steps=4)
    assert len(result) == 4
    for arr in result:
        assert arr.shape == w.shape


def test_07_iterative_prune_final_step_reaches_target_sparsity_fraction():
    w = np.random.default_rng(1).normal(size=100)
    result = iterative_prune(w, target_sparsity=0.5, num_steps=5)
    final_zero_fraction = np.mean(result[-1] == 0.0)
    assert np.isclose(final_zero_fraction, 0.5, atol=0.02)


# --- Edge cases ---------------------------------------------------------


def test_08_sparsity_never_decreases_across_iterative_prune_steps():
    w = np.random.default_rng(2).normal(size=50)
    result = iterative_prune(w, target_sparsity=0.7, num_steps=6)
    zero_counts = [np.count_nonzero(arr == 0.0) for arr in result]
    assert all(zero_counts[i] <= zero_counts[i + 1] for i in range(len(zero_counts) - 1))


def test_09_single_step_schedule_jumps_straight_to_target():
    w = np.random.default_rng(3).normal(size=20)
    result = iterative_prune(w, target_sparsity=0.6, num_steps=1)
    assert len(result) == 1
    assert np.isclose(np.mean(result[0] == 0.0), 0.6, atol=0.05)


# --- Array hygiene ------------------------------------------------------


def test_10_does_not_mutate_the_original_weight_across_steps():
    w = np.random.default_rng(4).normal(size=30)
    w_copy = w.copy()
    iterative_prune(w, target_sparsity=0.5, num_steps=3)
    assert np.array_equal(w, w_copy)


# --- Independent correctness oracle -----------------------------------


def test_11_matches_the_published_cubic_pruning_schedule_formula():
    # This is the exact cubic sparsity schedule published in Zhu & Gupta,
    # "To prune, or not to prune" (2017), used as the default pruning
    # schedule in TensorFlow's Model Optimization Toolkit -- not our own
    # derivation. With initial sparsity 0: s_t = s_f * (1 - (1 - t/n)^3).
    # At t/n = 0.3 with s_f = 1.0: s_t = 1 - 0.7^3 = 1 - 0.343 = 0.657.
    result = cubic_sparsity_schedule(3, 10, 1.0)
    assert np.isclose(result, 0.657, atol=1e-9)
