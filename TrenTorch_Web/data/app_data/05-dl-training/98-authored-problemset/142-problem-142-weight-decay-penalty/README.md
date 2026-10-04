---
name: problem-142-weight-decay-penalty
title: "Weight Decay Penalty"
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "regularization"
hint: "sum squared weights times coefficient"
tools: [NumPy]
---

## Statement

Compute the L2 weight-decay penalty for a parameter array.

### Function signature

```python
def solve(w, lam):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], 0.5)
```

**Output**

```text
2.5
```

**Example 2**

**Input**

```python
solve([0.0, 0.0], 3.0)
```

**Output**

```text
0.0
```

## Theory

### Core idea

Square and sum all parameter values, then multiply by `lam`.

### Contract

`penalty = lam * Σ_i w_i²`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
