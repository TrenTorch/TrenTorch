---
name: problem-159-bidirectional-rnn-merge
title: 'Bidirectional RNN Merge'
tags: [problemset, sequence-models-attention, bidirectional-rnns]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'bidirectional rnns'
hint: 'concatenate states at each position'
tools: [NumPy]
---

## Statement

Merge forward and backward RNN states along the feature axis.

### Function signature

```python
def solve(forward, backward):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1, 2], [3, 4]], [[5, 6], [7, 8]])
```

**Output**

```text
[[1, 2, 5, 6], [3, 4, 7, 8]]
```

**Example 2**

**Input**

```python
solve([[1, 2]], [[3, 4]])
```

**Output**

```text
[[1, 2, 3, 4]]
```

## Theory

### Core idea

The forward and backward arrays must have matching leading dimensions; concatenate their final axes.

### Contract

For each time step, the merged feature vector contains forward features followed by backward features.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
