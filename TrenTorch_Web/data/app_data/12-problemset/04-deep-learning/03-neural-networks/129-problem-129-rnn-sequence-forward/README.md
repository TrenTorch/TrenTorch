---
name: problem-129-rnn-sequence-forward
title: 'RNN Sequence Forward'
tags: [problemset, dl-core, rnn-basics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn basics'
hint: 'loop over rows: h = tanh(Wx@x + Wh@h + b); collect each h'
tools: [NumPy]
---

## Statement

Run a vanilla RNN over a whole sequence. `X` has one input vector per row; starting from the hidden state `h0`, apply $h_t=\tanh(W_xx_t+W_hh_{t-1}+b)$ for each row in order.

Implement `solve(X, h0, Wx, Wh, b)`.

**Returns.** Return an array of shape `(T, hidden)` whose row $t$ is the hidden state after reading input $t$ (the initial state `h0` is not included).

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
solve([[0.0], [0.0], [0.0]], [1.0], [[1.0]], [[1.0]], [0.0])
```

Output:

```text
[[0.761594], [0.642015], [0.56627]]
```

## Theory

### The simple version

Unrolling an RNN means applying the same step function over and over, feeding each step's output state back in as the next step's memory. The list of all hidden states is what later layers (or a loss at every step) consume.

### The recurrence

$$h_t=\tanh(W_xx_t+W_hh_{t-1}+b),\qquad t=1,\dots,T$$

### Why it matters

- Unrolling the RNN gives a representation for every position.
- Each state depends on all earlier inputs.

### How it works

1. Start from $h_0$.
2. For each input apply the step.
3. Collect the states.

### Worked example

Step 1: $\tanh(1\cdot1+0.5\cdot0)=0.7616$. Step 2: $\tanh(2+0.5\cdot0.7616)=\tanh(2.381)=0.9830$: [[0.761594], [0.983041]].

## Explanation

The state is carried through the loop and a copy of it is stored after every step. With zero input the second example shows pure memory: the state $1$ is pushed through $\tanh$ again and again, giving $0.76, 0.64, 0.57,\dots$, a slowly fading memory.
