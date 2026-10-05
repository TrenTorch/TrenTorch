---
name: problem-170-sequence-padding
title: 'Sequence Padding'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'truncate first, then append pad tokens'
tools: [NumPy]
---

## Statement

Right-pad variable-length sequences and return their original lengths.

### Function signature

```python
def solve(sequences, pad_value=0):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1, 2, 3], [4]], 0)
```

**Output**

```text
([[1, 2, 3], [4, 0, 0]], [3, 1])
```

**Example 2**

**Input**

```python
solve([[], [7, 8]], -1)
```

**Output**

```text
([[-1, -1], [7, 8]], [0, 2])
```

## Theory

### Core idea

Use the longest input sequence as the output width, append `pad_value` on the right, and report each input length.

### Contract

An empty sequence has length zero and receives only padding.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
