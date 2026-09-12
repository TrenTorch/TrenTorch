"""
pytest data/app_data/01-classical-ml/04-ensembles/05-random-forest-regression-oob/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
bootstrap_sample_with_oob = _module.bootstrap_sample_with_oob
train_random_forest_regressor = _module.train_random_forest_regressor
predict_random_forest_regressor = _module.predict_random_forest_regressor
oob_error = _module.oob_error


def _leaf(prediction: float) -> dict:
    return {"leaf": True, "prediction": prediction}


def test_in_bag_and_out_of_bag_partition_every_index_exactly_once():
    input = np.arange(20.0).reshape(20, 1)
    targets = np.arange(20.0)
    boot_input, boot_targets, oob_indices = bootstrap_sample_with_oob(input, targets, seed=0)
    assert boot_input.shape == input.shape
    in_bag = np.setdiff1d(np.arange(20), oob_indices)
    # every drawn index must be one of the ones NOT in oob_indices
    assert set(boot_input[:, 0].astype(int)).issubset(set(in_bag))
    assert len(set(oob_indices.tolist()) & set(in_bag.tolist())) == 0


def test_bootstrap_sample_with_oob_is_reproducible():
    input = np.arange(10.0).reshape(10, 1)
    targets = np.arange(10.0)
    _, _, oob1 = bootstrap_sample_with_oob(input, targets, seed=3)
    _, _, oob2 = bootstrap_sample_with_oob(input, targets, seed=3)
    assert np.array_equal(oob1, oob2)


def test_predict_random_forest_regressor_averages_not_votes():
    forest = [(_leaf(2.0), np.array([])), (_leaf(4.0), np.array([])), (_leaf(9.0), np.array([]))]
    input = np.array([[0.0], [0.0]])
    predictions = predict_random_forest_regressor(forest, input)
    assert np.allclose(predictions, 5.0)  # mean of 2, 4, 9


def test_oob_error_matches_hand_computation():
    forest = [
        (_leaf(2.0), np.array([0, 2])),
        (_leaf(4.0), np.array([1, 2])),
    ]
    input = np.zeros((3, 1))
    targets = np.array([3.0, 5.0, 10.0])
    # sample 0: OOB for tree A only -> pred 2.0, err (2-3)^2=1
    # sample 1: OOB for tree B only -> pred 4.0, err (4-5)^2=1
    # sample 2: OOB for both -> pred mean(2,4)=3.0, err (3-10)^2=49
    # mean = (1+1+49)/3 = 17.0
    assert np.isclose(oob_error(forest, input, targets), 17.0)


def test_samples_never_out_of_bag_are_excluded_not_treated_as_zero_error():
    # sample 1 is in-bag for the only tree, so it has no OOB prediction
    # at all -- it must be excluded from the average, not silently
    # scored as a perfect (zero-error) prediction.
    forest = [(_leaf(0.0), np.array([0]))]
    input = np.zeros((2, 1))
    targets = np.array([0.0, 1000.0])
    assert np.isclose(oob_error(forest, input, targets), 0.0)  # only sample 0 contributes


def test_oob_error_is_closer_to_true_test_error_than_in_bag_training_error():
    # Directly targets a plausible bug: evaluating every tree on every
    # sample (in-bag included) instead of only each sample's true OOB
    # trees. In-bag evaluation is optimistic (trees have partially
    # memorized their own bag), so real OOB error should sit much
    # closer to error on genuinely unseen test data than in-bag error does.
    rng = np.random.default_rng(5)
    input_train = rng.normal(size=(150, 2))
    targets_train = input_train[:, 0] ** 2 + rng.normal(scale=0.3, size=150)
    forest = train_random_forest_regressor(
        input_train, targets_train, n_trees=25, max_depth=8, seed=1
    )

    input_test = rng.normal(size=(150, 2))
    targets_test = input_test[:, 0] ** 2 + rng.normal(scale=0.3, size=150)
    test_predictions = predict_random_forest_regressor(forest, input_test)
    true_test_error = np.mean((test_predictions - targets_test) ** 2)

    in_bag_predictions = predict_random_forest_regressor(forest, input_train)
    in_bag_error = np.mean((in_bag_predictions - targets_train) ** 2)

    estimated_oob_error = oob_error(forest, input_train, targets_train)

    assert abs(estimated_oob_error - true_test_error) < abs(in_bag_error - true_test_error)
