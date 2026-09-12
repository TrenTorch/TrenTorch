"""
pytest data/app_data/01-classical-ml/07-evaluation/01-splitting-and-resampling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
train_test_split = _module.train_test_split
k_fold_split = _module.k_fold_split


def test_train_test_split_respects_test_size():
    input = np.arange(100).reshape(100, 1).astype(float)
    labels = np.arange(100)
    train_input, test_input, _, _ = train_test_split(input, labels, test_size=0.2, seed=0)
    assert test_input.shape[0] == 20
    assert train_input.shape[0] == 80


def test_train_test_split_has_no_overlap_and_full_coverage():
    input = np.arange(50).reshape(50, 1).astype(float)
    labels = np.arange(50)
    train_input, test_input, _, _ = train_test_split(input, labels, test_size=0.3, seed=1)
    train_set = set(train_input[:, 0].astype(int).tolist())
    test_set = set(test_input[:, 0].astype(int).tolist())
    assert train_set.isdisjoint(test_set)
    assert train_set | test_set == set(range(50))


def test_train_test_split_keeps_input_and_labels_paired():
    input = np.arange(20).reshape(20, 1).astype(float)  # input[i] == i
    labels = np.arange(20)  # labels[i] == i
    train_input, test_input, train_labels, test_labels = train_test_split(
        input, labels, test_size=0.25, seed=2
    )
    assert np.array_equal(train_input[:, 0].astype(int), train_labels)
    assert np.array_equal(test_input[:, 0].astype(int), test_labels)


def test_train_test_split_is_reproducible_with_the_same_seed():
    input = np.arange(30).reshape(30, 1).astype(float)
    labels = np.arange(30)
    a = train_test_split(input, labels, test_size=0.2, seed=42)
    b = train_test_split(input, labels, test_size=0.2, seed=42)
    for a_arr, b_arr in zip(a, b):
        assert np.array_equal(a_arr, b_arr)


def test_k_fold_split_returns_k_pairs():
    splits = k_fold_split(n_samples=20, k=5, seed=0)
    assert len(splits) == 5


def test_k_fold_split_val_sets_partition_every_sample_exactly_once():
    splits = k_fold_split(n_samples=23, k=4, seed=0)  # not evenly divisible on purpose
    all_val_indices = np.concatenate([val_idx for _, val_idx in splits])
    assert sorted(all_val_indices.tolist()) == list(range(23))
    # each index appears in exactly one fold's val_idx
    assert len(all_val_indices) == len(set(all_val_indices.tolist()))


def test_k_fold_split_train_and_val_never_overlap_within_a_fold():
    splits = k_fold_split(n_samples=30, k=6, seed=1)
    for train_idx, val_idx in splits:
        assert set(train_idx.tolist()).isdisjoint(set(val_idx.tolist()))
        assert set(train_idx.tolist()) | set(val_idx.tolist()) == set(range(30))


def test_k_fold_split_folds_are_roughly_equal_size():
    splits = k_fold_split(n_samples=20, k=4, seed=0)
    val_sizes = [len(val_idx) for _, val_idx in splits]
    assert max(val_sizes) - min(val_sizes) <= 1
    assert sum(val_sizes) == 20
