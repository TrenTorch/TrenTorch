---
name: majority-bag-vote-company-210
title: 'majority-bag-vote — Airbnb case'
tags: [problemset, classical-ml-trees-ensembles, bagging, airbnb]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Airbnb'
hint: 'bincount the votes; pick the smallest class among those with the highest count'
tools: [NumPy]
---

## Statement

Airbnb-inspired listing-quality model uses several bootstrap-trained classifiers that may disagree on a prediction. You need to aggregate their class votes deterministically so the team has a reliable majority-vote baseline.

`predictions` holds the class predicted by each bootstrap-trained classifier for **one** sample. Return the most frequent class; if several classes tie, return the smallest.

Implement `solve(predictions)`.

**Returns.** Return the winning class as a Python `int`. Classes are non-negative integers.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1, 0, 1])
```

Output:

```text
1
```

**Example 2**

Input:

```python
solve([2, 0, 2, 0, 1])
```

Output:

```text
0
```

## Theory

### The simple version

Bagging trains several models on different resamples of the data and lets them vote. Their individual errors tend to differ, so the majority is usually more reliable than any single member. A deterministic tie-break keeps results reproducible when votes are split evenly.

### The rule

$$\hat c=\min\Big\{c:\;\#\{b:\hat y_b=c\}=\max_{c'}\#\{b:\hat y_b=c'\}\Big\}$$

## Explanation

`np.bincount` counts the votes for each class label, and the smallest class among those with the maximum count wins. In the second example classes $0$ and $2$ each get two votes, so the smaller label $0$ is returned.
