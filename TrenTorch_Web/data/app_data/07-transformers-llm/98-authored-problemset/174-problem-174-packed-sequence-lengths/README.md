---
name: problem-174-packed-sequence-lengths
title: "Packed Sequence Lengths"
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "sequence padding"
hint: "prefix-sum the lengths"
tools: [NumPy]
---

## Statement

Compute exclusive cumulative offsets for packed sequence lengths.

### Function signature

```python
def solve(lengths):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([3, 0, 2])
```

**Output**

```text
[0, 3, 3]
```

**Example 2**

**Input**

```python
solve([1, 4])
```

**Output**

```text
[0, 1]
```

## Theory

### Core idea

The first offset is zero; every later offset is the sum of all preceding lengths.

### Contract

Zero-length rows repeat the preceding offset.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
