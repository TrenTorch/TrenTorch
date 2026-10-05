"""
pytest tests.py
"""

import math

import numpy as np
import pandas as pd

from _load import load_solution

_module = load_solution(__file__)
sort_by_columns = _module.sort_by_columns
rank_scores = _module.rank_scores
top_n = _module.top_n
percent_rank = _module.percent_rank


def _isnan(x):
    return isinstance(x, float) and math.isnan(x)


def _team():
    return pd.DataFrame(
        {
            "dept": ["ops", "dev", "dev", "ops", "dev", "hr", "dev"],
            "salary": [50, 70, 70, 50, 90, np.nan, 60],
            "name": list("ABCDEFG"),
        },
        index=[1, 2, 3, 4, 5, 6, 7],
    )


def _py_ranks(values, method):
    known = sorted((v for v in values if not _isnan(v)), reverse=True)
    out = []
    for v in values:
        if _isnan(v):
            out.append(math.nan)
            continue
        first = known.index(v) + 1
        count = known.count(v)
        if method == "min":
            out.append(float(first))
        elif method == "dense":
            out.append(float(sorted(set(known), reverse=True).index(v) + 1))
        else:
            out.append(first + (count - 1) / 2)
    return out


# ---- 1-5: sort_by_columns ----


def test_1_sorts_by_one_key_ascending():
    out = sort_by_columns(_team(), ["salary"], [True])
    assert out.index.tolist() == [1, 4, 7, 2, 3, 5, 6]


def test_2_sorts_by_one_key_descending_with_nan_still_last():
    out = sort_by_columns(_team(), ["salary"], [False])
    assert out.index.tolist() == [5, 2, 3, 7, 1, 4, 6]


def test_3_two_keys_with_different_directions():
    out = sort_by_columns(_team(), ["dept", "salary"], [True, False])
    assert out["name"].tolist() == ["E", "B", "C", "G", "F", "A", "D"]


def test_4_rows_tied_on_every_key_keep_their_input_order():
    out = sort_by_columns(_team(), ["salary"], [False])
    assert out.index.tolist()[1:3] == [2, 3]  # B and C both 70
    shuffled = _team().iloc[[2, 1, 0, 3, 4, 5, 6]]  # C before B now
    out2 = sort_by_columns(shuffled, ["salary"], [False])
    assert out2.index.tolist()[1:3] == [3, 2]


def test_5_input_is_not_changed_and_labels_travel_with_rows():
    df = _team()
    before = df.copy()
    out = sort_by_columns(df, ["name"], [False])
    pd.testing.assert_frame_equal(df, before)
    assert out.loc[5, "name"] == "E"


# ---- 6-10: rank_scores ----


def test_6_min_ranking_leaves_a_gap():
    s = pd.Series([90, 80, 80, 70])
    assert rank_scores(s, "min").tolist() == [1.0, 2.0, 2.0, 4.0]


def test_7_dense_ranking_has_no_gap():
    s = pd.Series([90, 80, 80, 70])
    assert rank_scores(s, "dense").tolist() == [1.0, 2.0, 2.0, 3.0]


def test_8_average_ranking_shares_the_mean_rank():
    s = pd.Series([90, 80, 80, 70])
    assert rank_scores(s, "average").tolist() == [1.0, 2.5, 2.5, 4.0]


def test_9_missing_stays_missing_and_index_is_kept():
    s = pd.Series([5.0, np.nan, 9.0], index=["a", "b", "c"], name="x")
    out = rank_scores(s, "min")
    assert out.index.tolist() == ["a", "b", "c"]
    assert out["a"] == 2.0 and out["c"] == 1.0
    assert math.isnan(out["b"])
    assert out.dtype.kind == "f"


def test_10_matches_a_plain_python_reference():
    for seed in range(6):
        values = np.random.default_rng(seed).integers(0, 6, size=15).astype(float)
        values[3] = np.nan
        s = pd.Series(values)
        for method in ("min", "dense", "average"):
            got = rank_scores(s, method).tolist()
            want = _py_ranks(values.tolist(), method)
            assert all((_isnan(g) and _isnan(w)) or g == w for g, w in zip(got, want))


# ---- 11-14: top_n ----


def test_11_returns_the_largest_first():
    out = top_n(_team(), "salary", 3)
    assert out.index.tolist() == [5, 2, 3]


def test_12_ties_keep_the_original_order():
    out = top_n(_team(), "salary", 4)
    assert out.index.tolist() == [5, 2, 3, 7]
    out2 = top_n(_team().iloc[::-1], "salary", 3)
    assert out2.index.tolist() == [5, 3, 2]


def test_13_missing_values_are_never_selected_so_fewer_rows_can_return():
    df = pd.DataFrame({"v": [np.nan, 4.0, np.nan]}, index=["a", "b", "c"])
    out = top_n(df, "v", 3)
    assert out.index.tolist() == ["b"]


def test_14_keeps_all_columns_and_labels():
    out = top_n(_team(), "salary", 2)
    assert out.columns.tolist() == ["dept", "salary", "name"]
    assert out["name"].tolist() == ["E", "B"]


# ---- 15-17: percent_rank ----


def test_15_smallest_is_zero_and_largest_is_one():
    out = percent_rank(pd.Series([10, 20, 30, 40]))
    assert out.tolist() == [0.0, 1 / 3, 2 / 3, 1.0]


def test_16_ties_share_the_lowest_rank():
    out = percent_rank(pd.Series([1, 2, 2, 3]))
    assert out.tolist() == [0.0, 1 / 3, 1 / 3, 1.0]


def test_17_missing_stays_missing_and_does_not_count():
    s = pd.Series([4.0, np.nan, 8.0, 6.0], index=list("abcd"))
    out = percent_rank(s)
    assert math.isnan(out["b"])
    assert out["a"] == 0.0 and out["d"] == 0.5 and out["c"] == 1.0
