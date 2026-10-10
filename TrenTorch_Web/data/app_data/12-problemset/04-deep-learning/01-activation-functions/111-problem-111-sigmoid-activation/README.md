---
name: problem-111-sigmoid-activation
title: 'Sigmoid Activation'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: '1/(1+exp(-x)) for x>=0, exp(x)/(1+exp(x)) for x<0'
tools: [NumPy]
---

## Statement

Apply the logistic sigmoid $1/(1+e^{-x})$ element-wise to an array of logits without overflowing for large positive or negative values.

Implement `solve(x)`.

**Returns.** Return a float NumPy array of the same shape with values in $[0,1]$.

### Examples

**Example 1**

Input:

```python
solve([0.0])
```

Output:

```text
[0.5]
```

**Example 2**

Input:

```python
solve([2.0, -2.0])
```

Output:

```text
[0.880797, 0.119203]
```

**Example 3**

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

The sigmoid squashes any real number into $(0,1)$, which can be read as a probability. It is the output activation for binary classification and the gating function inside LSTMs and GRUs.

### The stable formula

$$\sigma(x)=\begin{cases}\dfrac1{1+e^{-x}}&x\ge0\\[2mm]\dfrac{e^{x}}{1+e^{x}}&x<0\end{cases}$$

### Why it matters

- The sigmoid turns scores into probabilities.
- Both branches avoid overflowing exponentials.

### How it works

1. For $x\ge0$ use $1/(1+e^{-x})$.
2. For $x<0$ use $e^x/(1+e^x)$.

### Worked example

At $0$: $1/(1+1)=[0.5]$. At large positive inputs it tends to $1$ and at large negative ones to $0$.

## Explanation

Only a non-positive number is ever exponentiated, so `exp` cannot overflow; for very large $|x|$ the result simply saturates at $1$ or $0$. $\sigma(0)=0.5$ and $\sigma(-x)=1-\sigma(x)$.
