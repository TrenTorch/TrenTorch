"""
pytest tests.py
"""

import math

from _load import load_solution

_module = load_solution(__file__)
BloomFilter = _module.BloomFilter
false_positive_rate = _module.false_positive_rate
optimal_num_hashes = _module.optimal_num_hashes


def _positions(item, num_bits, num_hashes):
    h1 = (item * 2654435761) % 2**32
    h2 = ((item * 40503) % 2**32) | 1
    return [(h1 + i * h2) % num_bits for i in range(num_hashes)]


# ---- 1-8: the filter ----


def test_1_added_items_are_always_found():
    bloom = BloomFilter(2000, 4)
    for item in range(100):
        bloom.add(item)
    assert all(bloom.might_contain(item) for item in range(100))


def test_2_an_empty_filter_contains_nothing():
    bloom = BloomFilter(100, 3)
    assert not any(bloom.might_contain(i) for i in range(200))


def test_3_adding_sets_exactly_the_documented_positions():
    bloom = BloomFilter(64, 3)
    bloom.add(12345)
    expected = set(_positions(12345, 64, 3))
    assert {i for i, bit in enumerate(bloom.bits) if bit} == expected


def test_4_lookup_never_modifies_the_filter():
    bloom = BloomFilter(128, 3)
    bloom.add(7)
    before = list(bloom.bits)
    for i in range(100):
        bloom.might_contain(i)
    assert bloom.bits == before


def test_5_bits_are_a_plain_list_of_zeros_and_ones_of_the_right_length():
    bloom = BloomFilter(50, 2)
    for i in range(30):
        bloom.add(i)
    assert len(bloom.bits) == 50 and set(bloom.bits) <= {0, 1}


def test_6_adding_the_same_item_twice_changes_nothing_the_second_time():
    bloom = BloomFilter(100, 3)
    bloom.add(9)
    snapshot = list(bloom.bits)
    bloom.add(9)
    assert bloom.bits == snapshot


def test_7_a_tiny_filter_gives_false_positives():
    bloom = BloomFilter(8, 2)
    for item in range(20):
        bloom.add(item)
    assert any(bloom.might_contain(item) for item in range(1000, 1050))


def test_8_a_roomy_filter_has_a_low_measured_error_rate():
    bloom = BloomFilter(10_000, 7)
    for item in range(1000):
        bloom.add(item)
    errors = sum(bloom.might_contain(item) for item in range(10_000, 20_000))
    assert errors / 10_000 < 0.05


# ---- 9-13: the error formula ----


def test_9_formula_hand_computed():
    expected = (1 - math.exp(-3 * 100 / 1000)) ** 3
    assert math.isclose(false_positive_rate(100, 1000, 3), expected)


def test_10_error_rises_with_more_items():
    assert false_positive_rate(500, 1000, 3) > false_positive_rate(100, 1000, 3)


def test_11_error_falls_with_more_bits():
    assert false_positive_rate(100, 2000, 3) < false_positive_rate(100, 1000, 3)


def test_12_about_ten_bits_per_item_gives_roughly_one_percent():
    rate = false_positive_rate(1000, 9600, 7)
    assert 0.007 < rate < 0.013


def test_13_predicted_rate_is_close_to_the_measured_rate():
    n, m, k = 2000, 20_000, 7
    bloom = BloomFilter(m, k)
    for item in range(n):
        bloom.add(item)
    measured = sum(bloom.might_contain(i) for i in range(100_000, 130_000)) / 30_000
    assert abs(measured - false_positive_rate(n, m, k)) < 0.005


# ---- 14-17: choosing the number of hashes ----


def test_14_optimal_hashes_hand_computed():
    assert optimal_num_hashes(9600, 1000) == round(9.6 * math.log(2))
    assert optimal_num_hashes(9600, 1000) == 7


def test_15_never_less_than_one():
    assert optimal_num_hashes(10, 1000) == 1


def test_16_the_optimal_choice_beats_neighbouring_choices():
    n, m = 1000, 8000
    best = optimal_num_hashes(m, n)
    rate = lambda k: false_positive_rate(n, m, k)
    assert rate(best) <= rate(max(1, best - 2)) and rate(best) <= rate(best + 2)


def test_17_returns_an_int():
    assert isinstance(optimal_num_hashes(5000, 500), int)
