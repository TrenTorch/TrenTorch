---
name: problem-70-entropy-impurity
title: 'Entropy Impurity'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'normalise counts, drop zeros, then minus the sum of p*log2(p)'
tools: [NumPy]
---

## Statement

Compute the entropy, in bits, of a node from its class counts.

Implement `solve(counts)`.

**Returns.** Return a non-negative float. Classes with zero count contribute nothing, and a node with no samples at all has entropy `0.0`.

### Examples

**Example 1**

Input:

```python
solve([3, 1])
```

Output:

```text
0.811278
```

**Example 2**

Input:

```python
solve([2, 2])
```

Output:

```text
1.0
```

**Example 3**

Input:

```python
solve([4, 0])
```

Output:

```text
0.0
```

## Theory

### The simple version

Entropy measures how unpredictable the class of a random item from the node is. It is 0 for a pure node and largest when all classes are equally common. Decision trees choose the split that reduces entropy the most (the information gain).

### The formula

$$H=-\sum_k p_k\log_2 p_k,\qquad p_k=\frac{n_k}{\sum_j n_j}$$

## Explanation

Zero-count classes are dropped before taking the logarithm because $0\log0$ is taken as $0$. Proportions $[0.75,0.25]$ give about $0.811$ bits and $[0.5,0.5]$ give exactly $1$ bit.
