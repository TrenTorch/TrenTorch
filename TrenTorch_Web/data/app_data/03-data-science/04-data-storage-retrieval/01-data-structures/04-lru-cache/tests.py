"""
pytest tests.py
"""

import random

from _load import load_solution

_module = load_solution(__file__)
LRUCache = _module.LRUCache


# ---- 1-6: basic behaviour ----


def test_1_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1 and cache.get("b") == 2


def test_2_missing_key_returns_none():
    cache = LRUCache(2)
    assert cache.get("x") is None


def test_3_eviction_removes_the_least_recently_used_entry():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # evicts a
    assert cache.get("a") is None and cache.get("b") == 2 and cache.get("c") == 3


def test_4_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # a is now most recent, b is oldest
    cache.put("c", 3)  # evicts b
    assert cache.get("b") is None and cache.get("a") == 1


def test_5_put_on_an_existing_key_replaces_the_value_and_refreshes_it():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)  # evicts b, not a
    assert cache.get("a") == 10 and cache.get("b") is None


def test_6_updating_an_existing_key_does_not_evict_anything():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("b", 20)
    assert len(cache) == 2 and cache.get("a") == 1


# ---- 7-11: recency order ----


def test_7_keys_by_recency_most_recent_first():
    cache = LRUCache(3)
    for key in "abc":
        cache.put(key, 0)
    assert cache.keys_by_recency() == ["c", "b", "a"]


def test_8_get_moves_a_key_to_the_front():
    cache = LRUCache(3)
    for key in "abc":
        cache.put(key, 0)
    cache.get("a")
    assert cache.keys_by_recency() == ["a", "c", "b"]


def test_9_a_miss_changes_nothing():
    cache = LRUCache(3)
    for key in "ab":
        cache.put(key, 0)
    cache.get("zzz")
    assert cache.keys_by_recency() == ["b", "a"]


def test_10_order_after_eviction():
    cache = LRUCache(2)
    cache.put(1, "x")
    cache.put(2, "y")
    cache.put(3, "z")
    assert cache.keys_by_recency() == [3, 2]


def test_11_empty_cache_has_no_keys():
    cache = LRUCache(4)
    assert cache.keys_by_recency() == [] and len(cache) == 0


# ---- 12-15: capacity edge cases ----


def test_12_capacity_one_keeps_only_the_latest_entry():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") is None and cache.get("b") == 2 and len(cache) == 1


def test_13_size_never_exceeds_the_capacity():
    cache = LRUCache(5)
    for i in range(100):
        cache.put(i, i)
        assert len(cache) <= 5
    assert cache.keys_by_recency() == [99, 98, 97, 96, 95]


def test_14_values_can_be_falsy_and_still_count_as_present():
    cache = LRUCache(2)
    cache.put("zero", 0)
    cache.put("empty", [])
    assert cache.get("zero") == 0 and cache.get("empty") == []


def test_15_evicted_key_can_be_added_again():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 3)
    assert cache.get("a") == 3 and cache.get("b") is None


# ---- 16-18: against a simple model ----


class _Model:
    """A slow list-based LRU used as an oracle."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.order = []  # most recent last
        self.data = {}

    def get(self, key):
        if key not in self.data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.order.remove(key)
        elif len(self.data) >= self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)


def test_16_matches_the_model_on_a_random_workload():
    rng = random.Random(0)
    cache, model = LRUCache(4), _Model(4)
    for _ in range(2000):
        key = rng.randint(0, 9)
        if rng.random() < 0.5:
            assert cache.get(key) == model.get(key)
        else:
            value = rng.randint(0, 99)
            cache.put(key, value)
            model.put(key, value)
        assert cache.keys_by_recency() == model.order[::-1]


def test_17_hit_rate_improves_for_repeated_keys():
    cache = LRUCache(3)
    hits = 0
    for key in [1, 2, 3] * 20:
        if cache.get(key) is not None:
            hits += 1
        else:
            cache.put(key, key)
    assert hits == 57


def test_18_a_scan_larger_than_the_cache_evicts_everything_useful():
    cache = LRUCache(3)
    for key in (1, 2, 3):
        cache.put(key, key)
    for key in range(10, 20):
        cache.put(key, key)
    assert cache.get(1) is None and cache.get(2) is None and cache.get(3) is None
