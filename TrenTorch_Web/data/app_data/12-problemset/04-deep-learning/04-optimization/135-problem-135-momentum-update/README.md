---
name: problem-135-momentum-update
title: 'Momentum Update'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'v = mu*v + grad; w = w - lr*v; return (v, w)'
tools: [NumPy]
---

## Statement

Perform one SGD-with-momentum update using the (PyTorch-style) rule $v\leftarrow\mu v+g$, then $w\leftarrow w-\eta v$.

Implement `solve(w, v, grad, lr, mu)`.

**Returns.** Return a tuple `(new_velocity, new_weights)`.

### Examples

**Example 1**

Input:

```python
solve([1.0], [0.0], [2.0], 0.1, 0.9)
```

Output:

```text
([2.0], [0.8])
```

**Example 2**

Input:

```python
solve([0.92], [2.0], [-1.0], 0.1, 0.9)
```

Output:

```text
([0.8], [0.84])
```

## Theory

### The simple version

Momentum remembers the direction the weights have recently been moving and keeps pushing that way, like a ball rolling downhill. It smooths out noisy gradients and speeds up travel along long, shallow valleys.

### The formulas

$$v_{t+1}=\mu v_t+g_t,\qquad w_{t+1}=w_t-\eta\,v_{t+1}$$

## Explanation

With $\mu=0$ this is plain SGD. In the second example the old velocity $2$ is decayed to $1.8$, then the new gradient $-1$ is added to give $0.8$, so the weight moves by $-0.08$. The velocity is returned together with the weights because it must be fed into the next step.
