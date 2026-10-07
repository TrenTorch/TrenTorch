---
name: problem-84-feature-importance-from-splits
title: 'Feature Importance from Splits'
tags: [problemset, classical-ml-trees-ensembles, feature-importance]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'feature importance'
hint: 'sum per feature in a dict, then divide by the total'
tools: [NumPy]
---

## Statement

Turn the impurity reductions of the splits in a tree into feature importances. `splits` is a list of `(feature, impurity_reduction)` pairs, one per internal node. Sum the reductions per feature and normalise so the importances add up to 1.

Implement `solve(splits)`.

**Returns.** Return a dict `{feature: importance}` in order of first appearance. If the total reduction is $0$ the un-normalised sums are returned.

### Examples

**Example 1**

Input:

```python
solve([('a', 1.0), ('b', 2.0), ('a', 1.0)])
```

Output:

```text
{'a': 0.5, 'b': 0.5}
```

**Example 2**

Input:

```python
solve([('x', 0.3), ('y', 0.1)])
```

Output:

```text
{'x': 0.75, 'y': 0.25}
```

## Theory

### The simple version

A feature is important to a tree if the splits that use it clean up the classes a lot. Adding up the impurity reduction achieved by every split on a feature, then dividing by the grand total, gives a share between 0 and 1 for each feature.

### The formula

$$\text{imp}_f=\frac{\sum_{s:\,\text{feature}(s)=f}\Delta_s}{\sum_s\Delta_s}$$

## Explanation

A feature that is used at several nodes accumulates its reductions, as `'a'` does in the first example ($1+1=2$ out of $4$). This impurity-based measure is cheap but biased toward features with many distinct values.
