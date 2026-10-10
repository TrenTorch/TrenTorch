---
name: sigmoid-logits-company-222
title: 'sigmoid-logits — ByteDance case'
tags: [problemset, classical-ml, logistic-regression, bytedance]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'ByteDance'
hint: '1/(1+exp(-z)) for z>=0, exp(z)/(1+exp(z)) for z<0'
tools: [NumPy]
---

## Statement

ByteDance-inspired binary prediction service produces logits that must be converted into probabilities for downstream decision logic. You need to implement the sigmoid transformation correctly, including large positive and negative inputs.

Convert logits to probabilities with the logistic sigmoid. The implementation must stay finite for very large positive and negative logits.

Implement `solve(z)`.

**Returns.** Return a float NumPy array of the same shape with values in $[0,1]$.

Convert logits to probabilities with the logistic sigmoid. The implementation must stay finite for very large positive and negative logits.

Implement `solve(z)`.

**Returns.** Return a float NumPy array of the same shape with values in $[0,1]$.

### Examples

**Example 1**

Input:

```python
solve([-1, 0, 1])
```

Output:

```text
[0.268941, 0.5, 0.731059]
```

**Example 2**

Input:

```python
solve([800.0, -800.0])
```

Output:

```text
[1.0, 0.0]
```

## Theory

### The simple version

A binary classifier outputs a real number (a logit). The sigmoid squashes it into $(0,1)$ so it can be read as a probability and compared with a decision threshold such as $0.5$.

### The stable formula

$$\sigma(z)=\begin{cases}\dfrac1{1+e^{-z}}&z\ge0\\[2mm]\dfrac{e^{z}}{1+e^{z}}&z<0\end{cases}$$

### Why it matters

- A model outputs unbounded scores (logits); decisions need probabilities between 0 and 1.
- Very large logits make a naive formula overflow, so a stable version is needed.

### How it works

1. For non-negative logits compute $1/(1+e^{-z})$.
2. For negative logits compute $e^z/(1+e^z)$.
3. Both branches only exponentiate a non-positive number.

### Worked example

$\sigma(-1)=e^{-1}/(1+e^{-1})=0.2689$, $\sigma(0)=0.5$ and $\sigma(1)=1/(1+e^{-1})=0.7311$, so the result is [0.268941, 0.5, 0.731059].

## Explanation

Each branch only exponentiates a non-positive number, so nothing overflows; for $|z|$ in the hundreds the result simply saturates at $1$ or $0$ (second example). $\sigma(0)=0.5$ and $\sigma(-z)=1-\sigma(z)$.
