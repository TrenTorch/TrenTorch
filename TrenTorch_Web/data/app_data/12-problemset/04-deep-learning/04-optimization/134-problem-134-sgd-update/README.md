---
name: problem-134-sgd-update
title: 'SGD Update'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'w - lr * grad'
tools: [NumPy]
---

## Statement

Perform one stochastic-gradient-descent update: $w\leftarrow w-\eta\,g$.

Implement `solve(w,grad,lr)`.

**Returns.** Return the updated parameters as a NumPy array (the input is not modified).

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [0.1, 0.2], 0.01)
```

Output:

```text
[0.999, 1.998]
```

**Example 2**

Input:

```python
solve([5.0], [-2.0], 0.5)
```

Output:

```text
[6.0]
```

## Theory

### The simple version

Gradient descent nudges each parameter a small step against its gradient, the direction in which the loss increases fastest. The learning rate $\eta$ sets the step size: too small and training is slow, too large and it overshoots or diverges.

### The formula

$$w_{t+1}=w_t-\eta\,\nabla_wL(w_t)$$

## Explanation

A negative gradient makes the parameter increase (second example: $5-0.5\cdot(-2)=6$). In _stochastic_ gradient descent `grad` is computed from a mini-batch rather than the whole dataset.
