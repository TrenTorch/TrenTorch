---
name: problem-157-lstm-cell
title: 'LSTM Cell'
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn-lstm-gru'
hint: 'gates = W @ concat(x, h) + b; split into i, f, o, g; c’ = sig(f)*c + sig(i)*tanh(g)'
tools: [NumPy]
---

## Statement

Compute one LSTM cell update. The single weight matrix `W` has shape `(4H, d + H)` and acts on the concatenation `[x, h]`; the four resulting gate blocks, each of length $H$, are in the order **input, forget, output, candidate** ($i,f,o,g$). The bias `b` has length $4H$.

Implement `solve(x, h, c, W, b)`.

**Returns.** Return a tuple `(h_new, c_new)` with $c_{new}=\sigma(f)\odot c+\sigma(i)\odot\tanh(g)$ and $h_{new}=\sigma(o)\odot\tanh(c_{new})$.

### Examples

**Example 1**

Input:

```python
solve([1.0], [0.0], [0.0], np.zeros((4, 2)), np.zeros(4))
```

Output:

```text
([0.0], [0.0])
```

**Example 2**

Input:

```python
solve([0.0], [0.0], [2.0], np.zeros((4, 2)), [0.0, 4.0, 4.0, 0.0])
```

Output:

```text
([0.944104], [1.964028])
```

## Theory

### The simple version

An LSTM adds a separate memory cell $c$ to the RNN and protects it with three gates, each a number between 0 and 1: the _forget_ gate decides how much old memory to keep, the _input_ gate decides how much new information to write, and the _output_ gate decides how much of the memory to reveal as the hidden state. This lets gradients flow over long spans.

### The formulas

$$\begin{aligned}[i,f,o,g]&=W[x,h]+b\\ c'&=\sigma(f)\odot c+\sigma(i)\odot\tanh(g)\\ h'&=\sigma(o)\odot\tanh(c')\end{aligned}$$

### Why it matters

- The LSTM's gated memory carries information over long spans without the gradient vanishing.
- Each gate is a number between 0 and 1 that opens or closes a flow.

### How it works

1. Gates $=W[x,h]+b$, split into $i,f,o,g$.
2. $c'=\sigma(f)c+\sigma(i)\tanh(g)$.
3. $h'=\sigma(o)\tanh(c')$.

### Worked example

With zero weights and bias every gate is $\sigma(0)=0.5$ and the candidate $\tanh(0)=0$, so $c'=0.5\cdot0+0.5\cdot0=0$ and $h'=0$: ([0.0], [0.0]).

## Explanation

With all-zero weights and biases every gate is $\sigma(0)=0.5$ and the candidate is $\tanh(0)=0$, so a zero state stays zero (first example). In the second example the forget and output gates are almost fully open ($\sigma(4)\approx0.98$) and the input gate is half-open with a zero candidate, so the old memory $2$ passes through almost intact: $c'\approx1.96$.
