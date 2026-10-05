---
name: problem-169-attention-padding-mask
title: 'Attention Padding Mask'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'broadcast a boolean mask over query positions'
tools: [NumPy]
---

## Statement

Mark non-padding token IDs as allowed by the attention mask.

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
[True, False, True]
```

**Example 2**

**Input**

```python
solve([0, 0], 0)
```

**Output**

```text
[False, False]
```

## Theory

### Core idea

Compare every token ID with `pad_id`; non-padding positions are true and padding positions false.

### Contract

The result is a boolean array.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
