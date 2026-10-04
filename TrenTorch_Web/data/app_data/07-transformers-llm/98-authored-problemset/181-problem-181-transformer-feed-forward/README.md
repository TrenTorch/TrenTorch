---
name: problem-181-transformer-feed-forward
title: "Transformer Feed-Forward"
tags: [problemset, transformer-llm, transformer-architecture]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "transformer architecture"
hint: "apply activation between projections"
tools: [NumPy]
---

## Statement

Apply a two-layer position-wise feed-forward network with ReLU.

### Function signature

```python
def solve(x, W1, b1, W2, b2):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1.0, 2.0]], np.eye(2), [0.0, 0.0], np.eye(2), [0.0, 0.0])
```

**Output**

```text
[[1.0, 2.0]]
```

**Example 2**

**Input**

```python
solve([[-1.0, 2.0]], np.eye(2), [0.0, 0.0], np.eye(2), [1.0, -1.0])
```

**Output**

```text
[[1.0, 1.0]]
```

## Theory

### Core idea

Compute `max(0, x @ W1 + b1)` and project the hidden activations through `W2` with output bias `b2`.

### Contract

The final layer is linear; ReLU is applied only between the two affine transforms.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
