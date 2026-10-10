---
name: problem-75-random-feature-subset
title: 'Random Feature Subset'
tags: [problemset, classical-ml-trees-ensembles, random-forest]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'random forest'
hint: 'rng.choice(n_features, size=m, replace=False)'
tools: [NumPy]
---

## Statement

Choose `m` distinct feature indices out of `n_features`, uniformly at random **without replacement**, using `np.random.default_rng(seed).choice(n_features, size=m, replace=False)`. This is the feature subset a random-forest node considers when looking for a split.

Implement `solve(n_features,m,seed=0)`.

**Returns.** Return an integer NumPy array of length `m` (in drawn order, not sorted). `m` must not exceed `n_features`.

### Examples

**Example 1**

Input:

```python
solve(5, 2, 0)
```

Output:

```text
[3, 4]
```

**Example 2**

Input:

```python
solve(10, 3, 7)
```

Output:

```text
[7, 5, 6]
```

## Theory

### The simple version

A random forest decorrelates its trees by letting each split look at only a random subset of the features. If every tree could always use the single strongest feature, all trees would look alike and averaging them would help much less.

### Typical size

For classification, $m\approx\sqrt{d}$ features per split is the common default; for regression $d/3$.

### Why it matters

- Random forests look at only a random subset of features at each split so the trees differ from each other.
- Less correlated trees average to a better ensemble.

### How it works

1. Draw $m$ distinct feature indices without replacement.
2. Only these may be used at that split.

### Worked example

Choosing $2$ of $5$ features with seed $0$ gives [3, 4], so only those two features are considered at that node.

## Explanation

Sampling without replacement guarantees `m` different features. Each call builds its own seeded generator, so the subset is reproducible. The order of the returned indices is whatever NumPy draws and should not be relied on.
