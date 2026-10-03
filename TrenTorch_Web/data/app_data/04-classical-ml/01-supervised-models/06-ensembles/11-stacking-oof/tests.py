"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

solution = load_solution(__file__)
oof_predictions = solution.oof_predictions
stacking_weights = solution.stacking_weights


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _mean_model(X_train, y_train, X_test):
    return np.full(len(X_test), y_train.mean())


def test_oof_length_matches_rows():
    X = np.arange(6.0).reshape(6, 1)
    y = np.arange(6.0)
    assert oof_predictions(_mean_model, X, y, n_splits=3).shape == (6,)


def test_oof_uses_only_other_blocks_for_each_block():
    X = np.arange(6.0).reshape(6, 1)
    y = np.arange(6.0)
    out = oof_predictions(_mean_model, X, y, n_splits=3)
    assert np.allclose(out[:2], np.mean([2, 3, 4, 5]))
    assert np.allclose(out[2:4], np.mean([0, 1, 4, 5]))
    assert np.allclose(out[4:], np.mean([0, 1, 2, 3]))


def test_oof_never_uses_the_block_being_predicted():
    X = np.arange(6.0).reshape(6, 1)
    y = np.arange(6.0)
    seen = []

    def spy(X_train, y_train, X_test):
        seen.append((set(X_test[:, 0].tolist()), set(X_train[:, 0].tolist())))
        return np.zeros(len(X_test))

    oof_predictions(spy, X, y, n_splits=3)
    for test_set, train_set in seen:
        assert test_set.isdisjoint(train_set)


def test_oof_with_two_splits_covers_every_row():
    X = np.arange(4.0).reshape(4, 1)
    y = np.arange(4.0)
    out = oof_predictions(lambda a, b, c: np.ones(len(c)), X, y, n_splits=2)
    assert np.all(out == 1.0)


def test_n_splits_out_of_range_raises():
    X = np.arange(6.0).reshape(6, 1)
    y = np.arange(6.0)
    assert _raises_value_error(oof_predictions, _mean_model, X, y, 1)
    assert _raises_value_error(oof_predictions, _mean_model, X, y, 7)


def test_weights_pick_the_column_equal_to_the_target():
    rng = np.random.default_rng(0)
    y = rng.normal(size=20)
    P = np.column_stack([y, rng.normal(size=20)])
    w = stacking_weights(P, y)
    assert np.allclose(w, [1.0, 0.0], atol=1e-8)


def test_weights_have_one_entry_per_model():
    rng = np.random.default_rng(1)
    P = rng.normal(size=(15, 4))
    y = rng.normal(size=15)
    assert stacking_weights(P, y).shape == (4,)


def test_weights_recover_a_known_combination():
    rng = np.random.default_rng(2)
    P = rng.normal(size=(30, 2))
    y = 0.7 * P[:, 0] + 0.2 * P[:, 1]
    assert np.allclose(stacking_weights(P, y), [0.7, 0.2], atol=1e-8)


def test_mismatched_rows_raise():
    assert _raises_value_error(stacking_weights, np.ones((4, 2)), np.ones(5))


def test_same_input_gives_same_weights():
    rng = np.random.default_rng(3)
    P = rng.normal(size=(10, 3))
    y = rng.normal(size=10)
    assert np.array_equal(stacking_weights(P, y), stacking_weights(P, y))


def test_does_not_modify_inputs():
    rng = np.random.default_rng(4)
    P = rng.normal(size=(10, 2))
    y = rng.normal(size=10)
    P0, y0 = P.copy(), y.copy()
    stacking_weights(P, y)
    assert np.array_equal(P, P0) and np.array_equal(y, y0)
