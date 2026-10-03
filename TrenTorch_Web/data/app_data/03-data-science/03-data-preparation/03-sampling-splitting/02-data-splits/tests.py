"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
train_val_test_split = _module.train_val_test_split
time_ordered_split = _module.time_ordered_split
k_fold_indices = _module.k_fold_indices
expanding_window_splits = _module.expanding_window_splits


# ---- 1-6: shuffled three-way split ----


def test_1_sizes_follow_the_rounded_fractions():
    train, val, test = train_val_test_split(100, 0.15, 0.25, np.random.default_rng(0))
    assert (len(train), len(val), len(test)) == (60, 15, 25)


def test_2_sets_are_disjoint_and_cover_every_row():
    train, val, test = train_val_test_split(97, 0.2, 0.2, np.random.default_rng(1))
    everything = np.concatenate([train, val, test])
    assert sorted(everything.tolist()) == list(range(97))


def test_3_matches_one_permutation_in_train_val_test_order():
    train, val, test = train_val_test_split(10, 0.2, 0.3, np.random.default_rng(7))
    order = np.random.default_rng(7).permutation(10)
    np.testing.assert_array_equal(np.concatenate([train, val, test]), order)


def test_4_the_split_is_actually_shuffled():
    train, _, _ = train_val_test_split(1000, 0.1, 0.1, np.random.default_rng(2))
    assert not np.array_equal(train, np.sort(train))


def test_5_different_seeds_give_different_splits():
    a = train_val_test_split(50, 0.2, 0.2, np.random.default_rng(3))[2]
    b = train_val_test_split(50, 0.2, 0.2, np.random.default_rng(4))[2]
    assert not np.array_equal(a, b)


def test_6_zero_fractions_put_everything_in_training():
    train, val, test = train_val_test_split(20, 0.0, 0.0, np.random.default_rng(5))
    assert len(train) == 20 and len(val) == 0 and len(test) == 0


# ---- 7-10: time-ordered split ----


def test_7_time_split_is_chronological():
    train, val, test = time_ordered_split(10, 0.2, 0.2)
    np.testing.assert_array_equal(train, np.arange(0, 6))
    np.testing.assert_array_equal(val, np.arange(6, 8))
    np.testing.assert_array_equal(test, np.arange(8, 10))


def test_8_every_training_row_precedes_every_validation_and_test_row():
    train, val, test = time_ordered_split(200, 0.15, 0.15)
    assert train.max() < val.min() and val.max() < test.min()


def test_9_time_split_sizes_match_the_shuffled_split():
    a = time_ordered_split(103, 0.1, 0.2)
    b = train_val_test_split(103, 0.1, 0.2, np.random.default_rng(0))
    assert [len(s) for s in a] == [len(s) for s in b]


def test_10_time_split_is_deterministic_and_covers_all_rows():
    s1 = time_ordered_split(31, 0.2, 0.2)
    s2 = time_ordered_split(31, 0.2, 0.2)
    for a, b in zip(s1, s2):
        np.testing.assert_array_equal(a, b)
    assert sum(len(s) for s in s1) == 31


# ---- 11-15: k-fold ----


def test_11_there_are_k_folds_and_each_row_is_validated_once():
    folds = k_fold_indices(23, 5, np.random.default_rng(0))
    assert len(folds) == 5
    validated = np.concatenate([val for _, val in folds])
    assert sorted(validated.tolist()) == list(range(23))


def test_12_train_and_validation_are_disjoint_and_complete_per_fold():
    for train, val in k_fold_indices(20, 4, np.random.default_rng(1)):
        assert set(train).isdisjoint(set(val))
        assert sorted(np.concatenate([train, val]).tolist()) == list(range(20))


def test_13_fold_sizes_follow_array_split():
    folds = k_fold_indices(10, 3, np.random.default_rng(2))
    assert [len(val) for _, val in folds] == [4, 3, 3]


def test_14_matches_one_permutation_cut_into_blocks():
    folds = k_fold_indices(12, 4, np.random.default_rng(9))
    blocks = np.array_split(np.random.default_rng(9).permutation(12), 4)
    for (train, val), block in zip(folds, blocks):
        np.testing.assert_array_equal(val, block)
    np.testing.assert_array_equal(folds[0][0], np.concatenate(blocks[1:]))


def test_15_k_equal_to_n_is_leave_one_out():
    folds = k_fold_indices(6, 6, np.random.default_rng(3))
    assert all(len(val) == 1 and len(train) == 5 for train, val in folds)


# ---- 16-20: expanding window ----


def test_16_each_split_trains_only_on_the_past():
    for train, val in expanding_window_splits(30, 4, 10):
        assert train.max() < val.min()


def test_17_training_window_grows_with_each_split():
    sizes = [len(train) for train, _ in expanding_window_splits(30, 4, 10)]
    assert sizes == sorted(sizes) and len(set(sizes)) == 4


def test_18_hand_computed_blocks():
    splits = expanding_window_splits(10, 2, 4)
    np.testing.assert_array_equal(splits[0][0], np.arange(4))
    np.testing.assert_array_equal(splits[0][1], [4, 5, 6])
    np.testing.assert_array_equal(splits[1][0], np.arange(7))
    np.testing.assert_array_equal(splits[1][1], [7, 8, 9])


def test_19_validation_blocks_partition_the_later_rows():
    splits = expanding_window_splits(25, 5, 5)
    validated = np.concatenate([val for _, val in splits])
    np.testing.assert_array_equal(validated, np.arange(5, 25))


def test_20_returns_one_pair_per_split():
    assert len(expanding_window_splits(40, 6, 10)) == 6
