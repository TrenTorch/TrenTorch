"""
pytest tests.py
"""

import math

from _load import load_solution

_module = load_solution(__file__)
build_index = _module.build_index
search = _module.search
range_scan = _module.range_scan
index_height = _module.index_height


# ---- 1-7: building ----


def test_1_hand_computed_levels():
    levels = build_index(list(range(1, 10)), 3)
    assert levels[0] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert levels[1] == [[1, 4, 7]]
    assert len(levels) == 2


def test_2_leaf_level_holds_every_key_in_order():
    keys = list(range(0, 200, 3))
    levels = build_index(keys, 7)
    assert [k for page in levels[0] for k in page] == keys


def test_3_pages_never_exceed_the_fanout_and_only_the_last_may_be_short():
    levels = build_index(list(range(50)), 4)
    for level in levels:
        assert all(len(page) <= 4 for page in level)
        assert all(len(page) == 4 for page in level[:-1])


def test_4_upper_levels_hold_the_first_key_of_each_child_page():
    levels = build_index(list(range(100)), 5)
    firsts = [page[0] for page in levels[0]]
    flattened = [entry for page in levels[1] for entry in page]
    assert flattened == firsts


def test_5_the_top_level_is_a_single_page():
    for n in (1, 5, 6, 26, 125, 1000):
        assert len(build_index(list(range(n)), 5)[-1]) == 1


def test_6_empty_and_tiny_inputs():
    assert build_index([], 4) == [[[]]]
    assert build_index([42], 4) == [[[42]]]
    assert len(build_index([1, 2, 3, 4], 4)) == 1


def test_7_input_keys_are_not_modified():
    keys = [1, 2, 3, 4, 5]
    build_index(keys, 2)
    assert keys == [1, 2, 3, 4, 5]


# ---- 8-12: point lookups ----


def test_8_finds_every_stored_key():
    keys = list(range(0, 1000, 7))
    levels = build_index(keys, 6)
    assert all(search(levels, key)[0] for key in keys)


def test_9_reports_missing_keys_below_between_and_above_the_range():
    keys = list(range(10, 200, 10))
    levels = build_index(keys, 4)
    for missing in (5, 15, 55, 195, 1000, -3):
        assert search(levels, missing)[0] is False


def test_10_pages_read_equals_the_height_for_every_lookup():
    levels = build_index(list(range(500)), 5)
    for key in (0, 17, 250, 499, 999):
        assert search(levels, key)[1] == len(levels)


def test_11_a_single_page_index_reads_one_page():
    assert search(build_index([1, 2, 3], 10), 2) == (True, 1)


def test_12_every_key_in_a_large_index_is_found_with_few_page_reads():
    keys = list(range(0, 100_000, 3))
    levels = build_index(keys, 100)
    found, pages = search(levels, keys[12_345])
    assert found and pages == 3


# ---- 13-17: range scans ----


def test_13_range_returns_the_keys_in_order():
    levels = build_index(list(range(0, 100, 2)), 4)
    keys, _ = range_scan(levels, 11, 25)
    assert keys == [12, 14, 16, 18, 20, 22, 24]


def test_14_range_endpoints_are_inclusive():
    levels = build_index(list(range(20)), 4)
    assert range_scan(levels, 5, 8)[0] == [5, 6, 7, 8]


def test_15_page_reads_are_the_descent_plus_each_extra_leaf_page():
    levels = build_index(list(range(100)), 10)
    keys, pages = range_scan(levels, 0, 99)
    assert len(keys) == 100 and pages == len(levels) + 9


def test_16_empty_and_out_of_range_scans():
    levels = build_index(list(range(0, 100, 10)), 3)
    assert range_scan(levels, 11, 19)[0] == []
    assert range_scan(levels, 500, 900)[0] == []
    assert range_scan(levels, -50, -1)[0] == []


def test_17_range_scan_matches_a_brute_force_filter():
    keys = list(range(0, 5000, 7))
    levels = build_index(keys, 8)
    for low, high in [(0, 100), (333, 2222), (4900, 6000), (10, 10), (14, 14)]:
        assert range_scan(levels, low, high)[0] == [k for k in keys if low <= k <= high]


# ---- 18-20: height ----


def test_18_height_matches_the_built_index():
    for n in (0, 1, 4, 5, 6, 24, 25, 26, 124, 125, 126, 1000, 3000):
        assert index_height(n, 5) == len(build_index(list(range(n)), 5))


def test_19_height_is_logarithmic_in_the_number_of_keys():
    assert index_height(10**6, 100) == 3
    assert index_height(10**9, 100) == 5


def test_20_small_inputs_have_height_one_and_binary_fanout_is_log_two():
    assert index_height(0, 10) == 1 and index_height(10, 10) == 1
    assert index_height(1024, 2) == int(math.log2(1024))
