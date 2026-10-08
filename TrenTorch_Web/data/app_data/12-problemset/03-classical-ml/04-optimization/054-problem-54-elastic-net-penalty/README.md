---
name: problem-54-elastic-net-penalty
title: 'Elastic-Net Penalty'
tags: [problemset, classical-ml, regularization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'l1 * sum|w| + 0.5 * l2 * sum(w^2)'
tools: [NumPy]
---

## Statement

Compute the elastic-net penalty of a weight vector: an L1 term with strength `l1` plus an L2 term with strength `l2`, where the L2 term carries a factor $\tfrac12$.

Implement `solve(w,l1,l2)`.

**Returns.** Return a non-negative float $\;l_1\sum_j|w_j|+\tfrac12 l_2\sum_j w_j^2$.

### Examples

**Example 1**

Input:

```python
solve([1.0, -2.0], 0.1, 0.2)
```

Output:

```text
0.8
```

**Example 2**

Input:

```python
solve([0.0, 0.0, 0.0], 1.0, 1.0)
```

Output:

```text
0.0
```

## Theory

### The simple version

Elastic net mixes the two classic penalties. The L1 part encourages exact zeros (feature selection); the L2 part keeps weights small and stable when features are correlated. The two strengths are tuned independently.

### The formula

$$P(w)=\lambda_1\|w\|_1+\frac{\lambda_2}{2}\|w\|_2^2$$

### Why it matters

- Elastic net combines L1 (sparsity) and L2 (stability with correlated features).
- The two strengths can be tuned separately.

### How it works

1. $\lambda_1\sum|w_j|$.
2. $\tfrac12\lambda_2\sum w_j^2$.
3. Add them.

### Worked example

For $w=(1,-2)$: $\sum|w|=3$ and $\sum w^2=5$, so the penalty is $0.1\cdot3+0.5\cdot0.2\cdot5=0.3+0.5=0.8$.

## Explanation

Each term is summed over all weights. In the first example $\|w\|_1=3$ and $\|w\|_2^2=5$, so the penalty is $0.1\cdot3+0.5\cdot0.2\cdot5=0.8$. The all-zero weight vector has zero penalty.
