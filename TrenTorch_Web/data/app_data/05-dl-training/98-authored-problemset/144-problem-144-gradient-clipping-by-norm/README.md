---
name: problem-144-gradient-clipping-by-norm
title: "Gradient Clipping by Norm"
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "gradient stability"
hint: "multiply all gradients by clip_norm/norm"
tools: [NumPy]
---

## Statement

Clip a collection of gradients by their global L2 norm.

### Function signature

```python
def solve(grads, clip):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[3.0, 4.0], [0.0, 0.0]], 2.0)
```

**Output**

```text
[[1.2, 1.6], [0.0, 0.0]]
```

**Example 2**

**Input**

```python
solve([[1.0, 2.0]], 5.0)
```

**Output**

```text
[[1.0, 2.0]]
```

## Theory

### Core idea

Compute one norm across every gradient tensor. If it exceeds `clip`, scale all tensors by the same factor.

### Contract

`scale = min(1, clip / ||g||₂)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
