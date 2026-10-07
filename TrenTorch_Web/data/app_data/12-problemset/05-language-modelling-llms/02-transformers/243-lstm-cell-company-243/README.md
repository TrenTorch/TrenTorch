---
name: lstm-cell-company-243
title: 'lstm-cell — Lyft case'
tags: [problemset, sequence-models-attention, rnn-lstm-gru, lyft]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Lyft'
hint: 'c = f*c_prev + i*g; h = o*tanh(c)'
tools: [NumPy]
---

## Statement

Lyft-inspired ETA model processes a sequence of trip events with a compact recurrent unit. You need to perform one LSTM cell update from the already-activated input, forget and output gates, the candidate values and the previous cell state.

Compute one LSTM cell update from **already activated** gate values: `i`, `f`, `o` are the input, forget and output gate activations (in $(0,1)$), `g` is the candidate cell value and `c_prev` is the previous cell state. The new cell state is $c=f\odot c_{prev}+i\odot g$ and the new hidden state is $h=o\odot\tanh(c)$.

Implement `solve(i,f,o,g,c_prev)`.

**Returns.** Return a tuple `(h, c)` of NumPy vectors.

### Examples

**Example 1**

Input:

```python
solve([0.5, 0.5], [0.9, 0.9], [1.0, 1.0], [0.2, -0.2], [0.0, 0.0])
```

Output:

```text
([0.099668, -0.099668], [0.1, -0.1])
```

**Example 2**

Input:

```python
solve([0.0], [1.0], [1.0], [5.0], [2.0])
```

Output:

```text
([0.964028], [2.0])
```

## Theory

### The simple version

The LSTM's cell state is a conveyor belt of memory. The forget gate decides how much of the old memory to keep, the input gate decides how much of the new candidate to write, and the output gate decides how much of the (squashed) memory to expose as the hidden state.

### The formulas

$$c_t=f_t\odot c_{t-1}+i_t\odot g_t,\qquad h_t=o_t\odot\tanh(c_t)$$

## Explanation

In the first example the previous memory is $0$, so the new cell is $0.5\cdot0.2=0.1$ and the hidden state is $\tanh(0.1)\approx0.0997$. In the second the input gate is closed ($0$) and the forget gate is open ($1$), so the memory $2$ is carried over unchanged regardless of the candidate $5$.
