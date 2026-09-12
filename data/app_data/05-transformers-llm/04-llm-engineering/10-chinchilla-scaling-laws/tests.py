"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/10-chinchilla-scaling-laws/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
flops_for_training = _module.flops_for_training
chinchilla_optimal_allocation = _module.chinchilla_optimal_allocation


def test_flops_for_training_matches_the_6nd_formula():
    assert flops_for_training(num_params=1000, num_tokens=2000) == 6.0 * 1000 * 2000


def test_flops_for_training_doubling_params_doubles_flops():
    base = flops_for_training(1e6, 1e9)
    doubled = flops_for_training(2e6, 1e9)
    assert np.isclose(doubled / base, 2.0, atol=1e-6)


def test_flops_for_training_doubling_tokens_doubles_flops():
    base = flops_for_training(1e6, 1e9)
    doubled = flops_for_training(1e6, 2e9)
    assert np.isclose(doubled / base, 2.0, atol=1e-6)


def test_chinchilla_allocation_gives_equal_n_and_d():
    n_opt, d_opt = chinchilla_optimal_allocation(6e20)
    assert np.isclose(n_opt, d_opt, atol=1e-6)


def test_chinchilla_allocation_is_consistent_with_the_flops_formula():
    compute_budget = 6e20
    n_opt, d_opt = chinchilla_optimal_allocation(compute_budget)
    recomputed_flops = flops_for_training(n_opt, d_opt)
    assert np.isclose(recomputed_flops, compute_budget, rtol=1e-6)


def test_doubling_compute_budget_scales_n_and_d_each_by_sqrt_two():
    n_opt_1, d_opt_1 = chinchilla_optimal_allocation(1e20)
    n_opt_2, d_opt_2 = chinchilla_optimal_allocation(2e20)
    assert np.isclose(n_opt_2 / n_opt_1, np.sqrt(2.0), atol=1e-4)
    assert np.isclose(d_opt_2 / d_opt_1, np.sqrt(2.0), atol=1e-4)


def test_ten_x_compute_scales_n_and_d_each_by_sqrt_ten_not_by_ten():
    # Directly targets a mutant that scales N and D each linearly with C
    # (e.g. n_opt = C / 6), rather than with sqrt(C), which would
    # over-allocate both far beyond what a fixed compute budget supports.
    n_opt_1, _ = chinchilla_optimal_allocation(1e20)
    n_opt_2, _ = chinchilla_optimal_allocation(10e20)
    ratio = n_opt_2 / n_opt_1
    assert np.isclose(ratio, np.sqrt(10.0), atol=1e-3)
    assert not np.isclose(ratio, 10.0, atol=1e-3)
