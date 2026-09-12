---
name: unsupervised-isolation-forest
title: 'Isolation Forest: anomaly detection via random splits'
tags: [classical-ml, unsupervised, anomaly-detection]
difficulty: Intermediate
---

## Statement

Implement:

```python
def build_isolation_tree(input, max_depth, rng) -> dict: ...
def path_length(tree, x, current_depth=0) -> float: ...
def isolation_forest_fit(input, n_trees, max_depth, seed=None) -> list[dict]: ...
def anomaly_scores(forest, input, sample_size) -> np.ndarray: ...
```

- No labels anywhere, this is unsupervised, "anomalous" is never told to the model, it falls out of how easy a point is to isolate.
- Splits are **purely random**: a random feature, a random threshold within that feature's observed range, no Gini impurity or information gain involved at all.

## Theory

Every tree in this curriculum so far picked its splits to _separate classes well_ (Gini impurity, information gain) or _fit a target well_ (variance reduction). An isolation tree does neither, it picks a random feature and a random threshold within that feature's range, every single time, with no goal beyond splitting.

The insight: with purely random splits, an outlier, a point sitting far from the bulk of the data, tends to get separated from everything else in very few splits, almost any random threshold near it isolates it immediately. A normal point, buried in a dense cluster, needs many splits before it ends up alone, most random thresholds still leave it grouped with its neighbors.

```text
outlier: far from everything -> isolated in just a few random splits -> SHORT path
normal:  buried in a dense cluster -> needs many splits to isolate -> LONG path
```

So "how many splits does it take to isolate this point" (its path length in the tree) is itself a usable anomaly signal, no labels required. Averaging path length across many independently-built random trees (a forest of them) smooths out the randomness of any one tree's specific split choices.

The path length needs one refinement: a max-depth tree often stops with more than one sample still in a leaf (not fully isolated). That remaining group's own expected isolation cost is estimated by `c(n)`, the average number of comparisons an unsuccessful binary-search-tree lookup takes over `n` items, `2*(ln(n-1) + 0.5772...) - 2*(n-1)/n` (`0.5772...` is the Euler-Mascheroni constant, a real constant that shows up in exactly this average-BST-depth formula). Adding it to the actual splits taken gives a fair path-length estimate even for a leaf that wasn't split all the way down to size 1.

The final anomaly score, `2^(-average_path_length / c(sample_size))`, maps "short path" to a score near `1` (anomalous) and "long path, close to `c(sample_size)`, the expected path length for a typical point" to a score near `0.5` or below (normal). This normalization is what makes scores comparable across datasets of different sizes.

## Explanation

`build_isolation_tree` stops at a leaf when `max_depth` runs out, `1` or fewer samples remain, or the randomly-chosen feature happens to be constant across every remaining sample (no threshold could possibly split it). Otherwise, `rng.integers`/`rng.uniform` pick the random feature and threshold, and the recursive case is otherwise the exact same shape `03-best-split-minimal-tree`'s `build_tree` uses, just with the split chosen randomly instead of by search.

`path_length` walks the tree exactly like `predict_tree` does, counting depth as it goes, and at a leaf adds `_average_path_length_correction(tree["size"])`, the `c(n)` formula, for whatever samples never got fully isolated.

`isolation_forest_fit` builds `n_trees` independent trees, each on the _full_ `input` (no bootstrapping here, the randomness comes from the random splits themselves, not from resampling data the way `02-bagging` did).

`anomaly_scores` averages `path_length` across every tree in the forest for each sample, then applies the `2^(-avg / c(sample_size))` formula, `c(sample_size)` is the same correction function, evaluated once at the dataset's own size, this is the "typical" path length everything else is measured against.
