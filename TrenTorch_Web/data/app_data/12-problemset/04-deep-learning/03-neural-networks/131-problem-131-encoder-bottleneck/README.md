---
name: problem-131-encoder-bottleneck
title: 'Encoder Bottleneck'
tags: [problemset, dl-core, autoencoders]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'autoencoders'
hint: 'compress X with an encoder matrix'
tools: [NumPy]
---

## Statement

Map each input row into an encoded representation with a single affine transform.

### Function signature

```python
def solve(X, W, b):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]], [0, 1])
```

**Output**

```text
[[4, 6], [10, 12]]
```

**Example 2**

**Input**

```python
solve([[1, 1]], [[2], [3]], [1])
```

**Output**

```text
[[6]]
```

## Theory

### Core idea

Multiply the input matrix by the encoder weights and add the bias to each row.

### Contract

`encoded = X @ W + b`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
