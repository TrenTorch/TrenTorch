"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
HashTable = _module.HashTable


# ---- 1-6: basic operations ----


def test_1_put_and_get():
    table = HashTable()
    table.put(1, "one")
    table.put(2, "two")
    assert table.get(1) == "one" and table.get(2) == "two"


def test_2_missing_key_returns_the_default():
    table = HashTable()
    assert table.get(5) is None
    assert table.get(5, "none") == "none"


def test_3_put_replaces_an_existing_value_without_growing_the_size():
    table = HashTable()
    table.put("a", 1)
    table.put("a", 2)
    assert table.get("a") == 2 and len(table) == 1


def test_4_delete_returns_whether_the_key_was_present():
    table = HashTable()
    table.put(3, "x")
    assert table.delete(3) is True
    assert table.delete(3) is False
    assert table.get(3) is None and len(table) == 0


def test_5_len_counts_distinct_keys():
    table = HashTable()
    for i in range(5):
        table.put(i, i)
    table.delete(2)
    assert len(table) == 4


def test_6_works_with_string_and_tuple_keys():
    table = HashTable()
    table.put("word", 1)
    table.put((1, 2), "pair")
    assert table.get("word") == 1 and table.get((1, 2)) == "pair"


# ---- 7-11: collisions ----


def test_7_colliding_keys_share_a_bucket_and_both_survive():
    table = HashTable(capacity=8)
    table.put(1, "a")
    table.put(9, "b")  # 9 % 8 == 1
    table.put(17, "c")  # 17 % 8 == 1
    assert [table.get(1), table.get(9), table.get(17)] == ["a", "b", "c"]
    assert len(table.buckets[1]) == 3


def test_8_deleting_one_of_several_colliding_keys_keeps_the_others():
    table = HashTable(capacity=8)
    for key in (1, 9, 17):
        table.put(key, key)
    table.delete(9)
    assert table.get(1) == 1 and table.get(17) == 17 and table.get(9) is None


def test_9_replacing_a_value_in_a_colliding_bucket():
    table = HashTable(capacity=8)
    table.put(1, "a")
    table.put(9, "b")
    table.put(9, "B")
    assert table.get(9) == "B" and table.get(1) == "a" and len(table) == 2


def test_10_key_equal_but_different_type_is_treated_as_the_same_key():
    table = HashTable()
    table.put(2, "int")
    table.put(2.0, "float")  # 2 == 2.0 and hash(2) == hash(2.0)
    assert len(table) == 1 and table.get(2) == "float"


def test_11_buckets_hold_pairs_as_tuples():
    table = HashTable(capacity=4)
    table.put(1, "v")
    assert table.buckets[1] == [(1, "v")]


# ---- 12-17: growth ----


def test_12_capacity_doubles_when_the_load_factor_passes_three_quarters():
    table = HashTable(capacity=4)
    for i in range(3):
        table.put(i, i)
    assert table.capacity == 4  # load factor 0.75 is not above 0.75
    table.put(3, 3)
    assert table.capacity == 8


def test_13_everything_is_still_found_after_growth():
    table = HashTable(capacity=2)
    for i in range(200):
        table.put(i, i * i)
    assert table.capacity > 2
    assert all(table.get(i) == i * i for i in range(200))
    assert len(table) == 200


def test_14_load_factor_stays_at_or_below_the_limit():
    table = HashTable(capacity=2)
    for i in range(500):
        table.put(i, i)
        assert table.load_factor() <= 0.75


def test_15_replacing_a_value_never_triggers_growth():
    table = HashTable(capacity=4)
    for i in range(3):
        table.put(i, i)
    for _ in range(10):
        table.put(0, "again")
    assert table.capacity == 4


def test_16_rehash_places_pairs_by_the_new_modulus():
    table = HashTable(capacity=4)
    for i in (0, 1, 2, 3):
        table.put(i, i)  # fourth insert grows to 8
    for key in (0, 1, 2, 3):
        assert (key, key) in table.buckets[key % table.capacity]


def test_17_load_factor_is_len_over_capacity():
    table = HashTable(capacity=16)
    for i in range(4):
        table.put(i, i)
    assert table.load_factor() == 4 / 16


# ---- 18-20: keys ----


def test_18_keys_lists_every_key_once():
    table = HashTable()
    for i in (5, 1, 9, 3):
        table.put(i, i)
    assert sorted(table.keys()) == [1, 3, 5, 9]


def test_19_keys_after_delete_and_growth():
    table = HashTable(capacity=2)
    for i in range(20):
        table.put(i, i)
    for i in range(0, 20, 2):
        table.delete(i)
    assert sorted(table.keys()) == list(range(1, 20, 2))


def test_20_empty_table():
    table = HashTable()
    assert len(table) == 0 and table.keys() == [] and table.load_factor() == 0.0
