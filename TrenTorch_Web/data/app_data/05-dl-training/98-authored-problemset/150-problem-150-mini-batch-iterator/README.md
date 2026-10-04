---
name: problem-150-mini-batch-iterator
title: "Mini-Batch Iterator"
tags: [problemset, dl-training-theory, batch-dynamics]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "batch dynamics"
hint: "permute indices once per epoch"
tools: [NumPy]
---

## Statement

Shuffle examples once with a seed and divide them into mini-batches.

### Function signature

```python
def solve(X, y, batch_size, seed=0):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[0], [1], [2], [3], [4]], [0, 1, 2, 3, 4], 2, seed=0)
```

**Output**

```text
[([[2], [4]], [2, 4]), ([[3], [0]], [3, 0]), ([[1]], [1])]
```

**Example 2**

**Input**

```python
solve([[0], [1], [2], [3]], [0, 1, 2, 3], 3, seed=7)
```

**Output**

```text
[([[0], [2], [1]], [0, 2, 1]), ([[3]], [3])]
```

## Theory

### Core idea

Apply one seeded permutation to feature and label rows together, split into chunks of at most `batch_size`, and retain the final short batch.

### Contract

Each returned item is a pair `(feature_batch, label_batch)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
