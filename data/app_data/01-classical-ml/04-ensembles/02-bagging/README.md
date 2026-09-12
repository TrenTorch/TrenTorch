---
name: ensembles-bagging
title: 'Stretch: bagging concept'
tags: [classical-ml, ensembles, random-forest, stretch]
difficulty: Beginner
---

## Statement

Implement:

```python
def bootstrap_sample(input: np.ndarray, labels: np.ndarray, seed: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Resample n_samples rows with replacement."""

def train_random_forest(input, labels, n_trees, max_depth, seed=None) -> list[dict]:
    """Train n_trees independent trees, each on its own bootstrap sample."""
```

- Reuse `03-best-split-minimal-tree`'s `build_tree`, don't reimplement tree construction.
- The returned list is directly usable by `01-random-forest-majority-vote`'s `random_forest_predict`.
- Build exactly one random generator, before the loop over trees, not one per tree.

## Theory

`01-random-forest-majority-vote` assumed the trees already existed and were somehow different from each other. **Bagging** ("bootstrap aggregating") is the "somehow": give every tree the same learning algorithm, but a different, randomly resampled view of the same training set.

A bootstrap sample draws `n_samples` rows _with replacement_ from the original `n_samples` rows, some rows appear more than once, some don't appear at all. On average, a bootstrap sample contains about 63% of the original rows (each row has roughly a `1 - 1/e ≈ 63.2%` chance of appearing at least once), the rest are duplicates of rows that did.

```text
original data
   ↓ bootstrap_sample (different random draw each time)
sample_1, sample_2, ..., sample_n
   ↓ build_tree (same algorithm, different data)
tree_1,   tree_2,   ...,   tree_n
   ↓ random_forest_predict (majority vote)
final prediction
```

This is exactly why voting helps, from `01-random-forest-majority-vote`'s Theory: each tree overfits to the specific noise in _its own_ resampled data, and since each sample is a different random draw, that noise looks different from tree to tree. The genuine signal in the data (not noise) appears in every bootstrap sample, just with a slightly different set of duplicated rows, so every tree still picks it up. Averaging (voting) cancels the tree-specific noise while preserving the shared signal.

## Explanation

`bootstrap_sample` draws `rng.integers(0, n_samples, size=n_samples)`, `n_samples` indices, each independently uniform over `0..n_samples-1`, exactly the "with replacement" draw Theory describes, then indexes both `input` and `labels` with the same index array so a row and its label always travel together.

`train_random_forest` builds `np.random.default_rng(seed)` exactly once, _outside_ the loop over `n_trees`, then passes that same generator object into `bootstrap_sample` on every iteration. Passing an already-created `Generator` to `np.random.default_rng` returns that identical object, unreseeded, so its internal state keeps advancing across every call, the same "build the generator once, let it advance" discipline `07-production-mini-batch`'s mini-batch training relies on, for the identical reason: re-creating `default_rng(seed)` inside the loop would give every tree the exact same bootstrap sample, one random draw copied `n_trees` times instead of `n_trees` genuinely different ones.
