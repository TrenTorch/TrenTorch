---
name: problem-130-autoencoder-reconstruction
title: 'Autoencoder Reconstruction'
tags: [problemset, dl-core, autoencoders]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'autoencoders'
hint: 'mean squared reconstruction error'
tools: [NumPy]
---

## Statement

Measure reconstruction error using mean squared error over all elements.

### Function signature

```python
def solve(x, recon):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1, 2, 3], [1, 4, 1])
```

**Output**

```text
2.6666666666666665
```

**Example 2**

**Input**

```python
solve([0, 0], [1, -1])
```

**Output**

```text
1.0
```

## Theory

### Core idea

Subtract the reconstruction from the input elementwise, square the differences, and average them.

### Contract

`MSE = mean((x - recon) ** 2)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
