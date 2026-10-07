---
name: problem-49-logistic-sigmoid
title: 'Logistic Sigmoid'
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'logistic regression'
hint: 'use 1/(1+exp(-x)) for x>=0 and exp(x)/(1+exp(x)) for x<0'
tools: [NumPy]
---

## Statement

Compute the logistic sigmoid $\sigma(x)=1/(1+e^{-x})$ for an array of real logits **without overflow** for large positive or negative inputs.

Implement `solve(x)`.

**Returns.** Return a float NumPy array of the same shape with values in $[0, 1]$.

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
solve([1000.0, -1000.0])
```

Output:

```text
[1.0, 0.0]
```

## Theory

### The simple version

The sigmoid squashes any real number into $(0,1)$ so it can be read as a probability. The textbook formula breaks for very negative $x$: $e^{-x}$ overflows to infinity. The fix is to use a different but equal expression depending on the sign of $x$.

### The formula

$$\sigma(x)=\begin{cases}\dfrac1{1+e^{-x}}&x\ge0\\[2mm]\dfrac{e^{x}}{1+e^{x}}&x<0\end{cases}$$

## Explanation

Each branch only ever exponentiates a non-positive number, so $e^{\cdot}\le1$ and nothing overflows. The two branches are algebraically identical; the split exists purely for floating-point safety. Very large $|x|$ saturates cleanly to $1$ or $0$.
