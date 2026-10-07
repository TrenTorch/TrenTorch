---
name: problem-128-rnn-step
title: 'RNN Step'
tags: [problemset, dl-core, rnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn basics'
hint: 'tanh(Wx @ x + Wh @ h + b)'
tools: [NumPy]
---

## Statement

Compute one step of a vanilla (Elman) RNN: the new hidden state is $h'=\tanh(W_xx+W_hh+b)$ for the input vector `x`, previous hidden state `h`, input weights `Wx`, recurrent weights `Wh` and bias `b`.

Implement `solve(x, h, Wx, Wh, b)`.

**Returns.** Return the new hidden state as a NumPy vector with entries in $(-1,1)$.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [0.0, 1.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0])
```

Output:

```text
[0.761594, 0.995055]
```

**Example 2**

Input:

```python
solve([0.0], [0.0], [[1.0]], [[1.0]], [0.5])
```

Output:

```text
[0.462117]
```

## Theory

### The simple version

A recurrent network reads a sequence one element at a time while carrying a memory, the hidden state. At each step it mixes the current input with the previous memory through two weight matrices and squashes the result with $\tanh$ so the state stays bounded.

### The formula

$$h_t=\tanh(W_xx_t+W_hh_{t-1}+b)$$

## Explanation

The same weights are used at every step, which is what lets the network handle sequences of any length. In the first example the pre-activation is $(1,3)$ and $\tanh$ gives about $(0.76, 0.995)$.
