"""
pytest data/app_data/01-classical-ml/07-evaluation/13-model-selection-class-imbalance/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
balanced_accuracy = _module.balanced_accuracy
stratified_k_fold_split = _module.stratified_k_fold_split


def test_balanced_accuracy_matches_hand_computation():
    # class 0: 3 samples, 2 correct -> recall 2/3
    # class 1: 2 samples, 1 correct -> recall 1/2
    # balanced accuracy = mean(2/3, 1/2) = 7/12
    labels = np.array([0, 0, 0, 1, 1])
    predictions = np.array([0, 0, 1, 1, 0])
    result = balanced_accuracy(labels, predictions)
    assert np.isclose(result, 7.0 / 12.0)


def test_balanced_accuracy_of_perfect_predictions_is_one():
    labels = np.array([0, 1, 1, 0, 1])
    assert balanced_accuracy(labels, labels.copy()) == 1.0


def test_balanced_accuracy_exposes_majority_class_bias_where_plain_accuracy_hides_it():
    # 90 negatives, 10 positives, a model that predicts negative for
    # everything: plain accuracy is a misleadingly high 90%, but
    # balanced accuracy must reveal the total failure on the minority
    # class.
    labels = np.concatenate([np.zeros(90, dtype=int), np.ones(10, dtype=int)])
    predictions = np.zeros(100, dtype=int)  # always predicts the majority class
    plain_accuracy = np.mean(labels == predictions)
    result = balanced_accuracy(labels, predictions)
    assert plain_accuracy > 0.85
    assert np.isclose(result, 0.5)  # recall 1.0 on class 0, 0.0 on class 1, mean 0.5


def test_stratified_k_fold_preserves_class_ratio_in_every_fold():
    labels = np.concatenate([np.zeros(90, dtype=int), np.ones(10, dtype=int)])
    splits = stratified_k_fold_split(labels, k=5, seed=0)
    for _, val_idx in splits:
        assert np.isclose(labels[val_idx].mean(), 0.1, atol=1e-9)


def test_stratified_k_fold_partitions_every_sample_exactly_once():
    labels = np.concatenate([np.zeros(37, dtype=int), np.ones(13, dtype=int)])
    splits = stratified_k_fold_split(labels, k=5, seed=0)
    all_val = np.concatenate([val_idx for _, val_idx in splits])
    assert sorted(all_val.tolist()) == list(range(50))
    assert len(all_val) == len(set(all_val.tolist()))


def test_stratified_k_fold_train_and_val_never_overlap():
    labels = np.concatenate([np.zeros(40, dtype=int), np.ones(20, dtype=int)])
    splits = stratified_k_fold_split(labels, k=4, seed=1)
    for train_idx, val_idx in splits:
        assert set(train_idx.tolist()).isdisjoint(set(val_idx.tolist()))


def test_balanced_accuracy_weights_classes_equally_not_by_sample_count():
    # Directly targets a mutant that computes plain (per-sample)
    # accuracy instead of macro-averaged per-class recall: with 90
    # negatives (all correct) and 10 positives (all wrong), plain
    # accuracy is 0.9, balanced accuracy must be 0.5.
    labels = np.concatenate([np.zeros(90, dtype=int), np.ones(10, dtype=int)])
    predictions = np.concatenate([np.zeros(90, dtype=int), np.zeros(10, dtype=int)])
    result = balanced_accuracy(labels, predictions)
    assert np.isclose(result, 0.5)
    assert not np.isclose(result, 0.9)


def test_stratification_is_not_dropped_every_fold_matches_the_overall_ratio_every_seed():
    # Directly targets a mutant that shuffles ALL indices together
    # (like plain k_fold_split) instead of shuffling WITHIN each class:
    # a plain shuffle-then-slice would only match the overall ratio in
    # every fold by luck, stratification must match it EXACTLY, every
    # single seed, by construction.
    labels = np.concatenate([np.zeros(50, dtype=int), np.ones(10, dtype=int)])
    for seed in range(10):
        splits = stratified_k_fold_split(labels, k=5, seed=seed)
        val_ratios = [labels[val_idx].mean() for _, val_idx in splits]
        assert all(np.isclose(r, 1.0 / 6.0, atol=1e-9) for r in val_ratios)
