"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/04-canary-deployment/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
hash_bucket = _module.hash_bucket
is_routed_to_canary = _module.is_routed_to_canary
route_request = _module.route_request


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_same_request_id_always_routes_the_same_way():
    decisions = [is_routed_to_canary("user-42", 15) for _ in range(20)]
    assert len(set(decisions)) == 1


def test_02_zero_percent_canary_never_routes_there():
    assert not any(is_routed_to_canary(f"user-{i}", 0) for i in range(200))


# --- General-case coverage --------------------------------------------


def test_03_hundred_percent_canary_always_routes_there():
    assert all(is_routed_to_canary(f"user-{i}", 100) for i in range(200))


def test_04_canary_fraction_is_roughly_the_requested_percentage():
    n = 5000
    routed = sum(is_routed_to_canary(f"user-{i}", 20) for i in range(n))
    fraction = routed / n
    assert 0.15 < fraction < 0.25  # generous tolerance around the true 20%


def test_05_hash_bucket_is_deterministic_and_within_range():
    for key in ["a", "b", "request-123"]:
        bucket = hash_bucket(key, num_buckets=50)
        assert 0 <= bucket < 50
        assert bucket == hash_bucket(key, num_buckets=50)


# --- Parameter handling -------------------------------------------------


def test_06_route_request_dispatches_to_the_correct_model():
    def canary(req):
        return "canary-response"

    def stable(req):
        return "stable-response"

    # Find a request_id known to route to canary at 100%, and one at 0%.
    canary_result = route_request("any-id", 100, canary, stable)
    stable_result = route_request("any-id", 0, canary, stable)
    assert canary_result == "canary-response"
    assert stable_result == "stable-response"


def test_07_different_request_ids_can_route_differently():
    decisions = {is_routed_to_canary(f"user-{i}", 50) for i in range(50)}
    assert decisions == {True, False}  # a 50% split should produce both outcomes


# --- Edge cases ---------------------------------------------------------


def test_08_empty_string_request_id_still_routes_deterministically():
    a = is_routed_to_canary("", 30)
    b = is_routed_to_canary("", 30)
    assert a == b


def test_09_bucket_count_of_one_puts_everything_in_bucket_zero():
    assert hash_bucket("anything", num_buckets=1) == 0


# --- Independent correctness oracle -----------------------------------


def test_10_routing_decision_is_a_genuine_function_of_request_id_not_random():
    # Directly targets a mutant that uses real randomness (e.g.
    # random.random() < percentage/100) instead of a deterministic
    # hash -- the SAME request_id must produce the SAME decision
    # across a fresh process-level call, not just within one loop.
    first_pass = [is_routed_to_canary(f"stable-check-{i}", 37) for i in range(30)]
    second_pass = [is_routed_to_canary(f"stable-check-{i}", 37) for i in range(30)]
    assert first_pass == second_pass
