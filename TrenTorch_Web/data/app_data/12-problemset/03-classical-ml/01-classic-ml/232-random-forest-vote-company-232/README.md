---
name: random-forest-vote-company-232
title: 'random-forest-vote — Grab case'
tags: [problemset, classical-ml-trees-ensembles, random-forest, grab]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Grab'
hint: 'mean over trees (axis 0), then argmax'
tools: [NumPy]
---

## Statement

Grab-inspired demand classifier combines predictions from several decision trees trained on different samples. You need to average the trees' class probabilities and return the class with the highest mean probability, giving a deterministic ensemble baseline.

`P` has one row per tree and one column per class: row $t$ is tree $t$'s predicted class-probability vector for a single sample. Average the rows and return the index of the class with the highest mean probability (the lowest index on a tie).

Implement `solve(P)`.

**Returns.** Return the winning class index as a Python `int`.

`P` has one row per tree and one column per class: row $t$ is tree $t$'s predicted class-probability vector for a single sample. Average the rows and return the index of the class with the highest mean probability (the lowest index on a tie).

Implement `solve(P)`.

**Returns.** Return the winning class index as a Python `int`.

### Examples

**Example 1**

Input:

```python
solve([[0.8, 0.2], [0.4, 0.6], [0.7, 0.3]])
```

Output:

```text
0
```

**Example 2**

Input:

```python
solve([[0.2, 0.5, 0.3], [0.3, 0.3, 0.4]])
```

Output:

```text
1
```

## Theory

### The simple version

A random forest combines many trees. Instead of letting each tree cast one hard vote, "soft voting" averages the probabilities the trees assign to each class, so a tree that is very confident counts for more than a hesitant one.

### The rule

$$\bar p_c=\frac1T\sum_{t=1}^{T}p_{t,c},\qquad \hat c=\arg\max_c\bar p_c$$

### Why it matters

- A forest predicts by combining many trees.
- Averaging class probabilities (soft voting) lets a confident tree count for more than a hesitant one.

### How it works

1. Average the probability rows over the trees.
2. Return the index of the largest mean (lowest index on ties).

### Worked example

The three trees give class-0 probabilities $0.8$, $0.4$ and $0.7$, mean $0.633$, and class-1 mean $0.367$. Class 0 wins even though the second tree preferred class 1.

## Explanation

In the first example the mean probabilities are $(0.633,0.367)$, so class $0$ wins even though the second tree preferred class $1$. `argmax` returns the first maximum, which makes ties deterministic.
