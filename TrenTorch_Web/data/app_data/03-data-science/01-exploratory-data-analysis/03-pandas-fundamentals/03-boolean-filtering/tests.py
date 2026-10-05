"""
pytest tests.py
"""

import numpy as np
import pandas as pd

from _load import load_solution

_module = load_solution(__file__)
in_range = _module.in_range
from_cities_and_old_enough = _module.from_cities_and_old_enough
any_extreme = _module.any_extreme
exclude_values = _module.exclude_values
complete_rows = _module.complete_rows


def _people():
    return pd.DataFrame(
        {
            "name": ["Asha", "Ben", "Chen", "Dia", "Eli", "Fay", "Gus"],
            "city": ["Pune", "Delhi", "Pune", "Goa", "Delhi", "Pune", None],
            "age": [25, 41, 30, np.nan, 52, 19, 33],
            "score": [7.5, 3.0, np.nan, 9.0, 6.0, 1.5, 5.0],
        },
        index=[100, 101, 102, 103, 104, 105, 106],
    )


# ---- 1-4: in_range ----


def test_1_in_range_is_inclusive_at_both_ends():
    out = in_range(_people(), "age", 25, 41)
    assert out.index.tolist() == [100, 101, 102, 106]


def test_2_in_range_drops_missing_values():
    out = in_range(_people(), "score", 0, 100)
    assert 102 not in out.index


def test_3_in_range_keeps_original_labels_and_columns():
    df = _people()
    out = in_range(df, "age", 30, 60)
    assert out.columns.tolist() == df.columns.tolist()
    assert out.index.tolist() == [101, 102, 104, 106]


def test_4_in_range_can_select_nothing():
    assert in_range(_people(), "age", 200, 300).empty


# ---- 5-8: from_cities_and_old_enough ----


def test_5_both_conditions_must_hold():
    out = from_cities_and_old_enough(_people(), ["Pune", "Delhi"], 30)
    assert out.index.tolist() == [101, 102, 104]


def test_6_a_missing_age_never_passes():
    out = from_cities_and_old_enough(_people(), ["Goa"], 0)
    assert out.empty


def test_7_a_missing_city_never_matches():
    out = from_cities_and_old_enough(_people(), ["Pune", "Delhi", "Goa"], 0)
    assert 106 not in out.index


def test_8_accepts_any_iterable_of_cities_and_does_not_change_the_frame():
    df = _people()
    before = df.copy()
    out = from_cities_and_old_enough(df, ("Pune",), 20)
    assert out.index.tolist() == [100, 102]
    pd.testing.assert_frame_equal(df, before)


# ---- 9-11: any_extreme ----


def test_9_either_side_counts():
    out = any_extreme(_people(), "score", 2.0, 8.0)
    assert out.index.tolist() == [103, 105]


def test_10_the_boundaries_are_not_extreme():
    out = any_extreme(_people(), "age", 19, 52)
    assert out.empty


def test_11_missing_is_not_extreme():
    out = any_extreme(_people(), "age", 30, 40)
    assert 103 not in out.index
    assert out.index.tolist() == [100, 101, 104, 105]


# ---- 12-14: exclude_values ----


def test_12_removes_the_listed_values():
    out = exclude_values(_people(), "city", ["Pune"])
    assert out.index.tolist() == [101, 103, 104, 106]


def test_13_a_missing_value_is_kept_because_it_is_not_in_the_list():
    out = exclude_values(_people(), "city", ["Pune", "Delhi", "Goa"])
    assert out.index.tolist() == [106]


def test_14_empty_list_keeps_every_row():
    out = exclude_values(_people(), "city", [])
    assert out.index.tolist() == _people().index.tolist()


# ---- 15-17: complete_rows ----


def test_15_requires_every_listed_column():
    out = complete_rows(_people(), ["age", "score"])
    assert out.index.tolist() == [100, 101, 104, 105, 106]


def test_16_ignores_missing_values_in_unlisted_columns():
    out = complete_rows(_people(), ["name", "score"])
    assert out.index.tolist() == [100, 101, 103, 104, 105, 106]


def test_17_matches_a_plain_python_reference():
    df = _people()
    cols = ["city", "age"]
    expected = [
        label
        for label, row in df.iterrows()
        if all(not (v is None or (isinstance(v, float) and np.isnan(v))) for v in (row[c] for c in cols))
    ]
    assert complete_rows(df, cols).index.tolist() == expected
