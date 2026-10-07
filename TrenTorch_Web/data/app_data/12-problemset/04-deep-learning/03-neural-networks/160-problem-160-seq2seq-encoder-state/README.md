---
name: problem-160-seq2seq-encoder-state
title: 'Seq2Seq Encoder State'
tags: [problemset, sequence-models-attention, seq2seq]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'seq2seq'
hint: 'run the RNN loop and return the last hidden state'
tools: [NumPy]
---

## Statement

Encode a sequence with a vanilla tanh RNN and return only the **final** hidden state. This is the context vector a classic sequence-to-sequence encoder hands to the decoder.

Implement `solve(X, h0, Wx, Wh, b)`.

**Returns.** Return the last hidden state as a NumPy vector.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0]], [0.0], [[1.0]], [[0.5]], [0.0])
```

Output:

```text
[0.983041]
```

**Example 2**

Input:

```python
solve([[0.0], [0.0]], [1.0], [[1.0]], [[0.0]], [0.0])
```

Output:

```text
[0.0]
```

## Theory

### The simple version

A sequence-to-sequence model translates by first _reading_ the whole source sentence into one vector, then _writing_ the target from it. The encoder is an RNN, and the vector it passes on is simply its last hidden state.

### The recurrence

$$h_t=\tanh(W_xx_t+W_hh_{t-1}+b),\qquad c=h_T$$

## Explanation

The loop is the same as in the sequence RNN, but only the last state is kept. Squeezing a long sentence into one fixed-size vector is a bottleneck, which motivated attention. In the second example the recurrent weight is $0$ and the inputs are $0$, so the memory of $h_0=1$ is wiped out immediately and the result is $0$.
