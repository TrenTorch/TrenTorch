"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sturges_bins = _module.sturges_bins
freedman_diaconis_bins = _module.freedman_diaconis_bins
bin_edges = _module.bin_edges
histogram_counts = _module.histogram_counts


# ---- 1-4: Sturges ----


def test_1_known_values():
    assert sturges_bins(1) == 1
    assert sturges_bins(8) == 4
    assert sturges_bins(1000) == 11


def test_2_rounds_up_between_powers_of_two():
    assert sturges_bins(9) == 5
    assert sturges_bins(17) == 6


def test_3_grows_slowly_with_n():
    assert sturges_bins(10**6) == 21


def test_4_matches_numpy_sturges():
    for n in (5, 50, 500):
        x = np.random.default_rng(n).normal(size=n)
        assert sturges_bins(n) == len(np.histogram_bin_edges(x, bins="sturges")) - 1


# ---- 5-9: Freedman-Diaconis ----


def test_5_matches_a_hand_computed_case():
    x = np.arange(1.0, 9.0)  # n = 8, q1 = 2.75, q3 = 6.25, iqr = 3.5, range 7
    width = 2 * 3.5 / 8 ** (1 / 3)
    assert freedman_diaconis_bins(x) == math.ceil(7 / width)


def test_6_matches_numpy_fd_on_random_data():
    for seed in range(5):
        x = np.random.default_rng(seed).normal(size=400)
        assert freedman_diaconis_bins(x) == len(np.histogram_bin_edges(x, bins="fd")) - 1


def test_7_outliers_do_not_inflate_the_width_as_much_as_the_range():
    base = np.random.default_rng(1).normal(size=300)
    with_outlier = np.append(base, 1000.0)
    assert freedman_diaconis_bins(with_outlier) > freedman_diaconis_bins(base)


def test_8_zero_iqr_falls_back_to_sturges():
    x = np.array([5.0] * 30 + [9.0])
    assert freedman_diaconis_bins(x) == sturges_bins(31)


def test_9_returns_at_least_one_bin():
    assert freedman_diaconis_bins(np.array([1.0, 1.1, 1.2, 1.3, 40.0])) >= 1


# ---- 10-12: edges ----


def test_10_edges_span_the_data_evenly():
    np.testing.assert_allclose(bin_edges(np.array([2.0, 10.0, 6.0]), 4), [2.0, 4.0, 6.0, 8.0, 10.0])


def test_11_edge_count_is_bins_plus_one():
    assert bin_edges(np.random.default_rng(0).normal(size=50), 7).shape == (8,)


def test_12_edges_match_numpy():
    x = np.random.default_rng(2).normal(size=60)
    np.testing.assert_allclose(bin_edges(x, 6), np.histogram_bin_edges(x, bins=6))


# ---- 13-19: counts ----


def test_13_counts_hand_computed():
    x = np.array([0.0, 1.0, 1.5, 2.5, 3.0])
    np.testing.assert_array_equal(histogram_counts(x, np.array([0.0, 1.0, 2.0, 3.0])), [1, 2, 2])


def test_14_inner_edges_belong_to_the_bin_on_their_right():
    np.testing.assert_array_equal(histogram_counts(np.array([1.0]), np.array([0.0, 1.0, 2.0])), [0, 1])


def test_15_last_bin_includes_its_right_edge():
    np.testing.assert_array_equal(histogram_counts(np.array([2.0]), np.array([0.0, 1.0, 2.0])), [0, 1])


def test_16_values_outside_the_edges_are_ignored():
    x = np.array([-5.0, 0.5, 1.5, 99.0])
    np.testing.assert_array_equal(histogram_counts(x, np.array([0.0, 1.0, 2.0])), [1, 1])


def test_17_counts_match_numpy_histogram():
    for seed in range(5):
        x = np.random.default_rng(seed).normal(size=500)
        edges = bin_edges(x, 12)
        np.testing.assert_array_equal(histogram_counts(x, edges), np.histogram(x, bins=edges)[0])


def test_18_counts_sum_to_the_number_of_values_when_edges_cover_the_data():
    x = np.random.default_rng(3).exponential(size=300)
    assert histogram_counts(x, bin_edges(x, 9)).sum() == 300


def test_19_empty_bins_appear_as_zeros_and_dtype_is_integer():
    counts = histogram_counts(np.array([0.1, 0.2, 9.9]), np.array([0.0, 1.0, 5.0, 10.0]))
    np.testing.assert_array_equal(counts, [2, 0, 1])
    assert counts.dtype.kind == "i"
