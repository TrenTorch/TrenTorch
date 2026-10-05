---
name: problem-151-gradient-accumulation
title: 'Gradient Accumulation'
tags: [problemset, dl-training-theory, batch-dynamics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'batch dynamics'
hint: 'sum gradients and divide by accumulation count'
tools: [NumPy]
---

## Statement

Average a collection of equally shaped micro-batch gradients elementwise.

### Function signature

```python
def solve(grads):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1.0, 3.0], [3.0, 5.0]])
```

**Output**

```text
[2.0, 4.0]
```

**Example 2**

**Input**

```python
solve([[2.0, -2.0], [4.0, 0.0], [6.0, 2.0]])
```

**Output**

```text
[4.0, 0.0]
```

## Theory

### Core idea

Sum each gradient tensor and divide by the number of micro-batches.

### Contract

`g_mean = (g_1 + ... + g_m) / m`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
