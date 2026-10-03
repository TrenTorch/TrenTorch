"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
class_weights = _module.class_weights
random_oversample = _module.random_oversample
random_undersample = _module.random_undersample
interpolate_minority = _module.interpolate_minority


def _imbalanced():
    X = np.arange(20.0).reshape(10, 2)
    y = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 2])  # counts 7, 2, 1
    return X, y


# ---- 1-4: class weights ----


def test_1_weights_match_a_hand_computed_case():
    weights = class_weights(np.array([0, 0, 0, 1]))
    assert np.isclose(weights[0], 4 / (2 * 3)) and np.isclose(weights[1], 4 / (2 * 1))


def test_2_every_class_carries_equal_total_weight():
    y = _imbalanced()[1]
    weights = class_weights(y)
    totals = [weights[label] * np.sum(y == label) for label in weights]
    assert np.allclose(totals, totals[0])
    assert np.isclose(totals[0], len(y) / 3)


def test_3_balanced_data_gets_weight_one():
    weights = class_weights(np.array([0, 1, 2, 0, 1, 2]))
    assert all(np.isclose(w, 1.0) for w in weights.values())


def test_4_works_with_string_labels():
    weights = class_weights(np.array(["no", "no", "no", "yes"]))
    assert set(weights) == {"no", "yes"} and weights["yes"] > weights["no"]


# ---- 5-10: oversampling ----


def test_5_every_class_reaches_the_majority_count():
    X, y = _imbalanced()
    _, y_new = random_oversample(X, y, np.random.default_rng(0))
    assert [int(np.sum(y_new == c)) for c in (0, 1, 2)] == [7, 7, 7]


def test_6_original_rows_come_first_unchanged():
    X, y = _imbalanced()
    X_new, y_new = random_oversample(X, y, np.random.default_rng(1))
    np.testing.assert_array_equal(X_new[:10], X)
    np.testing.assert_array_equal(y_new[:10], y)


def test_7_added_rows_are_copies_of_rows_of_the_right_class():
    X, y = _imbalanced()
    X_new, y_new = random_oversample(X, y, np.random.default_rng(2))
    for row, label in zip(X_new[10:], y_new[10:]):
        matches = np.all(X == row, axis=1)
        assert matches.any() and y[matches][0] == label


def test_8_matches_an_independent_replay_of_the_draws():
    X, y = _imbalanced()
    rng = np.random.default_rng(3)
    expected = [np.arange(10)]
    for label in (1, 2):
        rows = np.flatnonzero(y == label)
        expected.append(rng.choice(rows, size=7 - len(rows), replace=True))
    picked = np.concatenate(expected)
    X_new, y_new = random_oversample(X, y, np.random.default_rng(3))
    np.testing.assert_array_equal(X_new, X[picked])
    np.testing.assert_array_equal(y_new, y[picked])


def test_9_balanced_input_is_returned_unchanged():
    X = np.arange(8.0).reshape(4, 2)
    y = np.array([0, 0, 1, 1])
    X_new, y_new = random_oversample(X, y, np.random.default_rng(4))
    np.testing.assert_array_equal(X_new, X)
    np.testing.assert_array_equal(y_new, y)


def test_10_inputs_are_not_modified_by_oversampling():
    X, y = _imbalanced()
    X0, y0 = X.copy(), y.copy()
    random_oversample(X, y, np.random.default_rng(5))
    np.testing.assert_array_equal(X, X0)
    np.testing.assert_array_equal(y, y0)


# ---- 11-15: undersampling ----


def test_11_every_class_is_cut_to_the_smallest_count():
    X, y = _imbalanced()
    _, y_new = random_undersample(X, y, np.random.default_rng(0))
    assert [int(np.sum(y_new == c)) for c in (0, 1, 2)] == [1, 1, 1]


def test_12_kept_rows_are_real_rows_with_matching_labels():
    X, y = _imbalanced()
    X_new, y_new = random_undersample(X, y, np.random.default_rng(1))
    for row, label in zip(X_new, y_new):
        matches = np.all(X == row, axis=1)
        assert matches.sum() == 1 and y[matches][0] == label


def test_13_rows_are_not_repeated():
    X = np.arange(40.0).reshape(20, 2)
    y = np.array([0] * 15 + [1] * 5)
    X_new, _ = random_undersample(X, y, np.random.default_rng(2))
    assert len({tuple(r) for r in X_new}) == len(X_new) == 10


def test_14_classes_appear_in_sorted_order_with_sorted_indices():
    X = np.arange(30.0).reshape(15, 2)
    y = np.array([1] * 8 + [0] * 4 + [2] * 3)
    X_new, y_new = random_undersample(X, y, np.random.default_rng(3))
    np.testing.assert_array_equal(y_new, [0, 0, 0, 1, 1, 1, 2, 2, 2])
    for label in (0, 1, 2):
        block = X_new[y_new == label][:, 0]
        assert np.all(np.diff(block) > 0)


def test_15_matches_an_independent_replay_of_the_draws():
    X, y = _imbalanced()
    rng = np.random.default_rng(4)
    kept = [np.sort(rng.choice(np.flatnonzero(y == label), size=1, replace=False)) for label in (0, 1, 2)]
    picked = np.concatenate(kept)
    X_new, y_new = random_undersample(X, y, np.random.default_rng(4))
    np.testing.assert_array_equal(X_new, X[picked])
    np.testing.assert_array_equal(y_new, y[picked])


# ---- 16-20: interpolation ----


def test_16_output_shape():
    points = np.random.default_rng(0).normal(size=(6, 3))
    assert interpolate_minority(points, 10, np.random.default_rng(1)).shape == (10, 3)


def test_17_new_points_lie_on_a_segment_between_two_real_points():
    minority = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]])
    new = interpolate_minority(minority, 50, np.random.default_rng(2))
    assert np.all(new >= -1e-12) and np.all(new.sum(axis=1) <= 10.0 + 1e-9)


def test_18_two_points_give_points_on_their_line():
    minority = np.array([[0.0, 0.0], [4.0, 8.0]])
    new = interpolate_minority(minority, 20, np.random.default_rng(3))
    np.testing.assert_allclose(new[:, 1], 2.0 * new[:, 0], atol=1e-12)
    assert np.all((new[:, 0] >= 0.0) & (new[:, 0] <= 4.0))


def test_19_matches_an_independent_replay_of_the_draws():
    minority = np.random.default_rng(5).normal(size=(5, 2))
    rng = np.random.default_rng(6)
    expected = []
    for _ in range(4):
        i, j = rng.choice(5, size=2, replace=False)
        u = rng.random()
        expected.append(minority[i] + u * (minority[j] - minority[i]))
    got = interpolate_minority(minority, 4, np.random.default_rng(6))
    np.testing.assert_allclose(got, expected)


def test_20_input_is_not_modified_and_zero_new_points_is_empty():
    minority = np.random.default_rng(7).normal(size=(4, 2))
    original = minority.copy()
    out = interpolate_minority(minority, 0, np.random.default_rng(8))
    assert out.shape == (0, 2)
    np.testing.assert_array_equal(minority, original)
