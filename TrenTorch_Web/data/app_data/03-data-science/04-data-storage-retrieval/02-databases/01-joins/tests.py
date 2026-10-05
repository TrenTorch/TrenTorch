"""
pytest tests.py
"""

import random

from _load import load_solution

_module = load_solution(__file__)
nested_loop_join = _module.nested_loop_join
hash_join = _module.hash_join
sort_merge_join = _module.sort_merge_join

CUSTOMERS = [
    {"id": 1, "name": "Asha"},
    {"id": 2, "name": "Ben"},
    {"id": 3, "name": "Chen"},
]
ORDERS = [
    {"id": 2, "item": "pen"},
    {"id": 1, "item": "ink"},
    {"id": 2, "item": "pad"},
    {"id": 9, "item": "ghost"},
]


def _canonical(rows):
    return sorted(sorted(row.items()) for row in rows)


# ---- 1-6: nested loop (the reference) ----


def test_1_hand_computed_inner_join():
    result = nested_loop_join(CUSTOMERS, ORDERS, "id")
    assert result == [
        {"id": 1, "name": "Asha", "item": "ink"},
        {"id": 2, "name": "Ben", "item": "pen"},
        {"id": 2, "name": "Ben", "item": "pad"},
    ]


def test_2_unmatched_rows_are_dropped_from_both_sides():
    result = nested_loop_join(CUSTOMERS, ORDERS, "id")
    assert all(row["id"] in (1, 2) for row in result)


def test_3_duplicate_keys_give_every_combination():
    left = [{"k": 1, "a": "x"}, {"k": 1, "a": "y"}]
    right = [{"k": 1, "b": 1}, {"k": 1, "b": 2}, {"k": 1, "b": 3}]
    assert len(nested_loop_join(left, right, "k")) == 6


def test_4_right_value_wins_on_a_column_name_clash():
    left = [{"k": 1, "v": "left"}]
    right = [{"k": 1, "v": "right"}]
    assert nested_loop_join(left, right, "k") == [{"k": 1, "v": "right"}]


def test_5_empty_tables_give_an_empty_result():
    assert nested_loop_join([], ORDERS, "id") == []
    assert nested_loop_join(CUSTOMERS, [], "id") == []


def test_6_inputs_are_not_modified():
    left = [dict(row) for row in CUSTOMERS]
    right = [dict(row) for row in ORDERS]
    for join in (nested_loop_join, hash_join, sort_merge_join):
        join(left, right, "id")
    assert left == CUSTOMERS and right == ORDERS


# ---- 7-11: hash join ----


def test_7_hash_join_matches_the_nested_loop_exactly_including_order():
    assert hash_join(CUSTOMERS, ORDERS, "id") == nested_loop_join(CUSTOMERS, ORDERS, "id")


def test_8_hash_join_with_duplicate_keys_keeps_the_documented_order():
    left = [{"k": 1, "a": "x"}, {"k": 2, "a": "y"}, {"k": 1, "a": "z"}]
    right = [{"k": 1, "b": 1}, {"k": 1, "b": 2}]
    assert hash_join(left, right, "k") == nested_loop_join(left, right, "k")


def test_9_hash_join_agrees_on_random_tables():
    rng = random.Random(0)
    for _ in range(20):
        left = [{"k": rng.randint(0, 5), "l": i} for i in range(rng.randint(0, 12))]
        right = [{"k": rng.randint(0, 5), "r": i} for i in range(rng.randint(0, 12))]
        assert hash_join(left, right, "k") == nested_loop_join(left, right, "k")


def test_10_hash_join_does_not_compare_every_pair():
    comparisons = []

    class Key:
        def __init__(self, v):
            self.v = v

        def __hash__(self):
            return hash(self.v)

        def __eq__(self, other):
            comparisons.append(1)
            return self.v == other.v

    left = [{"k": Key(i % 50), "l": i} for i in range(400)]
    right = [{"k": Key(i % 50), "r": i} for i in range(400)]
    hash_join(left, right, "k")
    assert len(comparisons) < 400 * 400 / 4


def test_11_hash_join_works_with_string_keys():
    left = [{"city": "pune", "pop": 1}, {"city": "delhi", "pop": 2}]
    right = [{"city": "delhi", "tz": "IST"}]
    assert hash_join(left, right, "city") == [{"city": "delhi", "pop": 2, "tz": "IST"}]


# ---- 12-17: sort-merge join ----


def test_12_sort_merge_returns_rows_ordered_by_key():
    result = sort_merge_join(CUSTOMERS, ORDERS, "id")
    assert [row["id"] for row in result] == [1, 2, 2]
    assert [row["item"] for row in result] == ["ink", "pen", "pad"]


def test_13_sort_merge_returns_the_same_rows_as_the_nested_loop():
    assert _canonical(sort_merge_join(CUSTOMERS, ORDERS, "id")) == _canonical(
        nested_loop_join(CUSTOMERS, ORDERS, "id")
    )


def test_14_sort_merge_handles_runs_of_equal_keys_on_both_sides():
    left = [{"k": 2, "a": 1}, {"k": 1, "a": 2}, {"k": 2, "a": 3}]
    right = [{"k": 2, "b": 1}, {"k": 2, "b": 2}, {"k": 3, "b": 3}]
    result = sort_merge_join(left, right, "k")
    assert [(r["a"], r["b"]) for r in result] == [(1, 1), (1, 2), (3, 1), (3, 2)]


def test_15_sort_merge_agrees_on_random_tables():
    rng = random.Random(1)
    for _ in range(20):
        left = [{"k": rng.randint(0, 6), "l": i} for i in range(rng.randint(0, 15))]
        right = [{"k": rng.randint(0, 6), "r": i} for i in range(rng.randint(0, 15))]
        assert _canonical(sort_merge_join(left, right, "k")) == _canonical(nested_loop_join(left, right, "k"))


def test_16_sort_merge_on_already_sorted_input_and_no_overlap():
    left = [{"k": i} for i in range(5)]
    right = [{"k": i + 10} for i in range(5)]
    assert sort_merge_join(left, right, "k") == []


def test_17_all_three_algorithms_agree_with_all_keys_equal():
    left = [{"k": 7, "l": i} for i in range(4)]
    right = [{"k": 7, "r": i} for i in range(3)]
    assert len(sort_merge_join(left, right, "k")) == 12
    assert hash_join(left, right, "k") == nested_loop_join(left, right, "k")
