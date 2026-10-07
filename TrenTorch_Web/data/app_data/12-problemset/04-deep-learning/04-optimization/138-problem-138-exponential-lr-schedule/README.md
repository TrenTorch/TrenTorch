---
name: problem-138-exponential-lr-schedule
title: 'Exponential LR Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'lr0 * gamma ** t'
tools: [NumPy]
---

## Statement

Compute the learning rate after `t` steps under exponential decay: $\eta_t=\eta_0\,\gamma^{t}$, where `lr0` is the initial rate and `gamma` the per-step decay factor.

Implement `solve(lr0,gamma,t)`.

**Returns.** Return the learning rate as a float.

### Examples

**Example 1**

Input:

```python
solve(0.1, 0.9, 5)
```

Output:

```text
0.059049
```

**Example 2**

Input:

```python
solve(1.0, 0.5, 3)
```

Output:

```text
0.125
```

## Theory

### The simple version

Large learning rates make fast progress early; small ones fine-tune near the end. Exponential decay shrinks the rate by the same percentage at every step, so it falls quickly at first and then settles.

### The formula

$$\eta_t=\eta_0\,\gamma^{\,t},\qquad 0<\gamma<1$$

## Explanation

With $\eta_0=1$ and $\gamma=0.5$ the rate halves each step: $1,0.5,0.25,0.125$ (second example, $t=3$). The decay factor is usually very close to $1$ when it is applied per step.
