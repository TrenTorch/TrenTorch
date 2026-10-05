---
name: problem-167-attention-weighted-sum
title: 'Attention Weighted Sum'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'matrix multiply weights by V'
tools: [NumPy]
---

## Statement

Compute the weighted sum of value vectors.

### Function signature

```python
def solve(weights, values):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[0.25, 0.75]], [[2.0, 0.0], [0.0, 4.0]])
```

**Output**

```text
[[0.5, 3.0]]
```

**Example 2**

**Input**

```python
solve([[1.0, 0.0]], [[2.0, 0.0], [0.0, 4.0]])
```

**Output**

```text
[[2.0, 0.0]]
```

## Theory

### Core idea

Multiply the attention-weight matrix by the value matrix; each query row becomes a weighted value representation.

### Contract

`context = weights @ values`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
