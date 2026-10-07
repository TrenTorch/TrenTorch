---
name: problem-112-tanh-activation
title: 'Tanh Activation'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'np.tanh'
tools: [NumPy]
---

## Statement

Apply the hyperbolic tangent activation element-wise.

Implement `solve(x)`.

**Returns.** Return a float NumPy array of the same shape with values in $(-1,1)$.

### Examples

**Example 1**

Input:

```python
solve([-2.0, 0.0, 2.0])
```

Output:

```text
[-0.964028, 0.0, 0.964028]
```

**Example 2**

Input:

```python
solve([20.0, -20.0])
```

Output:

```text
[1.0, -1.0]
```

## Theory

### The simple version

Tanh is a rescaled sigmoid that is centred at zero: it maps large negative inputs to $-1$, zero to $0$ and large positive inputs to $+1$. Zero-centred outputs often make optimisation easier than the sigmoid's $(0,1)$ range, and it is used in RNN and LSTM cells.

### The formula

$$\tanh(x)=\frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}=2\sigma(2x)-1$$

## Explanation

`np.tanh` is already numerically stable, saturating cleanly to $\pm1$ for large inputs (second example). It is an odd function: $\tanh(-x)=-\tanh(x)$.
