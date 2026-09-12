"""
pytest data/app_data/01-classical-ml/04-ensembles/02-bagging/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
bootstrap_sample = _module.bootstrap_sample
train_random_forest = _module.train_random_forest
random_forest_predict = load_solution(
    "01-classical-ml/04-ensembles/01-random-forest-majority-vote"
).random_forest_predict


def test_bootstrap_sample_preserves_shape():
    input = np.arange(20.0).reshape(10, 2)
    labels = np.arange(10)
    boot_input, boot_labels = bootstrap_sample(input, labels, seed=0)
    assert boot_input.shape == input.shape
    assert boot_labels.shape == labels.shape


def test_bootstrap_sample_is_reproducible_with_the_same_seed():
    input = np.arange(20.0).reshape(10, 2)
    labels = np.arange(10)
    a_input, a_labels = bootstrap_sample(input, labels, seed=7)
    b_input, b_labels = bootstrap_sample(input, labels, seed=7)
    assert np.array_equal(a_input, b_input)
    assert np.array_equal(a_labels, b_labels)


def test_bootstrap_sample_keeps_rows_and_labels_paired():
    # labels[i] must always match input[i] -- resampling with a shared
    # index array is what guarantees this, a separately-resampled
    # labels array would break the pairing.
    input = np.arange(10.0).reshape(10, 1)  # input[i] == i
    labels = np.arange(10)  # labels[i] == i
    boot_input, boot_labels = bootstrap_sample(input, labels, seed=3)
    assert np.array_equal(boot_input[:, 0], boot_labels.astype(float))


def test_bootstrap_sample_draws_with_replacement_on_average_63_percent_unique():
    # A real statistical property of bootstrap resampling: each row has
    # roughly a 1 - 1/e ~= 63.2% chance of appearing at least once.
    # Averaged over many independent draws, well within a generous
    # tolerance band.
    n = 200
    input = np.arange(n).reshape(n, 1).astype(float)
    labels = np.arange(n)
    fractions = []
    for seed in range(30):
        boot_input, _ = bootstrap_sample(input, labels, seed=seed)
        fractions.append(len(np.unique(boot_input)) / n)
    assert 0.55 < np.mean(fractions) < 0.72


def test_train_random_forest_returns_the_requested_number_of_trees():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(30, 2))
    labels = (input[:, 0] > 0).astype(int)
    trees = train_random_forest(input, labels, n_trees=5, max_depth=3, seed=1)
    assert len(trees) == 5


def test_trees_are_genuinely_different_not_five_copies_of_one_bootstrap_draw():
    # Directly targets the "re-seeded the RNG inside the loop" bug:
    # if every tree trained on the identical bootstrap sample, they'd
    # all be structurally identical dicts. With enough trees on noisy
    # data, at least one pair should differ.
    rng = np.random.default_rng(2)
    input = rng.normal(size=(40, 2))
    labels = (input[:, 0] + rng.normal(scale=0.5, size=40) > 0).astype(int)
    trees = train_random_forest(input, labels, n_trees=8, max_depth=4, seed=5)
    assert any(trees[0] != tree for tree in trees[1:])


def test_forest_achieves_good_accuracy_on_separable_data():
    rng = np.random.default_rng(4)
    input = rng.normal(size=(200, 2))
    labels = (input[:, 0] + input[:, 1] > 0).astype(int)
    trees = train_random_forest(input, labels, n_trees=15, max_depth=4, seed=9)
    predictions = random_forest_predict(trees, input)
    accuracy = np.mean(predictions == labels)
    assert accuracy > 0.85
