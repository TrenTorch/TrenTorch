---
name: problem-161-teacher-forcing-step
title: 'Teacher Forcing Step'
tags: [problemset, sequence-models-attention, teacher-forcing]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'teacher forcing'
hint: 'sample or use a deterministic threshold'
tools: [NumPy]
---

## Statement

Choose the next sequence input using teacher forcing.

### Function signature

```python
def solve(target, predicted, use_target):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1, 2, 3], [0, 1, 2], True)
```

**Output**

```text
[1, 2, 3]
```

**Example 2**

**Input**

```python
solve([1, 2, 3], [0, 1, 2], False)
```

**Output**

```text
[0, 1, 2]
```

## Theory

### Core idea

Return `target` when `use_target` is true; otherwise return `predicted`.

### Contract

The selector does not transform either candidate.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
