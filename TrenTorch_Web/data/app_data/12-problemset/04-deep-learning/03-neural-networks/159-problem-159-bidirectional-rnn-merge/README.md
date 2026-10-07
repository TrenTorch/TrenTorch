---
name: problem-159-bidirectional-rnn-merge
title: 'Bidirectional RNN Merge'
tags: [problemset, sequence-models-attention, bidirectional-rnns]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'bidirectional rnns'
hint: 'np.concatenate((forward, backward), axis=-1)'
tools: [NumPy]
---

## Statement

Merge the outputs of a bidirectional RNN by concatenating the forward and backward hidden states along the last (feature) axis. Both inputs must have the same shape except for the last dimension.

Implement `solve(forward, backward)`.

**Returns.** Return a NumPy array whose last dimension is the sum of the two input feature sizes. Mismatched leading dimensions raise `ValueError`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [[5.0], [6.0]])
```

Output:

```text
[[1.0, 2.0, 5.0], [3.0, 4.0, 6.0]]
```

**Example 2**

Input:

```python
solve([[1.0]], [[2.0]])
```

Output:

```text
[[1.0, 2.0]]
```

## Theory

### The simple version

A normal RNN only knows the past at each position. A bidirectional RNN also runs a second RNN from the end of the sequence backwards, so every position gets context from both sides. The two views are joined by concatenation.

### The formula

$$h_t=[\,\overrightarrow{h_t};\overleftarrow{h_t}\,]\in\mathbb R^{H_f+H_b}$$

## Explanation

The backward states must be aligned with the forward ones (the same time step in the same row) before merging. Concatenation keeps all the information and lets the next layer decide how to combine it; summing or averaging would discard the distinction.
