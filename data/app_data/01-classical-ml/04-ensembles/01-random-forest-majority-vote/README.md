---
name: ensembles-random-forest-majority-vote
title: 'Random Forest: majority vote aggregation'
tags: [classical-ml, ensembles, random-forest]
difficulty: Beginner
---

## Statement

Implement:

```python
def random_forest_predict(trees: list[dict], input: np.ndarray) -> np.ndarray:
    """
    trees: a list of already-built trees.
    Returns: shape (n_samples,), majority vote across all trees.
    """
```

- Reuse `03-best-split-minimal-tree`'s `predict_tree`, don't reimplement tree traversal here.
- Ties are broken by the lower class label (a natural side effect of using sorted class values, no special-case code needed).

## Theory

A single decision tree, greedily built, has a real weakness: `03-best-split-minimal-tree`'s Theory names it directly, greedy top-down search can miss useful structure (the XOR example), and a tree built all the way down to pure leaves overfits the specific training samples it saw. A random forest's answer isn't a better tree, it's _many_ trees, each trained slightly differently (typically on a bootstrap-resampled version of the training set, `02-bagging` names this), and a prediction that combines all of their opinions.

For classification, "combines all of their opinions" means a vote: run every tree on the same input, and whichever class gets the most votes wins.

```text
tree_1(x), tree_2(x), ..., tree_n(x)  -->  majority(votes)
```

The value of this isn't that any individual tree gets better, each one is still built the same greedy way, on its own resampled data, and might individually be a mediocre or even outright wrong predictor on a given sample. The value is that their _mistakes_ tend to be less correlated than their correct answers, different trees, seeing different resampled data, tend to overfit to different specific noise, so voting cancels out a good deal of that noise while the genuine signal (which every tree tends to pick up, since it's really there in the data) survives the vote intact.

## Explanation

`votes = np.array([predict_tree(tree, input) for tree in trees])` runs every tree once, stacking results into shape `(n_trees, n_samples)`, row `i` is every prediction tree `i` made, column `j` is every tree's opinion on sample `j`.

For each sample (each column `votes[:, i]`), `np.unique(..., return_counts=True)` gets the distinct classes voted for and how many trees voted for each, `values[np.argmax(counts)]` picks the class with the most votes. `np.unique` returns its `values` sorted, and `np.argmax` returns the _first_ index achieving the maximum, so a tie between class `0` and class `1` resolves to `0`, a deterministic, if arbitrary, tie-break, not a crash or a random choice.
