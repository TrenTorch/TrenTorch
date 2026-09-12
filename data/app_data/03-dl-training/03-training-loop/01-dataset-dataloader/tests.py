"""
pytest data/app_data/03-dl-training/03-training-loop/01-dataset-dataloader/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/03-training-loop/{Path(__file__).resolve().parent.name}")
ArrayDataset = _module.ArrayDataset
DataLoader = _module.DataLoader


def test_array_dataset_len_matches_number_of_samples():
    ds = ArrayDataset(np.zeros((10, 3)), np.zeros(10))
    assert len(ds) == 10


def test_array_dataset_getitem_returns_matching_feature_target_pair():
    features = np.array([[1.0, 2.0], [3.0, 4.0]])
    targets = np.array([0, 1])
    ds = ArrayDataset(features, targets)
    x, y = ds[1]
    assert np.allclose(x, [3.0, 4.0])
    assert y == 1


def test_dataloader_yields_every_sample_exactly_once_without_shuffle():
    features = np.arange(10).reshape(10, 1).astype(float)
    targets = np.arange(10)
    ds = ArrayDataset(features, targets)
    loader = DataLoader(ds, batch_size=3, shuffle=False)
    seen = []
    for batch_x, batch_y in loader:
        seen.extend(batch_y.tolist())
    assert sorted(seen) == list(range(10))


def test_dataloader_preserves_order_when_not_shuffled():
    features = np.arange(10).reshape(10, 1).astype(float)
    targets = np.arange(10)
    ds = ArrayDataset(features, targets)
    loader = DataLoader(ds, batch_size=4, shuffle=False)
    seen = []
    for batch_x, batch_y in loader:
        seen.extend(batch_y.tolist())
    assert seen == list(range(10))


def test_dataloader_last_batch_is_smaller_when_size_does_not_divide_evenly():
    features = np.arange(10).reshape(10, 1).astype(float)
    targets = np.arange(10)
    ds = ArrayDataset(features, targets)
    loader = DataLoader(ds, batch_size=3, shuffle=False)
    batch_sizes = [len(batch_y) for _, batch_y in loader]
    assert batch_sizes == [3, 3, 3, 1]


def test_dataloader_len_matches_ceiling_division():
    ds = ArrayDataset(np.zeros((10, 1)), np.zeros(10))
    loader = DataLoader(ds, batch_size=3)
    assert len(loader) == 4
    loader2 = DataLoader(ds, batch_size=5)
    assert len(loader2) == 2


def test_dataloader_features_and_targets_stay_correctly_paired_after_shuffling():
    features = np.arange(20).reshape(20, 1).astype(float)
    targets = np.arange(20)  # target[i] == feature[i, 0] by construction
    ds = ArrayDataset(features, targets)
    loader = DataLoader(ds, batch_size=4, shuffle=True, seed=42)
    for batch_x, batch_y in loader:
        assert np.allclose(batch_x[:, 0], batch_y)


def test_dataloader_shuffle_with_same_seed_produces_the_same_order():
    features = np.arange(10).reshape(10, 1).astype(float)
    targets = np.arange(10)
    ds = ArrayDataset(features, targets)
    order1 = [y for _, batch_y in DataLoader(ds, 3, shuffle=True, seed=7) for y in batch_y.tolist()]
    order2 = [y for _, batch_y in DataLoader(ds, 3, shuffle=True, seed=7) for y in batch_y.tolist()]
    assert order1 == order2


def test_dataloader_shuffle_actually_changes_the_order():
    features = np.arange(30).reshape(30, 1).astype(float)
    targets = np.arange(30)
    ds = ArrayDataset(features, targets)
    unshuffled = [y for _, batch_y in DataLoader(ds, 30, shuffle=False) for y in batch_y.tolist()]
    shuffled = [y for _, batch_y in DataLoader(ds, 30, shuffle=True, seed=1) for y in batch_y.tolist()]
    assert unshuffled != shuffled


def test_shuffle_uses_seeded_random_state_not_unseeded_global_random():
    # Directly targets a mutant that shuffles with plain np.random.shuffle
    # (the global, unseeded RNG) instead of np.random.RandomState(seed):
    # two DataLoaders built with the SAME seed would then no longer
    # produce identical orders.
    features = np.arange(50).reshape(50, 1).astype(float)
    targets = np.arange(50)
    ds = ArrayDataset(features, targets)
    order1 = [y for _, batch_y in DataLoader(ds, 50, shuffle=True, seed=123) for y in batch_y.tolist()]
    order2 = [y for _, batch_y in DataLoader(ds, 50, shuffle=True, seed=123) for y in batch_y.tolist()]
    assert order1 == order2
