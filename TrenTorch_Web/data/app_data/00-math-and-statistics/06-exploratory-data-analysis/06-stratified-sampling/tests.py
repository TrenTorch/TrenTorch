"""
pytest data/app_data/00-math-and-statistics/06-exploratory-data-analysis/06-stratified-sampling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/06-exploratory-data-analysis/{Path(__file__).resolve().parent.name}"
)
class_proportions = _module.class_proportions
stratified_sample_indices = _module.stratified_sample_indices


def test_class_proportions_matches_hand_computation():
    labels = np.array([0, 0, 0, 1, 1])
    result = class_proportions(labels)
    assert np.isclose(result[0], 0.6)
    assert np.isclose(result[1], 0.4)


def test_class_proportions_sums_to_one():
    labels = np.array([0, 1, 2, 0, 1, 0, 2, 2])
    result = class_proportions(labels)
    assert np.isclose(sum(result.values()), 1.0)


def test_stratified_sample_preserves_class_balance_on_imbalanced_data():
    labels = np.array([0] * 950 + [1] * 50)
    indices = stratified_sample_indices(labels, sample_size=100, seed=0)
    sampled_labels = labels[indices]
    fraction_class_1 = (sampled_labels == 1).mean()
    assert np.isclose(fraction_class_1, 0.05, atol=0.03)


def test_stratified_sample_never_misses_the_minority_class():
    labels = np.array([0] * 95 + [1] * 5)
    indices = stratified_sample_indices(labels, sample_size=20, seed=0)
    sampled_labels = labels[indices]
    assert (sampled_labels == 1).sum() >= 1


def test_stratified_sample_is_reproducible_with_same_seed():
    labels = np.array([0] * 50 + [1] * 50)
    a = stratified_sample_indices(labels, sample_size=20, seed=42)
    b = stratified_sample_indices(labels, sample_size=20, seed=42)
    assert np.array_equal(np.sort(a), np.sort(b))


def test_stratified_sample_indices_are_valid_and_unique():
    labels = np.array([0] * 30 + [1] * 20 + [2] * 10)
    indices = stratified_sample_indices(labels, sample_size=20, seed=1)
    assert len(indices) == len(set(indices))  # no duplicates (sampled without replacement)
    assert np.all(indices >= 0) and np.all(indices < len(labels))


def test_stratified_sample_covers_every_class_present_in_a_balanced_dataset():
    labels = np.array([0] * 30 + [1] * 30 + [2] * 30)
    indices = stratified_sample_indices(labels, sample_size=30, seed=2)
    sampled_labels = set(labels[indices])
    assert sampled_labels == {0, 1, 2}


def test_stratified_sample_gives_each_class_exactly_its_rounded_share():
    # Directly targets a mutant that samples uniformly across all
    # indices, ignoring class boundaries entirely: a correct
    # implementation must give EACH class exactly round(proportion *
    # sample_size) examples, deterministically, not just approximately
    # right numbers by luck.
    labels = np.array([0] * 80 + [1] * 20)  # proportions: 0.8, 0.2
    indices = stratified_sample_indices(labels, sample_size=50, seed=0)
    sampled_labels = labels[indices]
    assert (sampled_labels == 0).sum() == 40  # round(0.8 * 50)
    assert (sampled_labels == 1).sum() == 10  # round(0.2 * 50)


def test_stratified_sample_does_not_ignore_class_proportions():
    # Directly targets a mutant that samples uniformly across all
    # indices (ignoring class boundaries entirely), which on a severely
    # imbalanced dataset would very often produce zero minority-class
    # examples across repeated seeds -- the whole point stratification
    # exists to prevent.
    labels = np.array([0] * 990 + [1] * 10)
    minority_counts = []
    for seed in range(10):
        indices = stratified_sample_indices(labels, sample_size=60, seed=seed)
        minority_counts.append((labels[indices] == 1).sum())
    # A correctly-stratified sample should reliably include at least
    # one minority example across repeated seeds (expected ~0.5 per
    # draw, but stratification guarantees rounding keeps it near there).
    assert sum(minority_counts) > 0
