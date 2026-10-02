"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
ordinal_encode = _module.ordinal_encode
target_encode = _module.target_encode
apply_target_encoding = _module.apply_target_encoding
out_of_fold_target_encode = _module.out_of_fold_target_encode


# ---- 1-4: ordinal encoding ----


def test_1_ranks_follow_the_supplied_order():
    result = ordinal_encode(np.array(["M", "S", "XL", "L", "S"]), ["S", "M", "L", "XL"])
    np.testing.assert_array_equal(result, [1, 0, 3, 2, 0])


def test_2_unknown_labels_become_minus_one():
    result = ordinal_encode(np.array(["low", "weird", "high"]), ["low", "high"])
    np.testing.assert_array_equal(result, [0, -1, 1])


def test_3_order_is_respected_not_alphabetical():
    result = ordinal_encode(np.array(["b", "a"]), ["b", "a"])
    np.testing.assert_array_equal(result, [0, 1])


def test_4_returns_an_integer_array():
    assert ordinal_encode(np.array(["a"]), ["a"]).dtype.kind == "i"


# ---- 5-9: target encoding ----


def test_5_zero_smoothing_gives_plain_category_means():
    cats = np.array(["a", "a", "b", "b", "b"])
    y = np.array([1.0, 3.0, 2.0, 4.0, 6.0])
    mapping = target_encode(cats, y, smoothing=0.0)
    assert np.isclose(mapping["a"], 2.0) and np.isclose(mapping["b"], 4.0)


def test_6_smoothing_matches_a_hand_computed_case():
    cats = np.array(["a", "a", "b"])
    y = np.array([1.0, 1.0, 0.0])  # global mean 2/3
    mapping = target_encode(cats, y, smoothing=2.0)
    assert np.isclose(mapping["a"], (2 * 1.0 + 2 * (2 / 3)) / 4)
    assert np.isclose(mapping["b"], (1 * 0.0 + 2 * (2 / 3)) / 3)


def test_7_rare_categories_are_pulled_toward_the_global_mean():
    cats = np.array(["rare"] + ["common"] * 99)
    y = np.array([1.0] + [0.0] * 99)
    raw = target_encode(cats, y, smoothing=0.0)["rare"]
    smooth = target_encode(cats, y, smoothing=10.0)["rare"]
    assert raw == 1.0
    assert abs(smooth - y.mean()) < abs(raw - y.mean())


def test_8_large_categories_barely_move_with_smoothing():
    cats = np.array(["a"] * 1000 + ["b"] * 1000)
    y = np.array([1.0] * 1000 + [0.0] * 1000)
    mapping = target_encode(cats, y, smoothing=1.0)
    assert abs(mapping["a"] - 1.0) < 0.01


def test_9_every_category_gets_a_float_key():
    mapping = target_encode(np.array([1, 2, 2, 3]), np.array([0.0, 1.0, 1.0, 0.0]), 1.0)
    assert set(mapping) == {1, 2, 3}
    assert all(isinstance(v, float) for v in mapping.values())


# ---- 10-12: applying a mapping ----


def test_10_apply_looks_up_each_category():
    result = apply_target_encoding(np.array(["a", "b", "a"]), {"a": 0.2, "b": 0.7}, 0.5)
    np.testing.assert_allclose(result, [0.2, 0.7, 0.2])


def test_11_unseen_category_gets_the_default():
    result = apply_target_encoding(np.array(["a", "zzz"]), {"a": 0.2}, 0.5)
    np.testing.assert_allclose(result, [0.2, 0.5])


def test_12_apply_returns_a_float_array():
    assert apply_target_encoding(np.array(["a"]), {"a": 1}, 0.0).dtype.kind == "f"


# ---- 13-17: out-of-fold encoding ----


def test_13_a_rows_own_label_never_changes_its_own_encoding():
    cats = np.array(["a"] * 6 + ["b"] * 6)
    y = np.array([0.0, 1.0] * 6)
    base = out_of_fold_target_encode(cats, y, n_folds=3)
    flipped = y.copy()
    flipped[4] = 1.0 - flipped[4]
    changed = out_of_fold_target_encode(cats, flipped, n_folds=3)
    assert base[4] == changed[4]


def test_14_matches_an_independent_manual_computation():
    cats = np.array(["a", "b", "a", "b", "a", "b"])
    y = np.array([1.0, 0.0, 1.0, 1.0, 0.0, 0.0])
    got = out_of_fold_target_encode(cats, y, n_folds=3, smoothing=1.0)
    blocks = np.array_split(np.arange(6), 3)
    for block in blocks:
        rest = np.setdiff1d(np.arange(6), block)
        gm = y[rest].mean()
        for i in block:
            same = rest[cats[rest] == cats[i]]
            expected = (len(same) * y[same].mean() + gm) / (len(same) + 1) if len(same) else gm
            assert np.isclose(got[i], expected)


def test_15_unseen_category_in_a_fold_falls_back_to_the_other_rows_mean():
    cats = np.array(["a", "a", "a", "a", "z", "a"])
    y = np.array([1.0, 1.0, 1.0, 1.0, 0.0, 1.0])
    got = out_of_fold_target_encode(cats, y, n_folds=2)
    # the block holding the only "z" has no "z" in its training rows
    assert np.isclose(got[4], y[np.arange(6) < 3].mean())


def test_16_output_has_one_value_per_row():
    cats = np.array(list("abcabcabca"))
    y = np.arange(10.0)
    assert out_of_fold_target_encode(cats, y, n_folds=4).shape == (10,)


def test_17_inputs_are_not_modified():
    cats = np.array(["a", "b", "a", "b"])
    y = np.array([1.0, 0.0, 1.0, 0.0])
    c0, y0 = cats.copy(), y.copy()
    out_of_fold_target_encode(cats, y, 2, 1.0)
    np.testing.assert_array_equal(cats, c0)
    np.testing.assert_array_equal(y, y0)
