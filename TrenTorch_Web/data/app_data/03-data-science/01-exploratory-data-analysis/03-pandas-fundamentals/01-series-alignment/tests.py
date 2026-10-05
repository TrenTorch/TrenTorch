"""
pytest tests.py
"""

import math

import numpy as np
import pandas as pd

from _load import load_solution

_module = load_solution(__file__)
make_series = _module.make_series
aligned_sum = _module.aligned_sum
share_of_total = _module.share_of_total
lookup = _module.lookup


def _nan(x):
    return isinstance(x, float) and math.isnan(x)


def _as_dict(s):
    return {k: (None if _nan(v) else v) for k, v in s.items()}


def _reference_sum(a, b, fill):
    result = {}
    for label in sorted(set(a.index) | set(b.index)):
        x = a.get(label, math.nan)
        y = b.get(label, math.nan)
        if fill is not None:
            if _nan(x) and _nan(y):
                result[label] = math.nan
                continue
            x = fill if _nan(x) else x
            y = fill if _nan(y) else y
        result[label] = x + y
    return result


# ---- 1-3: make_series ----


def test_1_values_index_and_name():
    s = make_series([10, 20, 30], ["a", "b", "c"], "sales")
    assert isinstance(s, pd.Series)
    assert s.tolist() == [10, 20, 30]
    assert s.index.tolist() == ["a", "b", "c"]
    assert s.name == "sales"


def test_2_keeps_the_given_label_order_even_if_unsorted():
    s = make_series([1, 2, 3], ["z", "a", "m"], "x")
    assert s.index.tolist() == ["z", "a", "m"]


def test_3_accepts_any_iterable_and_integer_labels():
    s = make_series(range(3), (7, 8, 9), "n")
    assert s.index.tolist() == [7, 8, 9]
    assert s.loc[8] == 1


# ---- 4-10: aligned_sum ----


def test_4_same_labels_adds_elementwise():
    a = pd.Series([1.0, 2.0], index=["x", "y"])
    b = pd.Series([10.0, 20.0], index=["x", "y"])
    assert _as_dict(aligned_sum(a, b)) == {"x": 11.0, "y": 22.0}


def test_5_matches_by_label_not_by_position():
    a = pd.Series([1.0, 2.0, 3.0], index=["x", "y", "z"])
    b = pd.Series([30.0, 10.0, 20.0], index=["z", "x", "y"])
    assert _as_dict(aligned_sum(a, b)) == {"x": 11.0, "y": 22.0, "z": 33.0}


def test_6_label_on_one_side_only_gives_nan():
    a = pd.Series([1.0, 2.0], index=["x", "y"])
    b = pd.Series([5.0, 7.0], index=["y", "z"])
    assert _as_dict(aligned_sum(a, b)) == {"x": None, "y": 7.0, "z": None}


def test_7_result_index_is_the_sorted_union():
    a = pd.Series([1.0, 2.0], index=["q", "b"])
    b = pd.Series([3.0, 4.0], index=["z", "a"])
    assert aligned_sum(a, b).index.tolist() == ["a", "b", "q", "z"]


def test_8_fill_value_replaces_a_missing_label():
    a = pd.Series([1.0, 2.0], index=["x", "y"])
    b = pd.Series([5.0, 7.0], index=["y", "z"])
    assert _as_dict(aligned_sum(a, b, fill_value=0)) == {"x": 1.0, "y": 7.0, "z": 7.0}


def test_9_fill_value_also_replaces_nan_values_but_not_when_both_are_missing():
    a = pd.Series([1.0, np.nan, np.nan], index=["x", "y", "w"])
    b = pd.Series([np.nan, 4.0, np.nan], index=["x", "y", "w"])
    assert _as_dict(aligned_sum(a, b, fill_value=100.0)) == {"w": None, "x": 101.0, "y": 104.0}


def test_10_does_not_change_its_inputs():
    a = pd.Series([1.0, 2.0], index=["x", "y"])
    b = pd.Series([5.0, 7.0], index=["y", "z"])
    a_before, b_before = a.copy(), b.copy()
    aligned_sum(a, b, fill_value=0)
    pd.testing.assert_series_equal(a, a_before)
    pd.testing.assert_series_equal(b, b_before)


def test_11_matches_a_plain_python_reference_on_random_data():
    rng = np.random.default_rng(0)
    for seed in range(8):
        rng = np.random.default_rng(seed)
        labels = list("abcdefghij")
        la = rng.choice(labels, size=6, replace=False).tolist()
        lb = rng.choice(labels, size=6, replace=False).tolist()
        a = pd.Series(rng.integers(0, 50, size=6).astype(float), index=la)
        b = pd.Series(rng.integers(0, 50, size=6).astype(float), index=lb)
        a.iloc[0] = np.nan
        for fill in (None, 0.0, 5.0):
            got = _as_dict(aligned_sum(a, b, fill))
            want = {k: (None if _nan(v) else v) for k, v in _reference_sum(a, b, fill).items()}
            assert got == want


# ---- 12-15: share_of_total ----


def test_12_shares_of_a_simple_series():
    s = pd.Series([1, 3], index=["a", "b"], name="n")
    out = share_of_total(s)
    assert out.tolist() == [0.25, 0.75]


def test_13_missing_values_stay_missing_and_do_not_count_in_the_total():
    s = pd.Series([2.0, np.nan, 6.0], index=["a", "b", "c"])
    out = share_of_total(s)
    assert out.iloc[0] == 0.25 and out.iloc[2] == 0.75
    assert math.isnan(out.iloc[1])


def test_14_keeps_index_and_name_and_returns_floats():
    s = pd.Series([4, 4, 2], index=["x", "y", "z"], name="count")
    out = share_of_total(s)
    assert out.index.tolist() == ["x", "y", "z"]
    assert out.name == "count"
    assert out.dtype.kind == "f"


def test_15_non_missing_shares_sum_to_one():
    s = pd.Series(np.random.default_rng(1).integers(1, 20, size=12), index=list("abcdefghijkl"))
    assert math.isclose(share_of_total(s).sum(), 1.0)


# ---- 16-18: lookup ----


def test_16_returns_values_in_the_requested_order():
    s = pd.Series([10, 20, 30], index=["a", "b", "c"])
    out = lookup(s, ["c", "a"])
    assert out.index.tolist() == ["c", "a"]
    assert out.tolist() == [30, 10]


def test_17_unknown_label_gives_nan_instead_of_an_error():
    s = pd.Series([10.0, 20.0], index=["a", "b"])
    out = lookup(s, ["a", "zzz", "b"])
    assert out.index.tolist() == ["a", "zzz", "b"]
    assert out.iloc[0] == 10.0 and out.iloc[2] == 20.0
    assert math.isnan(out.iloc[1])


def test_18_can_request_labels_more_than_once_and_leaves_the_input_alone():
    s = pd.Series([1.0, 2.0], index=["a", "b"])
    before = s.copy()
    out = lookup(s, ["a", "a", "b"])
    assert out.tolist() == [1.0, 1.0, 2.0]
    pd.testing.assert_series_equal(s, before)
