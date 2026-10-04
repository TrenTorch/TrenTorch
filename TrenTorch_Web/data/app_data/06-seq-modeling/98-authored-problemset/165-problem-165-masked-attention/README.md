---
name: problem-165-masked-attention
title: "Masked Attention"
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "attention mechanism"
hint: "add -inf above the diagonal before softmax"
tools: [NumPy]
---

## Statement

Compute attention over only the allowed key positions.

### Function signature

```python
def solve(Q, K, V, mask):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 4.0]], [[True, False]])
```

**Output**

```text
[[2.0, 0.0]]
```

**Example 2**

**Input**

```python
solve([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 4.0]], [[False, True]])
```

**Output**

```text
[[0.0, 4.0]]
```

## Theory

### Core idea

Scale query-key dot products, assign zero probability to masked positions, normalize allowed positions, then take the weighted sum of values.

### Contract

The mask uses true for positions that may contribute.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
