---
name: problem-164-scaled-dot-product-attention
title: "Scaled Dot-Product Attention"
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "attention mechanism"
hint: "scores=QKᵀ/sqrt(d); softmax; multiply V"
tools: [NumPy]
---

## Statement

Compute scaled dot-product attention.

### Function signature

```python
def solve(Q, K, V, mask=None):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[0.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 4.0]])
```

**Output**

```text
[[1.0, 2.0]]
```

**Example 2**

**Input**

```python
solve([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 4.0]], [[True, False]])
```

**Output**

```text
[[2.0, 0.0]]
```

## Theory

### Core idea

Form `Q @ K.T / sqrt(d_k)`, optionally exclude mask-false positions, normalize each row with softmax, and multiply by `V`.

### Contract

True mask entries are allowed; an entirely masked row receives zero weights.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
