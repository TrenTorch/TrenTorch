---
name: problem-136-adam-first-step
title: "Adam First Step"
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "optimizers"
hint: "maintain first and second moments"
tools: [NumPy]
---

## Statement

Perform one bias-corrected Adam update.

### Function signature

```python
def solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0], [1.0], [0.0], [0.0], 1)
```

**Output**

```text
([0.999], [0.1], [0.001])
```

**Example 2**

**Input**

```python
solve([2.0], [0.0], [0.0], [0.0], 1)
```

**Output**

```text
([2.0], [0.0], [0.0])
```

## Theory

### Core idea

Update the first and second moments, correct both for initialization bias at step `t`, and use their ratio for the parameter update.

### Contract

The adaptive step is `m_hat / (sqrt(v_hat) + eps)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
