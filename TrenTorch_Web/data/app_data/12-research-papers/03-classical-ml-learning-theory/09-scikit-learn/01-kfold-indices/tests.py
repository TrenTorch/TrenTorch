"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/09-scikit-learn/01-kfold-indices/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sklearn-kfold")
kfold_indices = _module.kfold_indices


import numpy as np


def test_1_returns_k_pairs():
    assert len(kfold_indices(9, 3)) == 3


def test_2_test_folds_partition_all_indices():
    tests = np.concatenate([t for _, t in kfold_indices(10, 4)])
    np.testing.assert_array_equal(np.sort(tests), np.arange(10))


def test_3_train_and_test_cover_everything_without_overlap():
    for train, test in kfold_indices(7, 3):
        assert len(set(train) & set(test)) == 0
        assert len(train) + len(test) == 7


def test_4_fold_sizes_differ_by_at_most_one():
    sizes = [len(t) for _, t in kfold_indices(10, 4)]
    assert max(sizes) - min(sizes) <= 1


def test_5_matches_a_hand_case():
    pairs = kfold_indices(6, 3)
    np.testing.assert_array_equal(pairs[0][1], [0, 1])
    np.testing.assert_array_equal(pairs[0][0], [2, 3, 4, 5])


def test_6_does_not_mutate_arguments_or_returns_fresh_arrays():
    pairs = kfold_indices(4, 2)
    assert pairs[0][1] is not pairs[1][1]

