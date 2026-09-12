---
name: seq-rnn-cell-forward
title: 'Vanilla RNN cell, forward'
tags: [nlp, neural-networks]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[03-dl-training/02-layers/01-linear-forward]`'s `linear_forward` processes a single, fixed-size input and produces a single output, it has no notion of "sequence" or "what came before" at all. Recurrent Neural Networks were the first widely-used architecture built specifically to process SEQUENCES: instead of a single forward pass, an RNN walks through a sequence one element at a time, and at each step, combines the CURRENT input with a running "memory" of everything seen so far (the "hidden state"), producing both an output for that step and an UPDATED memory to carry into the next step. This is precisely the "processes tokens one at a time IN ORDER" behavior `[02-embeddings/03-sinusoidal-positional-encoding]`'s Statement contrasted attention against: an RNN's very act of stepping through a sequence in order IS how it encodes position, no separate positional encoding scheme needed at all.

This question implements exactly ONE step of that process: given the current input and the previous hidden state, compute the new hidden state. `Vanilla RNN cell, backward` and `Backprop through time (BPTT)`, immediately following this question, build on this single step to understand training an RNN across a whole sequence, and how gradients behave when this same step gets repeated many times in a row.

### From theory to code

Implement `rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)`. Compute a linear transformation of the CURRENT input (`x @ weight_ih.T + bias_ih`) and a SEPARATE linear transformation of the PREVIOUS hidden state (`h_prev @ weight_hh.T + bias_hh`), sum both results together, and apply `tanh` to produce the new hidden state.

### Constraints

- `weight_ih` has shape `(hidden_size, input_size)`, matching `[03-dl-training/02-layers/01-linear-forward]`'s `(out_features, in_features)` convention; `weight_hh` has shape `(hidden_size, hidden_size)` (since the hidden state feeds into itself).
- Both linear transformations (input-to-hidden and hidden-to-hidden) must be computed and summed BEFORE applying `tanh`, not `tanh` applied to each separately and then summed.
- The output has the SAME shape as `h_prev`: `(batch_size, hidden_size)`.
- Must work correctly for any `batch_size`, including `batch_size == 1`.

### Hints

<details>
<summary>Hint 1</summary>

`input_contribution = x @ weight_ih.T + bias_ih`, exactly `[03-dl-training/02-layers/01-linear-forward]`'s `linear_forward` applied to `x`.

</details>

<details>
<summary>Hint 2</summary>

`hidden_contribution = h_prev @ weight_hh.T + bias_hh`, the SAME kind of linear transformation, applied to `h_prev` instead of `x`, with its own separate weight/bias.

</details>

<details>
<summary>Hint 3</summary>

`return np.tanh(input_contribution + hidden_contribution)`: sum both contributions FIRST, then apply `tanh` once to the combined sum, not `tanh` to each piece separately.

</details>

## Theory

### The simple version

Reading a novel one sentence at a time while keeping a running mental summary of the plot so far: after each new sentence, you don't discard your previous understanding and start over, you BLEND the new sentence's content with your existing mental summary, updating it into a new, slightly-revised summary that carries forward into the next sentence. An RNN's hidden state is exactly this running mental summary, updated at every single time step by blending in whatever new information the current input provides.

### The formula

```
h_t = tanh(W_ih @ x_t + b_ih + W_hh @ h_{t-1} + b_hh)
```

Written with `x_t` and `h_{t-1}` as ROW vectors (matching this question's `(batch_size, ...)` convention): `h_t = tanh(x_t @ W_ih.T + b_ih + h_{t-1} @ W_hh.T + b_hh)`. The subscript `t` denotes the CURRENT time step; `t-1` denotes the PREVIOUS one, `h_t` becomes the input to this exact same formula on the NEXT step, `t+1`, which is what makes this a genuinely RECURRENT computation.

### How PyTorch actually implements this

`torch.nn.RNNCell` implements exactly this formula (this question's implementation matches it precisely, verified directly against `RNNCell`'s own forward pass), and `torch.nn.RNN` is essentially this same cell applied repeatedly across an entire sequence in a loop, internally, producing a full sequence of hidden states rather than requiring you to write that loop yourself. `weight_ih`, `weight_hh`, `bias_ih`, and `bias_hh` are all genuine `nn.Parameter`s, trained by ordinary backpropagation, exactly like `[03-dl-training/02-layers/01-linear-forward]`'s `weight`/`bias`, the one crucial difference from a plain feedforward layer being that `weight_hh` gets applied REPEATEDLY, once per time step, to a hidden state that itself depends on every previous time step, which is precisely the source of `Backprop through time (BPTT)`'s vanishing/exploding gradient concerns, immediately following this question: the SAME `weight_hh` matrix gets multiplied into the gradient computation once per time step, compounding across the sequence length exactly the way `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]`'s `matrix_gradient_norms` demonstrated for depth.

## Explanation

`rnn_cell_forward` computes `x @ weight_ih.T + bias_ih` (the input's own linear transformation, exactly `[03-dl-training/02-layers/01-linear-forward]`'s `linear_forward` applied to `x`) and `h_prev @ weight_hh.T + bias_hh` (the previous hidden state's own SEPARATE linear transformation, with its own weight and bias), sums both contributions together, and applies `np.tanh` to the sum, producing the new hidden state, which carries the same shape as `h_prev` and becomes the "previous hidden state" input to this same function on the next time step.
