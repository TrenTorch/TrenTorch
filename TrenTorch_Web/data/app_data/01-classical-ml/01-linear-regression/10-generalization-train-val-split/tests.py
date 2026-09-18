"""
pytest data/app_data/01-classical-ml/01-linear-regression/10-generalization-train-val-split/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}")
train_val_split = _module.train_val_split
generalization_gap = _module.generalization_gap

train_linear_regression = load_solution(
    "01-classical-ml/01-linear-regression/05-training-loop"
).train_linear_regression
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss


def test_train_val_split_sizes_match_val_fraction():
    x = np.arange(100.0).reshape(-1, 1)
    y = np.arange(100.0)
    x_train, y_train, x_val, y_val = train_val_split(x, y, val_fraction=0.2, seed=0)
    assert len(x_val) == 20
    assert len(x_train) == 80


def test_train_val_split_covers_every_row_exactly_once():
    x = np.arange(50.0).reshape(-1, 1)
    y = np.arange(50.0)
    x_train, y_train, x_val, y_val = train_val_split(x, y, val_fraction=0.3, seed=0)
    all_ids = np.concatenate([x_train.flatten(), x_val.flatten()])
    assert set(all_ids.tolist()) == set(x.flatten().tolist())
    assert len(all_ids) == 50


def test_train_val_split_keeps_features_and_targets_paired():
    # target[i] is always exactly x[i] + 1000, so any row that survives
    # shuffling with its pairing intact must still satisfy that relation.
    x = np.arange(30.0).reshape(-1, 1)
    y = x.flatten() + 1000.0
    x_train, y_train, x_val, y_val = train_val_split(x, y, val_fraction=0.3, seed=0)
    assert np.allclose(y_train, x_train.flatten() + 1000.0)
    assert np.allclose(y_val, x_val.flatten() + 1000.0)


def test_train_val_split_is_reproducible_with_same_seed():
    x = np.arange(40.0).reshape(-1, 1)
    y = np.arange(40.0)
    a = train_val_split(x, y, val_fraction=0.25, seed=7)
    b = train_val_split(x, y, val_fraction=0.25, seed=7)
    assert np.array_equal(a[0], b[0])
    assert np.array_equal(a[2], b[2])


def test_generalization_gap_matches_hand_computation():
    assert np.isclose(generalization_gap(train_loss=0.5, val_loss=0.8), 0.3)


def test_generalization_gap_is_negative_when_val_beats_train():
    assert generalization_gap(train_loss=1.0, val_loss=0.5) < 0.0


def test_generalization_gap_end_to_end_on_a_genuinely_overfit_model():
    # A concrete, real demonstration: a small, high-dimensional, very
    # noisy dataset lets a linear model essentially memorize the
    # training set (near-zero train loss) while performing far worse
    # on held-out data, a large positive generalization gap.
    rng = np.random.default_rng(2)
    n, d = 20, 15
    x = rng.normal(size=(n, d))
    y = x[:, 0] * 3.0 + rng.normal(scale=5.0, size=n)

    x_train, y_train, x_val, y_val = train_val_split(x, y, val_fraction=0.4, seed=1)
    weight, bias = train_linear_regression(x_train, y_train, lr=0.05, epochs=2000)

    train_predictions = linear(x_train, weight, bias).flatten()
    val_predictions = linear(x_val, weight, bias).flatten()
    train_loss = mse_loss(train_predictions, y_train)
    val_loss = mse_loss(val_predictions, y_val)

    gap = generalization_gap(train_loss, val_loss)
    assert train_loss < 0.01  # essentially memorized the training set
    assert gap > 10.0  # dramatically worse on unseen data


def test_generalization_gap_does_not_compute_the_difference_backwards():
    # Directly targets a mutant that swaps the subtraction order
    # (train_loss - val_loss instead of val_loss - train_loss): the
    # sign of the gap for a genuinely overfit model must be positive,
    # a swapped mutant would report it as negative.
    result = generalization_gap(train_loss=0.1, val_loss=5.0)
    assert result > 0.0
    assert np.isclose(result, 4.9)
