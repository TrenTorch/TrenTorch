---
name: problem-172-positional-encoding
title: 'Positional Encoding'
tags: [problemset, sequence-models-attention, positional-encoding]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'positional encoding'
hint: 'use sine on even dimensions and cosine on odd'
tools: [NumPy]
---

## Statement

Construct sinusoidal positional encodings.

### Function signature

```python
def solve(n, dim):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(2, 4)
```

**Output**

```text
[[0.0, 1.0, 0.0, 1.0], [0.84147098, 0.54030231, 0.00999983, 0.99995]]
```

**Example 2**

**Input**

```python
solve(1, 2)
```

**Output**

```text
[[0.0, 1.0]]
```

## Theory

### Core idea

For position `p` and dimension pair index `i`, use sine on even dimensions and cosine on odd dimensions with the standard `10000` frequency scale.

### Contract

The returned matrix has `n` rows and `dim` columns.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
