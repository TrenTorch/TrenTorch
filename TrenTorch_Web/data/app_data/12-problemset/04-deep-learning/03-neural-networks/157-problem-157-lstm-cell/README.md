---
name: problem-157-lstm-cell
title: 'LSTM Cell'
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn-lstm-gru'
hint: 'compute four gates and cell state'
tools: [NumPy]
---

## Statement

Apply one LSTM cell update.

### Function signature

```python
def solve(x, h, c, W, b):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([0.5], [0.5], [0.5], np.zeros((4, 2)), [0.0, 0.0, 0.0, 0.0])
```

**Output**

```text
([0.12245933], [0.25])
```

**Example 2**

**Input**

```python
solve([0.0], [0.0], [2.0], np.zeros((4, 2)), [0.0, 0.0, 0.0, 0.0])
```

**Output**

```text
([0.38079708], [1.0])
```

## Theory

### Core idea

Split the affine result into input, forget, output, and candidate gates; update the cell state, then compute the hidden state.

### Contract

`c_new = f * c + i * g`; `h_new = o * tanh(c_new)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
