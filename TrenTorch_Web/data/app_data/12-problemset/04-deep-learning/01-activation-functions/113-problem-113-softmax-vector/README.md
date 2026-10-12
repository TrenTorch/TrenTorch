---
name: problem-113-softmax-vector
title: 'Softmax Vector'
tags: [problemset, dl-core, activation-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'exp(x - max(x)) divided by its sum'
tools: [NumPy]
---

## Statement

Convert a one-dimensional vector of logits into probabilities with the softmax function, computed stably by subtracting the maximum first.

Implement `solve(x)`.

**Returns.** Return a float NumPy vector of the same length whose entries are positive and sum to 1.

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3])
```

Output:

```text
[0.090031, 0.244728, 0.665241]
```

**Example 2**

Input:

```python
solve([0, 0])
```

Output:

```text
[0.5, 0.5]
```

**Example 3**

Input:

```python
solve([1000.0, 1000.0, 999.0])
```

Output:

```text
[0.422319, 0.422319, 0.155362]
```

## Theory

### The simple version

Softmax turns arbitrary scores into a probability distribution: bigger scores get bigger probabilities, and the probabilities add up to 1. It is the output layer of multi-class classifiers and the core of attention.

### The formula

$$\operatorname{softmax}(x)_i=\frac{e^{x_i-m}}{\sum_j e^{x_j-m}},\qquad m=\max_j x_j$$

### Why it matters

- Softmax turns arbitrary scores into a probability distribution.
- Subtracting the maximum first keeps the exponentials from overflowing.

### How it works

1. Subtract the maximum.
2. Exponentiate.
3. Divide by the sum.

### Worked example

For $(1,2,3)$ after subtracting $3$ we get $(-2,-1,0)$ and the exponentials are $0.1353,\,0.3679,\,1$ with sum $1.5032$. Dividing gives [0.090031, 0.244728, 0.665241].

## Explanation

Subtracting $m$ does not change the result (the factor $e^{-m}$ cancels) but keeps every exponent $\le0$, so large logits like $1000$ do not overflow to infinity. The third example would produce `nan` without the shift.
