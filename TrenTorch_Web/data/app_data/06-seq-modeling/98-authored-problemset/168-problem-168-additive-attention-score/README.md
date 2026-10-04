---
name: problem-168-additive-attention-score
title: "Additive Attention Score"
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "attention mechanism"
hint: "apply tanh to a learned projection sum"
tools: [NumPy]
---

## Statement

Compute additive-attention scores for one query against a set of keys.

### Function signature

```python
def solve(query, keys, Wq, Wk, v):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], np.eye(2), np.eye(2), [1.0, 1.0])
```

**Output**

```text
[0.96402758, 1.52318831]
```

**Example 2**

**Input**

```python
solve([0.0, 0.0], [[0.0, 0.0]], np.eye(2), np.eye(2), [1.0, 1.0])
```

**Output**

```text
[0.0]
```

## Theory

### Core idea

Project the query with `Wq` and keys with `Wk`, apply tanh to each combined hidden vector, then project with vector `v`.

### Contract

`score_j = vᵀ tanh(query Wq + key_j Wk)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
