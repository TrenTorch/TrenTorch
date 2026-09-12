---
name: seq-rnn-lstm-cell-forward
title: 'LSTM cell, forward (gating mechanism)'
tags: [nlp, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-bptt-vanishing-exploding]` demonstrated PRECISELY why vanilla RNNs struggle with long sequences: the same `weight_hh` matrix gets multiplied into the gradient at every single time step, and that repeated multiplication compounds into vanishing or exploding behavior over enough steps, no matter how carefully `weight_hh` is initialized. The Long Short-Term Memory cell (Hochreiter & Schmidhuber, 1997) was specifically designed to sidestep this problem, by introducing a SEPARATE "cell state" `c`, alongside the usual hidden state `h`, that gets updated PRIMARILY through addition rather than repeated matrix multiplication: `c_next = f * c_prev + i * g`. That `f * c_prev` term is an elementwise MULTIPLY by a LEARNED, per-timestep gate value (not a fixed matrix multiplied in every single time regardless of content), and crucially, if the "forget gate" `f` happens to be close to `1` at a given step (meaning "keep most of the old memory"), the cell state can flow backward through MANY time steps nearly UNCHANGED, gradients don't have to compound through repeated multiplication by the same matrix the way `[03-bptt-vanishing-exploding]` demonstrated.

An LSTM achieves this by computing FOUR separate gate values at every step, each with its own learned weights, but all packed into the SAME linear transformation for efficiency: an "input gate" (how much of the new candidate information to let in), a "forget gate" (how much of the old cell state to keep vs. discard), a "candidate" (what NEW information might get added), and an "output gate" (how much of the updated cell state to actually expose as the hidden state).

### From theory to code

Implement `lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)`, matching `torch.nn.LSTMCell`'s exact packing convention: `weight_ih`/`weight_hh`/`bias_ih`/`bias_hh` each contain all FOUR gates' parameters stacked together, in order `[input, forget, cell/candidate, output]`. Compute the combined pre-activation `gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh` (shape `(batch_size, 4*hidden_size)`), split it into four equal `hidden_size`-wide chunks, apply `sigmoid` to the input/forget/output gates and `tanh` to the candidate, then combine via `c_next = f*c_prev + i*g` and `h_next = o*tanh(c_next)`.

### Constraints

- Gates must be extracted from `gates` in EXACTLY this order: input (`i`), forget (`f`), cell/candidate (`g`), output (`o`), matching `torch.nn.LSTMCell`'s packing convention.
- `i`, `f`, and `o` use `sigmoid` (values in `(0, 1)`, interpreted as "how much"); `g` uses `tanh` (values in `(-1, 1)`, an actual candidate VALUE, not a gate).
- `c_next = f * c_prev + i * g` (elementwise multiply, then add), NOT any matrix multiplication.
- `h_next = o * tanh(c_next)`, applying `tanh` to the UPDATED cell state before gating it with `o`.

### Hints

<details>
<summary>Hint 1: Computing and splitting the combined gates</summary>

`gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh` gives a `(batch_size, 4*hidden_size)` array. Split it with plain slicing: `gates[:, 0:hidden_size]` (input), `gates[:, hidden_size:2*hidden_size]` (forget), `gates[:, 2*hidden_size:3*hidden_size]` (candidate), `gates[:, 3*hidden_size:4*hidden_size]` (output).

</details>

<details>
<summary>Hint 2: Applying the right activation to each slice</summary>

`i_gate = sigmoid(gates[:, 0:hidden_size])`, `f_gate = sigmoid(gates[:, hidden_size:2*hidden_size])`, `g_gate = np.tanh(gates[:, 2*hidden_size:3*hidden_size])`, `o_gate = sigmoid(gates[:, 3*hidden_size:4*hidden_size])`. Three `sigmoid`s (gates), one `tanh` (the actual candidate content).

</details>

<details>
<summary>Hint 3: Combining into the new states</summary>

`c_next = f_gate * c_prev + i_gate * g_gate` (elementwise), then `h_next = o_gate * np.tanh(c_next)`. Return `(h_next, c_next)`, both are needed: `c_next` carries forward as the NEXT step's `c_prev`, and `h_next` is both this step's output AND the next step's `h_prev`.

</details>

## Theory

### The simple version

A river with a controllable dam gate system: the "forget gate" controls how much of the water already behind the dam gets released vs. retained, the "input gate" controls how much NEW water from upstream is allowed to flow in, and the "output gate" controls how much of the CURRENT reservoir level actually gets released downstream right now (as opposed to held in reserve for later). Crucially, when the forget gate is opened WIDE (close to 1, "retain almost everything"), water that entered the reservoir a long time ago can still be sitting there, essentially unchanged, many time steps later, exactly the LONG-RANGE memory an LSTM's cell state is designed to preserve, in stark contrast to a vanilla RNN's hidden state, which gets fully overwritten (via `tanh` of a NEW combined sum) at every single step.

### The formula

With `weight_ih`, `weight_hh`, `bias_ih`, `bias_hh` all packed as `[input, forget, cell, output]`:

```
gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh
i, f, g, o = split gates into 4 equal chunks

i = sigmoid(i)
f = sigmoid(f)
g = tanh(g)
o = sigmoid(o)

c_next = f * c_prev + i * g
h_next = o * tanh(c_next)
```

### How PyTorch actually implements this

`torch.nn.LSTMCell` implements exactly this formula, with exactly this `[i, f, g, o]` packing convention (this question's implementation matches it precisely, verified directly). The `f * c_prev` term, an elementwise multiply by a value in `(0, 1)` rather than a matrix multiply, is the mechanism specifically designed to solve `[03-bptt-vanishing-exploding]`'s problem: if the network LEARNS (through training) that `f` should stay close to `1` for a particular piece of information across many time steps, the gradient with respect to `c_prev` at that step is close to `1` too (since `d(c_next)/d(c_prev) = f`), letting gradients flow backward across many steps with comparatively little attenuation, a genuinely different mechanism from a vanilla RNN's `weight_hh`-multiplied-every-step pathway. `GRU cell, forward (simplified gating)`, immediately following this question, achieves a very similar effect with a SIMPLER gating structure (2 gates instead of 4, and no separate cell state), a common, often-comparable-in-practice alternative that trades some of the LSTM's representational flexibility for fewer parameters and a simpler implementation.

## Explanation

`lstm_cell_forward` computes the combined pre-activation `gates = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh` in one shot, then slices it into four `hidden_size`-wide chunks in `[input, forget, candidate, output]` order, applying `sigmoid` to the input, forget, and output gates (values in `(0,1)`, "how much") and `tanh` to the candidate (values in `(-1,1)`, the actual content being proposed).

It then computes `c_next = f_gate * c_prev + i_gate * g_gate`: the forget gate elementwise-scales how much of the OLD cell state survives, and the input gate elementwise-scales how much of the NEW candidate gets added in, both terms then summed (not multiplied together) to form the updated cell state. Finally, `h_next = o_gate * np.tanh(c_next)` applies `tanh` to the updated cell state and elementwise-scales it by the output gate, producing the new hidden state, which the function returns alongside `c_next`.
