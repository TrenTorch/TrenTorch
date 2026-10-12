---
name: problem-50-binary-cross-entropy
title: 'Binary Cross-Entropy'
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'logistic regression'
hint: 'max(z,0) - z*y + log1p(exp(-|z|)), averaged'
tools: [NumPy]
---

## Statement

Compute the mean binary cross-entropy from real-valued logits and 0/1 labels using a numerically stable formula that never evaluates the sigmoid directly.

Implement `solve(logits, labels)`.

**Returns.** Return a non-negative Python float. Very large logits must not overflow.

### Examples

**Example 1**

Input:

```python
solve([0.0, 0.0], [1.0, 0.0])
```

Output:

```text
0.693147
```

**Example 2**

Input:

```python
solve([2.0, -2.0, 1000.0], [1.0, 0.0, 1.0])
```

Output:

```text
0.084619
```

## Theory

### The simple version

Cross-entropy punishes a model for assigning low probability to what actually happened. Written naively as $-y\log\sigma(z)-(1-y)\log(1-\sigma(z))$ it breaks when $\sigma(z)$ rounds to exactly 0 or 1. Rearranging in terms of the raw logit $z$ avoids that.

### The stable form

$$\ell(z,y)=\max(z,0)-zy+\log\!\big(1+e^{-|z|}\big),\qquad \text{BCE}=\frac1n\sum_i\ell(z_i,y_i)$$

### Why it matters

- Cross-entropy is the loss for classification: it punishes confident wrong answers very hard.
- Working from logits keeps it finite even for huge logits.

### How it works

1. For each sample compute $\max(z,0)-zy+\log(1+e^{-|z|})$.
2. Average over samples.

### Worked example

With logits $0,0$ and labels $1,0$ each term is $0-0+\log(1+e^0)=\log2=0.6931$ (the model is unsure, so it pays $\log2$ either way), and the mean is 0.693147.

## Explanation

The identity is exact: it equals the textbook loss but only exponentiates $-|z|\le0$, so it cannot overflow, and `log1p` keeps precision when $e^{-|z|}$ is tiny. A correct, confident prediction such as logit $1000$ with label $1$ costs essentially $0$.
