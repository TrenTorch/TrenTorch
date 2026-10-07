---
name: problem-71-best-binary-split
title: 'Best Binary Split'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'try each distinct x except the max; score = weighted Gini of x<=t and x>t; keep the lowest'
tools: [NumPy]
---

## Statement

Find the best threshold for splitting one numeric feature `x` against class labels `y`. Candidate thresholds are the distinct observed values of `x` except the largest; the split is `x <= t` versus `x > t`, and its score is the weighted Gini impurity of the two sides. Pick the lowest score, preferring the smaller threshold on ties.

Implement `solve(x,y)`.

**Returns.** Return a tuple `(weighted_gini, threshold)`, or `None` if `x` has fewer than two distinct values (no valid split).

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1])
```

Output:

```text
(0.0, 2.0)
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 5.0], [0, 1, 0, 1, 1])
```

Output:

```text
(0.266667, 3.0)
```

**Example 3**

Input:

```python
solve([2.0, 2.0], [0, 1])
```

Output:

```text
None
```

## Theory

### The simple version

A decision tree grows by repeatedly asking the best yes/no question about a feature, such as "is $x\le2.5$?". The best question is the one whose two answers are the purest groups. Purity of the whole split is the Gini impurity of each side weighted by how many samples it holds.

### The formula

$$\text{score}(t)=\frac{n_L}{n}\,G(y_L)+\frac{n_R}{n}\,G(y_R),\qquad L=\{x\le t\},\;R=\{x>t\}$$

## Explanation

Only values that actually occur in the data can change the partition, so each distinct value (except the maximum, which would leave the right side empty) is tried. A later threshold replaces the best one only if its score is lower by more than $10^{-12}$, so ties (including floating-point noise) keep the smallest threshold. Here the threshold itself is a data value rather than the midpoint between neighbours.
