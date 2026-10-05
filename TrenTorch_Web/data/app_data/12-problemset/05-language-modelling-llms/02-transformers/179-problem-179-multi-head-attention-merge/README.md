---
name: problem-179-multi-head-attention-merge
title: 'Multi-Head Attention Merge'
tags: [problemset, transformer-llm, multi-head-attention]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'multi-head attention'
hint: 'transpose then reshape'
tools: [NumPy]
---

## Statement

Merge attention heads back into a feature axis.

### Function signature

```python
def solve(heads):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[[[1, 2], [5, 6]], [[3, 4], [7, 8]]]])
```

**Output**

```text
[[[1, 2, 3, 4], [5, 6, 7, 8]]]
```

**Example 2**

**Input**

```python
solve([[[[1], [3]], [[2], [4]]]])
```

**Output**

```text
[[[1, 2], [3, 4]]]
```

## Theory

### Core idea

Transpose `(batch, heads, time, head_features)` to put time before heads, then flatten the head and feature axes.

### Contract

The resulting shape is `(batch, time, heads * head_features)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
