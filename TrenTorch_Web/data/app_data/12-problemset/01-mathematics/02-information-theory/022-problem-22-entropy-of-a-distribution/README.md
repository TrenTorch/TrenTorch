---
name: problem-22-entropy-of-a-distribution
title: 'Entropy of a Distribution'
tags: [problemset, maths-stats-for-ml, information-theory]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Information Theory'
topic: 'information theory'
hint: 'drop zero probabilities, then sum minus p times log2 p'
tools: [NumPy]
---

## Statement

Compute the Shannon entropy, in bits, of a discrete probability vector.

Implement `solve(p)`.

**Returns.** Return a float. Entries equal to zero contribute nothing. The input must be a non-empty 1-D vector of non-negative values that sums to 1; otherwise `ValueError` is raised.

### Examples

**Example 1**

Input:

```python
solve([0.5, 0.5])
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve([0.25, 0.25, 0.25, 0.25])
```

Output:

```text
2.0
```

## Theory

### The simple version

Entropy measures how unpredictable a distribution is: the average number of yes/no questions you need to identify the outcome. A fair coin has 1 bit, and a fair four-sided die has 2 bits.

### The formula

$$H(p)=-\sum_i p_i\log_2 p_i,\qquad 0\log_2 0:=0$$

### Why it matters

- Entropy measures how unpredictable a distribution is; it is the basis of cross-entropy losses, information gain and compression limits.
- Working in bits makes the numbers easy to read: a fair coin is exactly one bit.

### How it works

1. Drop zero probabilities (their contribution is $0$).
2. For each remaining $p_i$ compute $p_i\log_2p_i$.
3. Add them up and negate.

### Worked example

For $(0.5,0.5)$: each term is $0.5\log_20.5=-0.5$, the sum is $-1$, and negating gives 1.0 bit.

## Explanation

Zero probabilities are removed before taking the logarithm, because $\log 0$ is undefined and the limit of $p\log p$ as $p\to 0$ is $0$. The base-2 logarithm gives the answer in bits.
