---
name: sgd-update-company-216
title: 'sgd-update — Snowflake case'
tags: [problemset, dl-training-theory, optimizers, snowflake]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Snowflake'
hint: 'theta - lr * grad'
tools: [NumPy]
---

## Statement

Snowflake-inspired ML platform team is validating a small optimizer implementation before using it inside a larger training workflow. You need to compute one exact SGD parameter update from the current parameters, learning rate, and gradients.

Compute one gradient-descent step: $\theta\leftarrow\theta-\eta\,g$.

Implement `solve(theta,grad,lr)`.

**Returns.** Return a NumPy array with the updated parameters; the inputs are not modified.

Compute one gradient-descent step: $\theta\leftarrow\theta-\eta\,g$.

Implement `solve(theta,grad,lr)`.

**Returns.** Return a NumPy array with the updated parameters; the inputs are not modified.

### Examples

**Example 1**

Input:

```python
solve([1, 2], [0.5, -1], 0.1)
```

Output:

```text
[0.95, 2.1]
```

**Example 2**

Input:

```python
solve([0.0], [10.0], 0.01)
```

Output:

```text
[-0.1]
```

## Theory

### The simple version

The gradient points in the direction in which the loss increases fastest, so stepping the opposite way lowers it. The learning rate $\eta$ is the step length. SGD applies this rule with a gradient estimated from a mini-batch.

### The formula

$$\theta_{t+1}=\theta_t-\eta\,\nabla_\theta L(\theta_t)$$

### Why it matters

- Every optimiser is a variation of this one update, so it is the baseline to understand first.
- Checking one exact step against a hand calculation is how you validate a training loop before running a long experiment.

### How it works

1. Multiply the gradient by the learning rate.
2. Subtract the result from the parameters, because the gradient points uphill.

### Worked example

With $\theta=(1,2)$, $g=(0.5,-1)$ and $\eta=0.1$ the step is $0.1\cdot(0.5,-1)=(0.05,-0.1)$. Subtracting gives $(1-0.05,\;2+0.1)=[0.95, 2.1]$.

## Explanation

A positive gradient pushes the parameter down and a negative gradient pushes it up: in the first example $1-0.1\cdot0.5=0.95$ and $2-0.1\cdot(-1)=2.1$. Doubling $\eta$ doubles the step.
