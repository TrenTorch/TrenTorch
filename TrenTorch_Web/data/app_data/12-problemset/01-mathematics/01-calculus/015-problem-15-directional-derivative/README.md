---
name: problem-15-directional-derivative
title: 'Directional Derivative'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'normalize the direction, then take the dot product with the gradient'
tools: [NumPy]
---

## Statement

Compute the directional derivative of a scalar function at a point, given the gradient there and a direction. The direction does not need to have length 1.

Implement `solve(grad, direction)`.

**Returns.** Return a float. A zero direction vector has no direction, so the result is `nan`.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0], [1.0, 0.0])
```

Output:

```text
3.0
```

**Example 2**

Input:

```python
solve([3.0, 4.0], [3.0, 4.0])
```

Output:

```text
5.0
```

## Theory

### The simple version

The directional derivative is the rate of change of the function when you move along a chosen direction. It is the part of the gradient that points that way.

### The formula

$$D_u f=\nabla f\cdot\frac{d}{\|d\|_2}$$

### Why it matters

- The directional derivative tells you how fast the function changes along any chosen direction, not just along the axes.
- It is the slope you feel when you step in that direction, which is how line searches and sensitivity analyses work.

### How it works

1. Normalise the direction to unit length (a zero direction gives `nan`).
2. Take the dot product of the gradient with that unit vector.

### Worked example

The gradient is $(3,4)$ and the direction is $(1,0)$, already of length $1$. The dot product is $3\cdot1+4\cdot0=3.0$: moving along the first axis changes the function at rate $3$.

## Explanation

The direction is normalized to unit length first. Without that step, doubling the direction vector would double the answer, which is not what a derivative along a direction means.
