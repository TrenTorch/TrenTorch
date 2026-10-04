---
name: problem-173-learned-positional-embeddings
title: "Learned Positional Embeddings"
tags: [problemset, sequence-models-attention, positional-encoding]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "positional encoding"
hint: "index an embedding matrix by position"
tools: [NumPy]
---

## Statement

Take the first `length` rows from a learned positional-embedding table.

### Function signature

```python
def solve(embeddings, length):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[0, 0], [1, 1], [2, 2]], 2)
```

**Output**

```text
[[0, 0], [1, 1]]
```

**Example 2**

**Input**

```python
solve([[2, 3], [4, 5]], 1)
```

**Output**

```text
[[2, 3]]
```

## Theory

### Core idea

Positions are selected in their existing order; no interpolation or recomputation is performed.

### Contract

The result is a prefix of the supplied table.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
