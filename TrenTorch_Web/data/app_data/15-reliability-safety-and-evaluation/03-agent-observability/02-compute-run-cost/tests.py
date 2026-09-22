"""pytest data/app_data/15-reliability-safety-and-evaluation/03-agent-observability/02-compute-run-cost/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

compute_run_cost = load_solution(
    f"15-reliability-safety-and-evaluation/03-agent-observability/{Path(__file__).resolve().parent.name}"
).compute_run_cost


def test_1_single_call():
    result = compute_run_cost([(1000, 500, 0.01, 0.03)])
    assert result["total_input_tokens"] == 1000
    assert result["total_output_tokens"] == 500
    assert abs(result["total_cost"] - (0.01 + 0.015)) < 1e-9


def test_2_multiple_calls_sum_tokens_and_cost():
    calls = [(1000, 500, 0.01, 0.03), (2000, 1000, 0.01, 0.03)]
    result = compute_run_cost(calls)
    assert result["total_input_tokens"] == 3000
    assert result["total_output_tokens"] == 1500
    assert abs(result["total_cost"] - (0.01 + 0.015 + 0.02 + 0.03)) < 1e-9


def test_3_different_prices_per_call():
    calls = [(1000, 0, 0.01, 0.03), (1000, 0, 0.02, 0.03)]
    result = compute_run_cost(calls)
    assert abs(result["total_cost"] - (0.01 + 0.02)) < 1e-9


def test_4_zero_tokens_zero_cost():
    result = compute_run_cost([(0, 0, 0.01, 0.03)])
    assert result == {"total_input_tokens": 0, "total_output_tokens": 0, "total_cost": 0.0}


def test_5_empty_calls_returns_zeroed_dict():
    assert compute_run_cost([]) == {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost": 0.0,
    }
