---
name: problem-135-momentum-update
title: 'Momentum Update'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'v=mu*v+grad; w-=lr*v'
tools: [NumPy]
---

## Statement

Perform one momentum update and return the updated velocity and parameters.

### Function signature

```python
def solve(w, v, grad, lr, mu):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0], [0.0], [2.0], 0.1, 0.9)
```

**Output**

```text
([2.0], [0.8])
```

**Example 2**

**Input**

```python
solve([0.92], [2.0], [-1.0], 0.1, 0.9)
```

**Output**

```text
([0.8], [0.84])
```

## Theory

### Core idea

First update velocity using the momentum coefficient, then subtract the learning-rate-scaled new velocity from the parameters.

### Contract

`v_new = mu * v + grad`; `w_new = w - lr * v_new`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
