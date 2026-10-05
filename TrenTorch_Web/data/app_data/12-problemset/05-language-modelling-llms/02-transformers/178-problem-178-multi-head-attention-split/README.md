---
name: problem-178-multi-head-attention-split
title: 'Multi-Head Attention Split'
tags: [problemset, transformer-llm, multi-head-attention]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'multi-head attention'
hint: 'reshape and transpose to head-major form'
tools: [NumPy]
---

## Statement

Split feature channels into multiple attention heads.

### Function signature

```python
def solve(X, n_heads):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[[1, 2, 3, 4], [5, 6, 7, 8]]], 2)
```

**Output**

```text
[[[[1, 2], [5, 6]], [[3, 4], [7, 8]]]]
```

**Example 2**

**Input**

```python
solve([[[1, 2, 3, 4]]], 1)
```

**Output**

```text
[[[[1, 2, 3, 4]]]]
```

## Theory

### Core idea

Reshape `(batch, time, features)` into head groups and transpose to `(batch, heads, time, head_features)`.

### Contract

The feature dimension must be divisible by the positive head count.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
