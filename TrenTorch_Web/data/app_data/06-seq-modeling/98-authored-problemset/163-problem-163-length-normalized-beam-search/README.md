---
name: problem-163-length-normalized-beam-search
title: "Length-Normalized Beam Search"
tags: [problemset, sequence-models-attention, beam-search]
difficulty: Intermediate
kind: problemset
relatedModule: "part-seq-modeling|Neural Networks"
topic: "beam search"
hint: "divide score by length^alpha"
tools: [NumPy]
---

## Statement

Select the beam with the best length-normalized score.

### Function signature

```python
def solve(beams, alpha):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([([1, 2], -3.0), ([3], -1.0)], 1.0)
```

**Output**

```text
([3], -1.0)
```

**Example 2**

**Input**

```python
solve([([1, 2], -3.0), ([3], -1.0)], 0.0)
```

**Output**

```text
([3], -1.0)
```

## Theory

### Core idea

For each `(sequence, score)`, divide the score by `len(sequence) ** alpha` and return the maximizing pair.

### Contract

The returned value is one of the supplied beam records.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
