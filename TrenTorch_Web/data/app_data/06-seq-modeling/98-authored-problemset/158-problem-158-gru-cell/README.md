---
name: problem-158-gru-cell
title: "GRU Cell"
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Advanced
kind: problemset
relatedModule: "part-seq-modeling|Neural Networks"
topic: "rnn-lstm-gru"
hint: "compute update and reset gates"
tools: [NumPy]
---

## Statement

Apply one GRU update and return its new hidden state.

### Function signature

```python
def solve(x, h, W, b, Wh, bh):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0], [2.0], np.zeros((2, 2)), [0.0, 0.0], np.zeros((1, 2)), [0.0])
```

**Output**

```text
[1.0]
```

**Example 2**

**Input**

```python
solve([0.0], [0.0], np.zeros((2, 2)), [0.0, 0.0], np.zeros((1, 2)), [0.0])
```

**Output**

```text
[0.0]
```

## Theory

### Core idea

Compute reset and update gates, form the candidate state from the reset-modulated old state, and interpolate between old and candidate states.

### Contract

The update gate controls how much of the candidate replaces the previous hidden state.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
