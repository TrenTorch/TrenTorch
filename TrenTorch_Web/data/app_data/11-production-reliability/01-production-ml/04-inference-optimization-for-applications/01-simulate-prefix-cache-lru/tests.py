"""pytest tests.py"""

from _load import load_solution

simulate_prefix_cache = load_solution(__file__).simulate_prefix_cache


def test_1_all_misses_within_capacity():
    assert simulate_prefix_cache(3, ["a", "b", "c"]) == [False, False, False]


def test_2_repeat_within_capacity_is_a_hit():
    assert simulate_prefix_cache(3, ["a", "b", "a"]) == [False, False, True]


def test_3_eviction_of_least_recently_used():
    # capacity 2: a, b fill cache; c evicts a (LRU); then a is a miss again.
    assert simulate_prefix_cache(2, ["a", "b", "c", "a"]) == [False, False, False, False]


def test_4_access_refreshes_recency_and_protects_from_eviction():
    # a is re-touched before c arrives, so b (now LRU) gets evicted instead of a.
    result = simulate_prefix_cache(2, ["a", "b", "a", "c", "a", "b"])
    assert result == [False, False, True, False, True, False]


def test_5_empty_requests_returns_empty_list():
    assert simulate_prefix_cache(4, []) == []
