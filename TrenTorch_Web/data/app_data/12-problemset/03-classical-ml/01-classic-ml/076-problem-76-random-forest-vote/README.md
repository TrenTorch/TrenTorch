---
name: problem-76-random-forest-vote
title: 'Random Forest Vote'
tags: [problemset, classical-ml-trees-ensembles, random-forest]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'random forest'
hint: 'for every column count the labels and take the most frequent (smallest on ties)'
tools: [NumPy]
---

## Statement

Combine the class predictions of several trees by majority vote. `predictions` has shape `(n_trees, n_samples)`; for every sample take the class chosen by most trees, breaking ties toward the smallest label.

Implement `solve(predictions)`.

**Returns.** Return a NumPy array of length `n_samples` with the voted class for each sample.

### Examples

**Example 1**

Input:

```python
solve([[0, 1, 1], [0, 1, 0], [1, 1, 0]])
```

Output:

```text
[0, 1, 0]
```

**Example 2**

Input:

```python
solve([[0, 1], [1, 1], [1, 0], [0, 0]])
```

Output:

```text
[0, 0]
```

## Theory

### The simple version

A random forest asks every tree for its answer and goes with the most popular one. Individual trees make mistakes, but if their mistakes are not all the same, the crowd is usually right more often than any single tree.

### The rule

$$\hat y_j=\arg\max_{c}\;\#\{t: f_t(x_j)=c\}$$

## Explanation

Each column of the input holds all trees' answers for one sample, so the code loops over the transposed array and counts the labels in each column. In the second example sample 0 gets two votes each for classes 0 and 1, and the tie goes to the smaller label 0.
