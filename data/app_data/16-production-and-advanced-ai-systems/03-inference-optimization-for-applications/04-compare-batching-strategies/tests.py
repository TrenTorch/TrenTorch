"""pytest data/app_data/16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/04-compare-batching-strategies/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

compare_batching_strategies = load_solution(
    f"16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/{Path(__file__).resolve().parent.name}"
).compare_batching_strategies


def test_1_evenly_divisible_batches():
    result = compare_batching_strategies(
        num_requests=10, max_batch_size=5, per_request_ms=2.0, per_batch_overhead_ms=10.0
    )
    assert result["individual_total_ms"] == 120.0
    assert result["batched_total_ms"] == 40.0
    assert result["savings_ms"] == 80.0


def test_2_requests_not_evenly_divisible_rounds_up_batch_count():
    result = compare_batching_strategies(
        num_requests=11, max_batch_size=5, per_request_ms=2.0, per_batch_overhead_ms=10.0
    )
    # 3 batches needed (5, 5, 1) even though the last is partial.
    assert result["batched_total_ms"] == 11 * 2.0 + 3 * 10.0


def test_3_batch_size_one_yields_no_savings():
    result = compare_batching_strategies(
        num_requests=5, max_batch_size=1, per_request_ms=2.0, per_batch_overhead_ms=10.0
    )
    assert result["savings_ms"] == 0.0


def test_4_zero_overhead_yields_no_savings_either():
    result = compare_batching_strategies(
        num_requests=8, max_batch_size=4, per_request_ms=3.0, per_batch_overhead_ms=0.0
    )
    assert result["individual_total_ms"] == result["batched_total_ms"]
    assert result["savings_ms"] == 0.0


def test_5_zero_requests_yields_zero_everywhere():
    result = compare_batching_strategies(
        num_requests=0, max_batch_size=4, per_request_ms=2.0, per_batch_overhead_ms=10.0
    )
    assert result == {"individual_total_ms": 0.0, "batched_total_ms": 0.0, "savings_ms": 0.0}
