---
name: problem-156-vanilla-rnn-sequence
title: 'Vanilla RNN Sequence'
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn-lstm-gru'
hint: 'loop over the rows, update h with tanh(Wx@x + Wh@h + b), store each h'
tools: [NumPy]
---

## Statement

Run a vanilla tanh RNN over an input sequence and return **every** hidden state. `X` has one input vector per row, `h0` is the initial state, and each step computes $h_t=\tanh(W_xx_t+W_hh_{t-1}+b)$.

Implement `solve(X, h0, Wx, Wh, b)`.

**Returns.** Return an array of shape `(T, hidden)`; the initial state is not included.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0]], [0.0], [[1.0]], [[0.5]], [0.0])
```

Output:

```text
[[0.761594], [0.983041]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0])
```

Output:

```text
[[0.761594, 0.0], [0.0, 0.761594]]
```

## Theory

### The simple version

An RNN processes a sequence one element at a time while carrying a hidden state that summarises everything seen so far. Collecting the hidden state at every step gives one feature vector per position, which is what tagging models and attention over RNN outputs use.

### The recurrence

$$h_t=\tanh(W_xx_t+W_hh_{t-1}+b)$$

### Why it matters

- Every position gets a state summarising what came before.
- That is what tagging and attention over RNN outputs use.

### How it works

1. Start from $h_0$.
2. Apply the tanh step to each input.
3. Store each state.

### Worked example

$\tanh(1+0.5\cdot0)=0.7616$, then $\tanh(2+0.5\cdot0.7616)=0.9830$: [[0.761594], [0.983041]].

## Explanation

The loop feeds the previous state back in at each step and stores a copy of the new one. In the second example the recurrent matrix is zero, so each state depends on the current input only and the result is $\tanh$ of the identity mapping.
