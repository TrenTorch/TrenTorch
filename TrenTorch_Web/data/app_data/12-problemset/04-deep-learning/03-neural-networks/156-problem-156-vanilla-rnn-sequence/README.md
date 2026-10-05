---
name: problem-156-vanilla-rnn-sequence
title: 'Vanilla RNN Sequence'
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn-lstm-gru'
hint: 'recur over time'
tools: [NumPy]
---

## Statement

Run a vanilla RNN over a sequence and return every hidden state.

### Function signature

```python
def solve(X, h0, Wx, Wh, b):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1.0], [2.0]], [0.0], [[1.0]], [[0.5]], [0.0])
```

**Output**

```text
[[0.76159416], [0.9830411]]
```

**Example 2**

**Input**

```python
solve([[0.0], [0.0]], [1.0], [[1.0]], [[0.0]], [0.0])
```

**Output**

```text
[[0.76159416], [0.76159416]]
```

## Theory

### Core idea

Apply the same tanh recurrence in input order, starting from `h0`.

### Contract

The result has one row per time step; it differs from an encoder summary by retaining intermediate states.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
