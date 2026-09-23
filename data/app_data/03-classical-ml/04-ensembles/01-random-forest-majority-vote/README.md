---
name: ensembles-random-forest-majority-vote
title: 'Random Forest: majority vote aggregation'
tags: [classical-ml, ensembles, random-forest]
difficulty: Beginner
---

## Statement

### The problem, from first principles

One tree can make a brittle decision from its particular training data. A forest lets independently built trees vote, so patterns they agree on survive while individual tree mistakes can be outvoted. This question combines already-built classification trees; it does not build or traverse them itself.

### From theory to code

Implement `random_forest_predict(trees, input)` by collecting each tree's predictions and taking a separate majority vote for every input row.

### Constraints

- `trees` is a list of compatible fitted tree dictionaries and `input` has shape `(n_samples, n_features)`.
- Return integer labels with shape `(n_samples,)`.
- Reuse `predict_tree` once per tree; do not reimplement traversal.
- Vote independently down each prediction column.
- Break ties by the lower class label.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Stacking one prediction vector per tree produces rows of tree opinions and columns of opinions about one sample.

</details>

<details><summary>Hint 2</summary>

For each column, `np.unique(..., return_counts=True)` supplies sorted labels and vote totals. `np.argmax` chooses the first maximum.

</details>

## Theory

### The simple version

Voting does not improve a single tree. It improves the group when their errors differ: noise that misleads one resampled tree is less likely to mislead a majority, while recurring signal receives repeated votes.

### The formula

```text
votes[t, i] = predict_tree(trees[t], input)[i]
prediction[i] = unique(votes[:, i])[argmax(vote_counts)]
```

`np.unique` returns labels in sorted order, and `np.argmax` returns the first tied maximum, so a class-label tie resolves to the lower label.

### How PyTorch actually implements this

Context only, untested by your submission: random forests are generally supplied by tree libraries rather than `torch.nn`; tensor vote counts can express the same aggregation.

## Explanation

`votes = np.array([predict_tree(tree, input) for tree in trees])` makes shape `(n_trees, n_samples)`. `predictions` is explicitly integer and has one slot per sample. The loop selects `votes[:, i]`, counts its sorted distinct labels, and stores `values[np.argmax(counts)]`. That column orientation is why every sample gets an independent majority rather than one global vote.
