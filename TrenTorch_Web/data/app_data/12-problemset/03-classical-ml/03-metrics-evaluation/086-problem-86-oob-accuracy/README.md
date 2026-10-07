---
name: problem-86-oob-accuracy
title: 'OOB Accuracy'
tags: [problemset, classical-ml-trees-ensembles, out-of-bag]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'out of bag'
hint: 'mean of (y_true == y_pred)'
tools: [NumPy]
---

## Statement

Compute the out-of-bag accuracy of a bagged ensemble: the fraction of samples whose out-of-bag prediction equals the true label. `y_true` and `y_pred` are aligned label arrays.

Implement `solve(y_true, y_pred)`.

**Returns.** Return a float in $[0,1]$.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1], [0, 0, 1])
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([1, 2, 2], [1, 2, 2])
```

Output:

```text
1.0
```

## Theory

### The simple version

Each tree in a random forest never saw about a third of the training samples. Predicting each sample using only the trees that did _not_ see it gives an honest estimate of generalisation without needing a separate validation set. The out-of-bag accuracy is just how often those predictions are right.

### The formula

$$\text{OOB accuracy}=\frac1n\sum_i\mathbb 1\big[\hat y^{\text{oob}}_i=y_i\big]$$

## Explanation

This function only does the final comparison; the out-of-bag predictions themselves come from voting over the trees whose mask excludes the sample. In the first example two of three labels match.
