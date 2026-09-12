---
name: seq-rnn-gru-cell-forward
title: 'GRU cell, forward (simplified gating)'
tags: [nlp, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-lstm-cell-forward]`'s LSTM solves `[03-bptt-vanishing-exploding]`'s vanishing-gradient problem with FOUR separate gates and a dedicated cell state `c`, carried alongside the hidden state `h`. The GRU (Gated Recurrent Unit, Cho et al., 2014) asks a genuinely useful engineering question: can most of the LSTM's benefit be achieved with LESS machinery? A GRU drops the separate cell state entirely (just one state, `h`, carried between steps, exactly like a vanilla RNN) and reduces four gates down to TWO: a "reset gate" (how much of the PREVIOUS hidden state to consider when computing a new candidate) and an "update gate" (how much of the OLD hidden state to keep vs. how much of the NEW candidate to blend in). In practice, GRUs are frequently competitive with LSTMs on many tasks, with meaningfully fewer parameters and a simpler implementation, which is part of why they remain a common practical choice even after LSTMs became well established.

The genuinely tricky implementation detail, and the reason this question is more than "the LSTM but with fewer gates": the reset gate `r` doesn't apply UNIFORMLY to the candidate computation, it multiplies ONLY the hidden-state contribution to the candidate (`Whn h + bhn`), never the input contribution (`Win x + bin`). This means the input and hidden pre-activations for the candidate gate have to be computed and kept SEPARATE, rather than summed together first (the way `[01-rnn-cell-forward]`'s and `[04-lstm-cell-forward]`'s pre-activations were), since `r` needs to gate only ONE of the two pieces before they're finally combined.

### From theory to code

Implement `gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)`, matching `torch.nn.GRUCell`'s packing convention: `[reset, update, new/candidate]`, three chunks (not four). Compute `gates_ih = x @ weight_ih.T + bias_ih` and `gates_hh = h_prev @ weight_hh.T + bias_hh` SEPARATELY (not summed). Compute `r` and `z` by summing their respective `gates_ih`/`gates_hh` slices and applying `sigmoid`. Compute `n` by applying `tanh` to `gates_ih`'s candidate slice PLUS `r` times `gates_hh`'s candidate slice (the reset gate applied ONLY to the hidden contribution). Combine via `h_next = (1-z)*n + z*h_prev`.

### Constraints

- `gates_ih` and `gates_hh` must be computed and kept SEPARATE (each its own `(batch_size, 3*hidden_size)` array), never summed together before the reset gate is applied.
- `r` and `z` are each `sigmoid` of the SUM of their respective `gates_ih`/`gates_hh` slices (both contributions summed BEFORE the sigmoid, exactly like `[01-rnn-cell-forward]`'s combined pre-activation).
- `n`'s hidden-side contribution (`gates_hh`'s candidate slice) must be multiplied by `r` BEFORE being added to `n`'s input-side contribution (`gates_ih`'s candidate slice); `n`'s input-side contribution is NEVER multiplied by `r`.
- `h_next = (1 - z) * n + z * h_prev`: `z` close to `1` means "keep mostly the OLD hidden state"; `z` close to `0` means "mostly replace it with the new candidate."

### Hints

<details>
<summary>Hint 1: r and z</summary>

`r_gate = sigmoid(gates_ih[:, 0:H] + gates_hh[:, 0:H])` and `z_gate = sigmoid(gates_ih[:, H:2H] + gates_hh[:, H:2H])`, where `H = hidden_size`, both are ordinary "sum both contributions, then sigmoid" gates, structurally identical to `[01-rnn-cell-forward]`'s combined pre-activation.

</details>

<details>
<summary>Hint 2: n, the reset-gated candidate</summary>

`n_gate = tanh(gates_ih[:, 2H:3H] + r_gate * gates_hh[:, 2H:3H])`: notice `r_gate` multiplies ONLY the `gates_hh` slice, `gates_ih`'s candidate slice is added in UNMODIFIED.

</details>

<details>
<summary>Hint 3: Combining into h_next</summary>

`h_next = (1.0 - z_gate) * n_gate + z_gate * h_prev`, a weighted blend (an interpolation, in fact, since `(1-z)` and `z` always sum to exactly `1`) between the brand-new candidate `n` and the OLD hidden state `h_prev`, controlled entirely by `z`.

</details>

## Theory

### The simple version

Editing a shared document with two independent controls: a "how much of my new draft edit should I even consider the EXISTING wording while writing it" dial (the reset gate, `r`, controls how much the OLD content influences the drafting of the NEW candidate text) and a completely separate "how much of the FINAL document should be my new edit vs. the original text, once I'm done drafting" dial (the update gate, `z`, controls the final blend). These are genuinely two DIFFERENT decisions, made at two different points in the process, which is exactly why a GRU needs both a reset gate (affecting how the CANDIDATE gets computed) and an update gate (affecting how the candidate gets BLENDED into the final result), rather than collapsing them into one.

### The formula

With `weight_ih`, `weight_hh`, `bias_ih`, `bias_hh` packed as `[reset, update, candidate]`:

```
gates_ih = x @ weight_ih.T + bias_ih
gates_hh = h_prev @ weight_hh.T + bias_hh

r = sigmoid(gates_ih[reset]    + gates_hh[reset])
z = sigmoid(gates_ih[update]   + gates_hh[update])
n = tanh(gates_ih[candidate]   + r * gates_hh[candidate])

h_next = (1 - z) * n + z * h_prev
```

### How PyTorch actually implements this

`torch.nn.GRUCell` implements exactly this formula, with exactly this `[reset, update, candidate]` packing and the specific "reset gates only the hidden contribution to the candidate" detail (this question's implementation matches it precisely, verified directly). The `h_next = (1-z)*n + z*h_prev` update is an INTERPOLATION (a "convex combination," since the two weights always sum to `1`), structurally similar in spirit to `[04-lstm-cell-forward]`'s additive `c_next = f*c_prev + i*g` update, both give the network a pathway to preserve old state through addition/interpolation rather than purely through repeated matrix multiplication, directly addressing `[03-bptt-vanishing-exploding]`'s core problem, just with a simpler two-gate, single-state structure instead of the LSTM's four-gate, dual-state one. Whether an LSTM or a GRU performs better on a given task is genuinely dataset- and architecture-dependent, and remains an empirical question practitioners often just test directly, rather than one either architecture wins decisively in general.

## Explanation

`gru_cell_forward` computes `gates_ih` and `gates_hh` SEPARATELY (never summed together up front, unlike `[01-rnn-cell-forward]`'s single combined pre-activation), since the reset gate needs to act on only ONE of them later. `r_gate` and `z_gate` are each computed by summing their respective slices of `gates_ih` and `gates_hh` and applying `sigmoid`, structurally ordinary gates. `n_gate` is computed by applying `tanh` to `gates_ih`'s candidate slice PLUS `r_gate` elementwise-multiplied into `gates_hh`'s candidate slice specifically, the reset gate gating ONLY the hidden-state contribution, exactly as the formula specifies. Finally, `h_next = (1.0 - z_gate) * n_gate + z_gate * h_prev` blends the new candidate and the old hidden state, weighted by `z_gate` and its complement, producing the updated (and only) hidden state a GRU carries forward.
