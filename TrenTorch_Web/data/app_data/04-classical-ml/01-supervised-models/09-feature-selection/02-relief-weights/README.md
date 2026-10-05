---
name: feature-selection-relief-weights
title: 'Relief feature weights'
tags: [classical-ml, feature-selection, filter-methods, relief, nearest-neighbor]
difficulty: Intermediate
---

## Statement

### Features that separate neighbors of different classes

A feature is useful when two nearby points that share a label agree on it, and two nearby points with different labels disagree on it. Relief scores every feature with exactly that idea, using one nearest same-class neighbor (the hit) and one nearest other-class neighbor (the miss) for each sample.

Implement `relief_weights(X, y)`. It returns one weight per feature.

For each sample `i`:

1. Find the hit: the nearest other sample with the same label, by Euclidean distance on all features. Ties go to the smallest index.
2. Find the miss: the nearest sample with a different label, by the same rule.
3. For every feature `j`, add `(|X[i, j] - X[miss, j]| - |X[i, j] - X[hit, j]|) / range_j` to `w[j]`, where `range_j = max - min` of feature `j`.

Divide the total by `n`.

### Constraints

- `X` is 2-D with at least two rows, `y` has one label per row, otherwise raise `ValueError`.
- A feature with zero range contributes nothing. Use a divisor of 1 for it.
- If a sample has no hit or no miss (its class is the only one present), skip that sample but still divide by `n`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute the full distance vector from sample `i`, set its own entry to infinity, then mask by the label to pick hits and misses.

</details>

## Theory

Relief is a filter, so it never fits a model. Its weights are an average of local differences, which means it can rank features that only matter through interactions with other features, where a global correlation score would miss them. Its weakness is the same locality: with few samples per neighborhood the estimate is noisy.

### Where this shows up in production

Feature screening for noisy wide tables, such as genomics panels or sensor data with many irrelevant channels, where univariate tests miss features that only matter in combination with others. Relief runs once before training and hands a shortlist to the real model.

### Using it to make decisions

Use it when you suspect interactions and the sample count is large enough that every point has close neighbours of both classes. Range-scale the features first, because the Euclidean neighbourhood changes when one feature is stretched. Choose how many features to keep by checking downstream validation performance at several cut-offs, not by a fixed weight threshold. If two features are near copies of each other, Relief scores both highly, so pair it with a redundancy check.

### Pros and cons

**Pros:** it sees feature interactions, handles several classes, and costs one pass over the neighbour structure.

**Cons:** the cost is quadratic in the number of samples, and the weights are sensitive to scaling and to irrelevant features that distort the neighbourhood. Redundant features all score high, and the method gives no guarantee about the best subset.

## Explanation

The solution loops over samples, uses the candidate index arrays to find the nearest hit and miss, and accumulates normalized absolute differences. Because candidates are kept in ascending index order, `np.argmin` returns the smallest index on ties.
