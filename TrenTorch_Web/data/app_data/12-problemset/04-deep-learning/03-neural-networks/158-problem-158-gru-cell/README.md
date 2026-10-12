---
name: problem-158-gru-cell
title: 'GRU Cell'
tags: [problemset, sequence-models-attention, rnn-lstm-gru]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn-lstm-gru'
hint: 'r,z = sigmoid(W@[x,h]+b); cand = tanh(Wh@[x, r*h]+bh); (1-z)*h + z*cand'
tools: [NumPy]
---

## Statement

Compute one GRU update. `W` has shape `(2H, d + H)` and produces the reset and update gates (in that order) from `[x, h]` plus the bias `b`; `Wh` has shape `(H, d + H)` and, together with the bias `bh`, produces the candidate state from `[x, r ⊙ h]`. The new state is $(1-z)\odot h+z\odot\tilde h$.

Implement `solve(x, h, W, b, Wh, bh)`.

**Returns.** Return the new hidden state as a NumPy vector of length $H$.

### Examples

**Example 1**

Input:

```python
solve([1.0], [2.0], np.zeros((2, 2)), [0.0, 0.0], np.zeros((1, 2)), [0.0])
```

Output:

```text
[1.0]
```

**Example 2**

Input:

```python
solve([0.0], [0.0], np.zeros((2, 2)), [0.0, 0.0], np.zeros((1, 2)), [0.0])
```

Output:

```text
[0.0]
```

## Theory

### The simple version

A GRU is a lighter alternative to the LSTM with no separate memory cell. The _reset_ gate decides how much of the old state to use when proposing a new candidate, and the _update_ gate decides how much to blend that candidate into the old state. A gate near 0 keeps the old state, near 1 replaces it.

### The formulas

$$\begin{aligned}[r,z]&=\sigma\big(W[x,h]+b\big)\\ \tilde h&=\tanh\big(W_h[x,\,r\odot h]+b_h\big)\\ h'&=(1-z)\odot h+z\odot\tilde h\end{aligned}$$

### Why it matters

- The GRU is a lighter alternative to the LSTM without a separate cell.
- Its update gate blends the old state with a new candidate.

### How it works

1. Reset and update gates from $[x,h]$.
2. Candidate $\tanh(W_h[x,r\odot h]+b_h)$.
3. $h'=(1-z)h+z\tilde h$.

### Worked example

With zero weights the gates are $0.5$ and the candidate is $0$, so $h'=0.5\cdot2+0.5\cdot0=[1.0]$.

## Explanation

With zero weights the gates are $\sigma(0)=0.5$ and the candidate is $\tanh(0)=0$, so the new state is half of the old one: $0.5\cdot2=1$ in the first example. A zero state stays zero (second example).
