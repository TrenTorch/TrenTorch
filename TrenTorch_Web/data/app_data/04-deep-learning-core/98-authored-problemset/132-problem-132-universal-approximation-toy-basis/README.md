---
name: problem-132-universal-approximation-toy-basis
title: "Universal Approximation Toy Basis"
tags: [problemset, dl-core, universal-approximation]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "universal approximation"
hint: "solve least squares over basis activations"
tools: [NumPy]
---

## Statement

Fit coefficients for a fixed ReLU hinge basis by least squares.

### Function signature

```python
def solve(X, y, knots):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([0, 1, 2], [0, 1, 2], [0])
```

**Output**

```text
([0, 1, 2], [1])
```

**Example 2**

**Input**

```python
solve([0, 1, 2], [0, 0, 1], [0])
```

**Output**

```text
([0, 0.4, 0.8], [0.4])
```

## Theory

### Core idea

For each sample and knot, form `max(x - knot, 0)`, solve the least-squares system for weights, and return both fitted values and weights.

### Contract

`B[i,j] = max(X[i] - knots[j], 0)` and `w = argmin ||B w - y||₂`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
