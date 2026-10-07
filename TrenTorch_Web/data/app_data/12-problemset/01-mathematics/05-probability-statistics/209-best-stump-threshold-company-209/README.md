---
name: best-stump-threshold-company-209
title: 'best-stump-threshold — Zomato case'
tags: [problemset, classical-ml-trees-ensembles, decision-trees, zomato]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Zomato'
hint: 'sort, try the midpoint between each pair of distinct neighbours, keep the lowest weighted Gini'
tools: [NumPy]
---

## Statement

Zomato-inspired ranking filter uses a single numeric feature to separate likely outcomes from unlikely ones. You need to find the threshold that gives the best classification score, providing a simple baseline before the team deploys a larger model. The threshold is the midpoint between two consecutive distinct sorted feature values that minimizes the sample-weighted Gini impurity of the two resulting sides, where the positive class is label 1. Ties go to the smaller threshold. Fewer than two distinct values raises `ValueError`.

Return the split threshold of a one-feature decision stump. Candidates are the midpoints between consecutive **distinct** sorted feature values; the winner minimises the sample-weighted Gini impurity of the two sides, and ties go to the smaller threshold.

Implement `solve(x, y)`.

**Returns.** Return the threshold as a Python float. At least two distinct feature values are required, otherwise `ValueError` is raised. Labels are 0/1.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 4.0, 7.0], [0, 0, 1, 1])
```

Output:

```text
3.0
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], [0, 1, 0, 1])
```

Output:

```text
1.5
```

**Example 3**

Input:

```python
solve([2.0, 2.0], [0, 1])
```

Output: Raises `ValueError`.

## Theory

### The simple version

A stump asks one yes/no question about one feature, such as "is the delivery distance below 3.5 km?". The best question is the one whose two answers are the purest groups. Placing the threshold halfway between neighbouring values is the usual convention because it is as far as possible from both.

### The score

$$\text{score}(t)=\frac{n_L}{n}\,G(y_L)+\frac{n_R}{n}\,G(y_R),\qquad t=\frac{x_{(i-1)}+x_{(i)}}{2}$$

## Explanation

Sorting once and cutting at every change of value tries each candidate in a single pass. Equal feature values can never be separated, so no threshold is placed between them. A later candidate replaces the current best only if its score is lower by more than $10^{-12}$, so exact (and floating-point-noise) ties keep the smaller threshold; in the second example thresholds $1.5$ and $3.5$ tie and $1.5$ wins.
