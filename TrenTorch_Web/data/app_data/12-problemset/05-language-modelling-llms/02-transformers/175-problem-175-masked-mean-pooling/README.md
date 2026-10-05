---
name: problem-175-masked-mean-pooling
title: 'Masked Mean Pooling'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'sum masked embeddings and divide by valid counts'
tools: [NumPy]
---

## Statement

Mean-pool token embeddings while ignoring masked positions.

### Function signature

```python
def solve(embeddings, mask):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[[1, 3], [3, 1], [9, 9]], [[2, 4], [4, 2], [1, 1]]], [[True, True, False], [False, False, False]])
```

**Output**

```text
[[2.0, 2.0], [0.0, 0.0]]
```

**Example 2**

**Input**

```python
solve([[[2, 4], [6, 8]]], [[False, True]])
```

**Output**

```text
[[6.0, 8.0]]
```

## Theory

### Core idea

For each batch row, average only embeddings whose mask is true; if no positions are selected, return a zero vector.

### Contract

Padding values never contribute to the numerator or count.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
