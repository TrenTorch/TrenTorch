---
name: problem-69-gini-impurity
title: 'Gini Impurity'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: '1 minus the sum of squared class proportions'
tools: [NumPy]
---

## Statement

Compute the Gini impurity of a node from its class counts.

Implement `solve(counts)`.

**Returns.** Return a float in $[0,1)$. Counts must be non-negative (otherwise `ValueError`). A node with no samples at all has impurity `0.0`.

### Examples

**Example 1**

Input:

```python
solve([2, 2])
```

Output:

```text
0.5
```

**Example 2**

Input:

```python
solve([5, 0, 0])
```

Output:

```text
0.0
```

**Example 3**

Input:

```python
solve([1, 1, 1, 1])
```

Output:

```text
0.75
```

## Theory

### The simple version

Gini impurity is the chance that two items drawn at random (with replacement) from the node belong to different classes. A pure node scores 0, and the score grows as the classes get more mixed. Decision trees use it to pick the splits that make nodes purer.

### The formula

$$G=1-\sum_{k}p_k^2,\qquad p_k=\frac{n_k}{\sum_j n_j}$$

## Explanation

Even split over two classes gives $1-(0.25+0.25)=0.5$, the maximum for two classes; four equal classes give $0.75$. With $K$ classes the maximum is $1-1/K$. An empty node has no defined proportions, and `0.0` is returned.
