---
name: problem-137-adamw-decoupled-decay
title: 'AdamW Decoupled Decay'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'apply weight decay directly to parameters'
tools: [NumPy]
---

## Statement

Perform one AdamW update with decoupled weight decay.

### Function signature

```python
def solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08, wd=0.01):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([2.0], [1.0], [0.0], [0.0], 1, lr=0.1, beta1=0.0, beta2=0.0, eps=0.0, wd=0.1)
```

**Output**

```text
([1.88], [1.0], [1.0])
```

**Example 2**

**Input**

```python
solve([1.0], [0.0], [0.0], [0.0], 1, lr=0.1, beta1=0.0, beta2=0.0, eps=0.0, wd=0.1)
```

**Output**

```text
([0.89], [0.0], [0.0])
```

## Theory

### Core idea

Compute the bias-corrected Adam moments; add `wd * w` to the adaptive update before applying the learning rate.

### Contract

`w_new = w - lr * (m_hat / (sqrt(v_hat) + eps) + wd * w)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
