---
name: problem-171-sequence-mask
title: "Sequence Mask"
tags: [problemset, sequence-models-attention, sequence-masking]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "sequence masking"
hint: "compare token IDs to pad ID"
tools: [NumPy]
---

## Statement

Create an integer mask for non-padding token IDs.

### Function signature

```python
def solve(ids, pad_id):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([4, 0, 7], 0)
```

**Output**

```text
[1, 0, 1]
```

**Example 2**

**Input**

```python
solve([0, 0, 1], 0)
```

**Output**

```text
[0, 0, 1]
```

## Theory

### Core idea

Return one where an ID differs from `pad_id`, and zero where it matches.

### Contract

This mask is integer-valued, unlike the boolean attention-padding mask.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
