"""
pytest data/app_data/01-classical-ml/04-ensembles/06-adaboost/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
adaboost_train = _module.adaboost_train
adaboost_predict = _module.adaboost_predict


def test_ensemble_has_one_entry_per_round():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(40, 2))
    labels = np.where(input[:, 0] > 0, 1, -1)
    ensemble = adaboost_train(input, labels, n_rounds=7, max_depth=1, seed=0)
    assert len(ensemble) == 7


def test_predictions_are_only_plus_or_minus_one():
    rng = np.random.default_rng(1)
    input = rng.normal(size=(40, 2))
    labels = np.where(input[:, 0] > 0, 1, -1)
    ensemble = adaboost_train(input, labels, n_rounds=5, max_depth=1, seed=0)
    predictions = adaboost_predict(ensemble, input)
    assert set(np.unique(predictions).tolist()).issubset({-1, 1})


def test_reproducible_with_the_same_seed():
    rng = np.random.default_rng(2)
    input = rng.normal(size=(50, 2))
    labels = np.where(input[:, 0] + input[:, 1] > 0, 1, -1)
    ensemble_a = adaboost_train(input, labels, n_rounds=10, max_depth=1, seed=7)
    ensemble_b = adaboost_train(input, labels, n_rounds=10, max_depth=1, seed=7)
    alphas_a = [alpha for _, alpha in ensemble_a]
    alphas_b = [alpha for _, alpha in ensemble_b]
    assert np.allclose(alphas_a, alphas_b)


def test_a_good_weak_learner_gets_a_positive_alpha():
    # On easily-separable data, the very first round's stump should
    # already be much better than chance -- its alpha must be positive
    # and sizeable, not near zero or negative.
    rng = np.random.default_rng(3)
    input = rng.normal(size=(100, 2))
    labels = np.where(input[:, 0] > 0, 1, -1)
    ensemble = adaboost_train(input, labels, n_rounds=1, max_depth=1, seed=0)
    _, alpha = ensemble[0]
    assert alpha > 1.0


def test_single_stump_cannot_solve_a_quadrant_pattern_but_boosting_helps():
    # A depth-1 stump can only split on one feature -- it cannot fully
    # separate the "top-right quadrant only" pattern
    # (03-best-split-minimal-tree's Theory names the same shape of
    # limitation). More boosting rounds, reweighting the samples each
    # stump gets wrong, should measurably close that gap.
    input = np.array([[1.0, 1.0], [1.0, -1.0], [-1.0, 1.0], [-1.0, -1.0]] * 15)
    labels = np.where((input[:, 0] > 0) & (input[:, 1] > 0), 1, -1)

    one_round = adaboost_train(input, labels, n_rounds=1, max_depth=1, seed=0)
    many_rounds = adaboost_train(input, labels, n_rounds=15, max_depth=1, seed=0)

    acc_one = np.mean(adaboost_predict(one_round, input) == labels)
    acc_many = np.mean(adaboost_predict(many_rounds, input) == labels)
    assert acc_many > acc_one
