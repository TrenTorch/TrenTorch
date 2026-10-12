---
name: problem-155-stable-logsumexp
title: 'Stable LogSumExp'
tags: [problemset, dl-training-theory, numerical-stability]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'numerical stability'
hint: 'm + log(sum(exp(x - m))) with m = max(x)'
tools: [NumPy]
---

## Statement

Compute $\log\sum_i e^{x_i}$ for a vector `x` without overflow, even when entries are as large as $1000$.

Implement `solve(x)`.

**Returns.** Return a Python float.

### Examples

**Example 1**

Input:

```python
solve([1000.0, 1001.0])
```

Output:

```text
1001.313262
```

**Example 2**

Input:

```python
solve([0.0, 0.0])
```

Output:

```text
0.693147
```

**Example 3**

Input:

```python
solve([-1000.0, -1000.0])
```

Output:

```text
-999.306853
```

## Theory

### The simple version

LogSumExp is a smooth version of the maximum: it is always slightly above $\max_i x_i$ and approaches it when one entry dominates. It appears inside softmax, cross-entropy and probabilistic models. Computed directly, $e^{1000}$ overflows to infinity and $e^{-1000}$ underflows to zero.

### The stable formula

$$\log\sum_ie^{x_i}=m+\log\sum_ie^{x_i-m},\qquad m=\max_ix_i$$

### Why it matters

- LogSumExp appears inside softmax and cross-entropy.
- Computed naively, $e^{1000}$ overflows.

### How it works

1. $m=\max x$.
2. $m+\log\sum e^{x-m}$.

### Worked example

For $(1000,1001)$: $m=1001$; $e^{-1}+1=1.3679$; $\ln1.3679=0.3133$, so the result is $1001+0.3133=1001.313262$.

## Explanation

After subtracting the maximum, the largest exponent is $0$, so the sum is at least $1$ and no term overflows. In the first example $m=1001$ and the result is $1001+\log(1+e^{-1})\approx1001.313$. Two equal entries $0,0$ give $\log2$.
