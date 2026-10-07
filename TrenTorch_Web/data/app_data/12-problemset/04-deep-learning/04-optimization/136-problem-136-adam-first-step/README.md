---
name: problem-136-adam-first-step
title: 'Adam First Step'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'update m and v, divide by 1-beta^t, w -= lr*m_hat/(sqrt(v_hat)+eps)'
tools: [NumPy]
---

## Statement

Perform one bias-corrected Adam update. Given weights `w`, gradient `g`, first and second moment estimates `m`, `v` and the step number `t` (starting at 1), update the moments with `beta1` and `beta2`, correct their initialisation bias, and move the weights by `lr * m_hat / (sqrt(v_hat) + eps)`.

Implement `solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08)`.

**Returns.** Return a tuple `(new_w, new_m, new_v)`. Defaults: `lr=0.001`, `beta1=0.9`, `beta2=0.999`, `eps=1e-8`.

### Examples

**Example 1**

Input:

```python
solve([1.0], [1.0], [0.0], [0.0], 1)
```

Output:

```text
([0.999], [0.1], [0.001])
```

**Example 2**

Input:

```python
solve([2.0], [0.0], [0.0], [0.0], 1)
```

Output:

```text
([2.0], [0.0], [0.0])
```

## Theory

### The simple version

Adam keeps two running averages per parameter: the mean of the gradient (like momentum) and the mean of the squared gradient (a measure of its typical size). Dividing the first by the square root of the second gives every parameter a step of a sensible size regardless of how large its gradients are.

### The formulas

$$m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2$$

$$\hat m_t=\frac{m_t}{1-\beta_1^t},\quad \hat v_t=\frac{v_t}{1-\beta_2^t},\quad w_t=w_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\varepsilon}$$

## Explanation

The moments start at zero, so early on they are biased toward zero; dividing by $1-\beta^t$ undoes that. On the very first step $\hat m=g$ and $\hat v=g^2$, so the update is about $\eta\cdot\operatorname{sign}(g)$: in the first example the weight moves from $1$ to $0.999$. A zero gradient (second example) leaves the weights unchanged.
