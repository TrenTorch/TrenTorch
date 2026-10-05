"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
missingness_rate_by_group = _module.missingness_rate_by_group
mean_by_missingness = _module.mean_by_missingness
likely_mechanism = _module.likely_mechanism
add_missing_indicators = _module.add_missing_indicators

nan = np.nan


# ---- 1-4: missing rate by group ----


def test_1_rates_match_a_hand_computed_case():
    x = np.array([1.0, nan, 3.0, nan, nan, 6.0])
    groups = np.array(["a", "a", "a", "b", "b", "b"])
    rates = missingness_rate_by_group(x, groups)
    assert np.isclose(rates["a"], 1 / 3)
    assert np.isclose(rates["b"], 2 / 3)


def test_2_group_with_no_gaps_has_rate_zero():
    rates = missingness_rate_by_group(np.array([1.0, 2.0, nan]), np.array([0, 0, 1]))
    assert rates[0] == 0.0 and rates[1] == 1.0


def test_3_every_label_appears_as_a_key():
    groups = np.array(["x", "y", "z", "x"])
    rates = missingness_rate_by_group(np.array([1.0, nan, 3.0, 4.0]), groups)
    assert set(rates) == {"x", "y", "z"}


def test_4_rates_are_between_zero_and_one_and_return_floats():
    rng = np.random.default_rng(0)
    x = np.where(rng.random(50) < 0.3, nan, 1.0)
    rates = missingness_rate_by_group(x, rng.integers(0, 3, size=50))
    assert all(0.0 <= r <= 1.0 and isinstance(r, float) for r in rates.values())


# ---- 5-8: means split by missingness ----


def test_5_means_hand_computed():
    target = np.array([1.0, nan, 3.0, nan])
    other = np.array([10.0, 20.0, 30.0, 40.0])
    observed, missing = mean_by_missingness(target, other)
    assert np.isclose(observed, 20.0) and np.isclose(missing, 30.0)


def test_6_empty_side_gives_nan():
    observed, missing = mean_by_missingness(np.array([1.0, 2.0]), np.array([5.0, 7.0]))
    assert np.isclose(observed, 6.0) and np.isnan(missing)
    observed, missing = mean_by_missingness(np.array([nan, nan]), np.array([5.0, 7.0]))
    assert np.isnan(observed) and np.isclose(missing, 6.0)


def test_7_returns_plain_floats():
    observed, missing = mean_by_missingness(np.array([1.0, nan]), np.array([1.0, 2.0]))
    assert isinstance(observed, float) and isinstance(missing, float)


def test_8_target_values_themselves_do_not_matter_only_whether_present():
    other = np.array([1.0, 2.0, 3.0, 4.0])
    a = mean_by_missingness(np.array([100.0, nan, -5.0, nan]), other)
    b = mean_by_missingness(np.array([0.0, nan, 0.0, nan]), other)
    assert a == b


# ---- 9-13: the verdict ----


def test_9_random_gaps_look_mcar():
    rng = np.random.default_rng(1)
    other = rng.normal(size=4000)
    target = np.where(rng.random(4000) < 0.3, nan, 1.0)
    assert likely_mechanism(target, other) == "MCAR-like"


def test_10_gaps_that_follow_another_column_look_mar():
    rng = np.random.default_rng(2)
    other = rng.normal(size=4000)
    target = np.where(other > 0.5, nan, 1.0)
    assert likely_mechanism(target, other) == "MAR-like"


def test_11_no_gaps_is_mcar_like():
    assert likely_mechanism(np.array([1.0, 2.0, 3.0]), np.array([5.0, 9.0, 1.0])) == "MCAR-like"


def test_12_constant_other_column_is_mcar_like():
    assert likely_mechanism(np.array([1.0, nan, 3.0]), np.array([4.0, 4.0, 4.0])) == "MCAR-like"


def test_13_threshold_controls_the_verdict():
    target = np.array([1.0, nan, 1.0, nan])
    other = np.array([0.0, 1.0, 0.0, 1.0])  # gap 1.0, std 0.5, so d = 2
    assert likely_mechanism(target, other, threshold=1.0) == "MAR-like"
    assert likely_mechanism(target, other, threshold=3.0) == "MCAR-like"


# ---- 14-18: missing indicators ----


def test_14_indicator_columns_only_for_gappy_columns():
    x = np.array([[1.0, nan, 3.0], [4.0, 5.0, nan], [7.0, 8.0, 9.0]])
    result = add_missing_indicators(x)
    assert result.shape == (3, 5)  # 3 original + flags for columns 1 and 2


def test_15_flags_are_correct_and_in_column_order():
    x = np.array([[1.0, nan, 3.0], [4.0, 5.0, nan], [7.0, 8.0, 9.0]])
    result = add_missing_indicators(x)
    np.testing.assert_array_equal(result[:, 3], [1.0, 0.0, 0.0])  # column 1
    np.testing.assert_array_equal(result[:, 4], [0.0, 1.0, 0.0])  # column 2


def test_16_original_columns_are_unchanged_including_nan():
    x = np.array([[1.0, nan], [2.0, 3.0]])
    result = add_missing_indicators(x)
    np.testing.assert_array_equal(result[:, :2], x)


def test_17_array_without_gaps_is_returned_unchanged_in_shape():
    x = np.arange(6.0).reshape(3, 2)
    result = add_missing_indicators(x)
    np.testing.assert_array_equal(result, x)


def test_18_input_is_not_modified():
    x = np.array([[1.0, nan], [2.0, 3.0]])
    original = x.copy()
    add_missing_indicators(x)
    np.testing.assert_array_equal(x, original)
