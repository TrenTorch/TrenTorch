"""
pytest tests.py
"""

import math
import statistics

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
group_summary = _module.group_summary
add_group_mean = _module.add_group_mean
zscore_within_group = _module.zscore_within_group
top_n_per_group = _module.top_n_per_group


def _isnan(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def _staff():
    return pd.DataFrame(
        {
            "dept": ["ops", "dev", "dev", "ops", "dev", "hr", None, "ops"],
            "salary": [50.0, 70.0, 90.0, 60.0, 80.0, np.nan, 99.0, 55.0],
            "name": list("ABCDEFGH"),
        },
        index=list("pqrstuvw"),
    )


def _groups(df, key, value):
    out = {}
    for k, v in zip(df[key], df[value]):
        if _isnan(k):
            continue
        out.setdefault(k, []).append(v)
    return out


# ---- 1-5: group_summary ----


def test_1_one_row_per_key_sorted_ascending():
    out = group_summary(_staff(), "dept", "salary")
    assert out.index.tolist() == ["dev", "hr", "ops"]


def test_2_columns_in_order_and_n_counts_known_values():
    out = group_summary(_staff(), "dept", "salary")
    assert out.columns.tolist() == ["n", "mean", "median", "max"]
    assert out["n"].tolist() == [3, 0, 3]


def test_3_statistics_match_a_python_reference():
    out = group_summary(_staff(), "dept", "salary")
    assert out.loc["dev", "mean"] == pytest.approx(80.0)
    assert out.loc["dev", "median"] == 80.0
    assert out.loc["ops", "max"] == 60.0
    assert out.loc["ops", "mean"] == pytest.approx(55.0)


def test_4_a_group_of_only_missing_values_is_kept_with_nan_statistics():
    out = group_summary(_staff(), "dept", "salary")
    assert out.loc["hr", "n"] == 0
    assert math.isnan(out.loc["hr", "mean"]) and math.isnan(out.loc["hr", "max"])


def test_5_rows_with_a_missing_key_are_in_no_group():
    out = group_summary(_staff(), "dept", "salary")
    assert out["n"].sum() == 6  # 8 rows - 1 missing key - 1 missing salary
    random_df = pd.DataFrame({"k": ["a", "b", "a", None, "b", "a"], "v": [1.0, 2.0, 3.0, 4.0, 5.0, np.nan]})
    got = group_summary(random_df, "k", "v")
    ref = _groups(random_df, "k", "v")
    for k, vals in ref.items():
        known = [v for v in vals if not _isnan(v)]
        assert got.loc[k, "mean"] == pytest.approx(statistics.mean(known))
        assert got.loc[k, "n"] == len(known)


# ---- 6-8: add_group_mean ----


def test_6_adds_the_group_mean_to_every_member():
    out = add_group_mean(_staff(), "dept", "salary")
    assert out["salary_group_mean"].tolist()[0] == pytest.approx(55.0)
    assert out.loc["q", "salary_group_mean"] == pytest.approx(80.0)


def test_7_keeps_every_row_and_adds_only_one_column():
    df = _staff()
    out = add_group_mean(df, "dept", "salary")
    assert out.index.tolist() == df.index.tolist()
    assert out.columns.tolist() == df.columns.tolist() + ["salary_group_mean"]


def test_8_missing_key_gets_nan_and_the_input_is_not_changed():
    df = _staff()
    before = df.copy()
    out = add_group_mean(df, "dept", "salary")
    assert math.isnan(out.loc["v", "salary_group_mean"])
    pd.testing.assert_frame_equal(df, before)


# ---- 9-12: zscore_within_group ----


def test_9_zscores_of_a_known_group():
    out = zscore_within_group(_staff(), "dept", "salary")
    ops = [50.0, 60.0, 55.0]
    expected = [(x - statistics.mean(ops)) / statistics.stdev(ops) for x in ops]
    assert out["p"] == pytest.approx(expected[0])
    assert out["s"] == pytest.approx(expected[1])
    assert out["w"] == pytest.approx(expected[2])


def test_10_group_of_one_missing_value_or_missing_key_is_nan():
    out = zscore_within_group(_staff(), "dept", "salary")
    assert math.isnan(out["u"])  # hr, salary missing
    assert math.isnan(out["v"])  # key missing
    single = pd.DataFrame({"k": ["a", "b", "b"], "v": [1.0, 2.0, 4.0]})
    assert math.isnan(zscore_within_group(single, "k", "v").iloc[0])


def test_11_zero_spread_is_nan_not_inf():
    df = pd.DataFrame({"k": ["a", "a", "a"], "v": [5.0, 5.0, 5.0]})
    assert zscore_within_group(df, "k", "v").isna().all()


def test_12_keeps_the_index_and_group_zscores_have_mean_zero():
    df = pd.DataFrame({"k": ["a"] * 5 + ["b"] * 5, "v": np.random.default_rng(0).normal(size=10)}, index=list("abcdefghij"))
    out = zscore_within_group(df, "k", "v")
    assert out.index.tolist() == df.index.tolist()
    assert out.groupby(df["k"]).mean().abs().max() < 1e-12


# ---- 13-17: top_n_per_group ----


def test_13_picks_the_largest_in_each_group():
    out = top_n_per_group(_staff(), "dept", "salary", 2)
    assert out["name"].tolist() == ["C", "E", "D", "H"]


def test_14_ordered_by_key_then_value_descending():
    out = top_n_per_group(_staff(), "dept", "salary", 5)
    assert out["dept"].tolist() == ["dev", "dev", "dev", "ops", "ops", "ops"]
    assert out["salary"].tolist() == [90.0, 80.0, 70.0, 60.0, 55.0, 50.0]


def test_15_keeps_all_columns_and_original_labels():
    out = top_n_per_group(_staff(), "dept", "salary", 1)
    assert out.columns.tolist() == ["dept", "salary", "name"]
    assert out.index.tolist() == ["r", "s"]


def test_16_ties_keep_the_original_order():
    df = pd.DataFrame({"k": ["a", "a", "a"], "v": [7.0, 7.0, 7.0], "id": [1, 2, 3]})
    assert top_n_per_group(df, "k", "v", 2)["id"].tolist() == [1, 2]


def test_17_matches_a_python_reference_on_random_data():
    rng = np.random.default_rng(7)
    df = pd.DataFrame({"k": rng.choice(list("abc"), size=30), "v": rng.integers(0, 10, size=30).astype(float)})
    out = top_n_per_group(df, "k", "v", 3)
    for key in "abc":
        rows = sorted(((v, -i) for i, (k, v) in enumerate(zip(df["k"], df["v"])) if k == key), reverse=True)[:3]
        assert sorted(out.loc[out["k"] == key, "v"].tolist(), reverse=True) == [v for v, _ in rows]
        assert len(out[out["k"] == key]) == len(rows)
