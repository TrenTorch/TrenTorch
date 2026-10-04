---
name: problem-129-rnn-sequence-forward
title: "RNN Sequence Forward"
tags: [problemset, dl-core, rnn-basics]
difficulty: Advanced
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "rnn basics"
hint: "carry hidden state across time"
tools: [NumPy]
---

## Statement

Run a vanilla RNN recurrence over all input rows and return each hidden state.

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

Start at `h0`; for each row `x_t`, compute `h_t = tanh(Wx @ x_t + Wh @ h_(t-1) + b)`.

### Contract

The output preserves time order and has one state per input row.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
