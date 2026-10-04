---
name: problem-134-sgd-update
title: "SGD Update"
tags: [problemset, dl-training-theory, optimizers]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "optimizers"
hint: "w -= lr*grad"
tools: [NumPy]
---

## Statement

Perform one stochastic-gradient-descent parameter update.

### Function signature

```python
def solve(w, grad, lr):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], [0.5, -1.0], 0.1)
```

**Output**

```text
[0.95, 2.1]
```

**Example 2**

**Input**

```python
solve([0.0], [2.0], 0.25)
```

**Output**

```text
[-0.5]
```

## Theory

### Core idea

Subtract the learning-rate-scaled gradient from the current parameter values.

### Contract

`w_new = w - lr * grad`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
