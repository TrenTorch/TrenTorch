"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/01-online-vs-batch-inference/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
online_inference = _module.online_inference
batch_inference = _module.batch_inference
online_total_overhead = _module.online_total_overhead
batch_total_overhead = _module.batch_total_overhead
worst_case_batch_wait_time = _module.worst_case_batch_wait_time


def _double_model(xs):
    return [x * 2 for x in xs]


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_online_inference_returns_a_single_result():
    assert online_inference(_double_model, 5) == 10


def test_02_batch_inference_processes_all_requests_together():
    assert batch_inference(_double_model, [1, 2, 3]) == [2, 4, 6]


# --- General-case coverage --------------------------------------------


def test_03_online_overhead_scales_with_request_count():
    assert math.isclose(online_total_overhead(100, 0.01), 1.0)


def test_04_batching_reduces_total_overhead():
    online = online_total_overhead(100, 0.01)
    batched = batch_total_overhead(100, 0.01, batch_size=10)
    assert batched < online
    assert math.isclose(batched, 0.1)


def test_05_larger_batches_reduce_overhead_further():
    small_batch = batch_total_overhead(1000, 0.01, batch_size=10)
    large_batch = batch_total_overhead(1000, 0.01, batch_size=100)
    assert large_batch < small_batch


# --- Parameter handling -------------------------------------------------


def test_06_partial_final_batch_still_costs_a_full_overhead_charge():
    # 105 requests, batch_size=10 -> 11 batches (last one only has 5)
    assert math.isclose(batch_total_overhead(105, 1.0, batch_size=10), 11.0)


def test_07_worst_case_wait_time_grows_with_batch_size():
    small = worst_case_batch_wait_time(batch_size=2, per_request_arrival_interval=1.0)
    large = worst_case_batch_wait_time(batch_size=32, per_request_arrival_interval=1.0)
    assert large > small


# --- Edge cases ---------------------------------------------------------


def test_08_batch_size_of_one_matches_online_overhead():
    assert math.isclose(batch_total_overhead(50, 0.02, batch_size=1), online_total_overhead(50, 0.02))


def test_09_batch_size_of_one_has_zero_wait_time():
    assert math.isclose(worst_case_batch_wait_time(batch_size=1, per_request_arrival_interval=5.0), 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_online_and_batch_are_functionally_equivalent_just_grouped_differently():
    # Directly targets a mutant that changes what batch_inference
    # actually computes (e.g. averaging instead of processing each
    # request): calling online_inference on each request individually
    # must match calling batch_inference on all of them at once.
    requests = [1, 2, 3, 4, 5]
    online_results = [online_inference(_double_model, r) for r in requests]
    batched_results = batch_inference(_double_model, requests)
    assert online_results == batched_results
