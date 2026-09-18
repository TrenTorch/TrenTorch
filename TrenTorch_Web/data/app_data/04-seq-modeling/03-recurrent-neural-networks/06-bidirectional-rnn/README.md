---
name: seq-rnn-bidirectional
title: 'Stretch: bidirectional RNN'
tags: [nlp, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-rnn-cell-forward]`'s RNN processes a sequence strictly left to right: the hidden state at position 5 has seen positions 0 through 5, but has absolutely no information about position 6, 7, or beyond, they haven't happened yet, as far as the recurrence is concerned. For GENERATING text one token at a time (covered later in this curriculum), this causal, left-to-right constraint is exactly correct and unavoidable, you genuinely can't see the future when generating it. But for many other tasks, understanding a sentence's grammar, tagging each word's part of speech, translating a full sentence you already have complete access to, restricting the model to only ever see what came BEFORE each position is an artificial and unnecessary limitation: the word "bank" means something different in "I sat by the river bank" versus "I deposited money at the bank," and that disambiguating context can come from EITHER direction, sometimes from words that appear LATER in the sentence.

A bidirectional RNN removes this restriction directly: run TWO completely separate RNNs over the same sequence, one processing left-to-right as usual, one processing right-to-left, each with its own independently-learned weights, and at every position, concatenate BOTH directions' hidden states together. The result: every single position's final representation has now seen the ENTIRE sequence, both what came before it and what comes after it, something neither direction alone could ever provide.

### From theory to code

Implement `bidirectional_rnn_forward`, running `[01-rnn-cell-forward]`'s `rnn_cell_forward` (already provided, reused via `load_solution`) TWICE across `x_seq` (shape `(seq_len, batch_size, input_size)`): once forward, stepping through positions `0` to `seq_len-1` in order, and once backward, stepping through positions `seq_len-1` down to `0`, using its OWN separate weights. At every ORIGINAL time step, concatenate that step's forward-direction hidden state with that SAME step's backward-direction hidden state, and return the full `(seq_len, batch_size, 2*hidden_size)` result, in the ORIGINAL, un-reversed time order.

### Constraints

- The forward pass must process `x_seq` in order (`t = 0, 1, ..., seq_len-1`), using `weight_ih_fwd`/`weight_hh_fwd`/etc.
- The backward pass must process `x_seq` in REVERSE order (`t = seq_len-1, ..., 1, 0`), using its OWN, separate `weight_ih_bwd`/`weight_hh_bwd`/etc.
- The final result must be in ORIGINAL time order: position `t`'s output is the concatenation of the forward pass's hidden state AT position `t` and the backward pass's hidden state AT position `t` (not the order those values happened to be COMPUTED in during the backward loop).
- The output's last axis must be `2*hidden_size`: forward hidden state concatenated with backward hidden state, in that order.

### Hints

<details>
<summary>Hint 1: The forward pass</summary>

`h_fwd = h0_forward`, then `for t in range(seq_len): h_fwd = rnn_cell_forward(x_seq[t], h_fwd, weight_ih_fwd, weight_hh_fwd, bias_ih_fwd, bias_hh_fwd); forward_outputs.append(h_fwd)`, appending each step's output in the natural order they're computed.

</details>

<details>
<summary>Hint 2: The backward pass, and putting it back in order</summary>

`h_bwd = h0_backward`, then `for t in reversed(range(seq_len)): h_bwd = rnn_cell_forward(x_seq[t], h_bwd, weight_ih_bwd, weight_hh_bwd, bias_ih_bwd, bias_hh_bwd); backward_outputs.append(h_bwd)`. This loop APPENDS in the order positions were VISITED (last position first), so call `backward_outputs.reverse()` afterward to put the list back into original time order before combining.

</details>

<details>
<summary>Hint 3: Combining</summary>

`combined = [np.concatenate([f, b], axis=-1) for f, b in zip(forward_outputs, backward_outputs)]`, then `return np.stack(combined, axis=0)`. Since both lists are now in original time order (after the reverse in Hint 2), `zip` correctly pairs up each position's forward and backward hidden states.

</details>

## Theory

### The simple version

Editing a sentence you've written entirely, where you can freely look BOTH backward at what you've already written AND forward at what comes later in the same sentence, versus reading it aloud live, one word at a time, where you can only ever reference words you've already SAID. Understanding a finished piece of writing benefits enormously from seeing the whole thing at once; GENERATING it, one word at a time as it's produced, fundamentally cannot. A bidirectional RNN is built for the FIRST situation, where the entire sequence is already available, understanding a complete sentence, tagging a finished document, not for generating new text one token at a time.

### The formula

```
h_forward[t]  = rnn_cell_forward(x[t], h_forward[t-1], weights_fwd)     for t = 0, ..., seq_len-1
h_backward[t] = rnn_cell_forward(x[t], h_backward[t+1], weights_bwd)    for t = seq_len-1, ..., 0

output[t] = concat(h_forward[t], h_backward[t])
```

Note `h_backward`'s recurrence runs in the OPPOSITE direction (`h_backward[t]` depends on `h_backward[t+1]`, the FUTURE step, not the past one), which is exactly why it needs its own separate loop over the sequence, walked in reverse.

### How PyTorch actually implements this

`torch.nn.RNN(..., bidirectional=True)` (and the equivalent flag on `LSTM`/`GRU`) implements exactly this pattern internally, running both directions and concatenating their outputs at every time step, with `weight_ih_l0`/`weight_hh_l0`/etc. for the forward direction and `weight_ih_l0_reverse`/`weight_hh_l0_reverse`/etc. for the backward direction (this question's implementation matches `torch.nn.RNN(bidirectional=True)`'s output precisely, verified directly). Bidirectional RNNs became a standard building block for sequence-LABELING tasks (part-of-speech tagging, named entity recognition) and as an ENCODER component within `Sequence-to-sequence / encoder-decoder`, the very next question in this track: an encoder is free to see the WHOLE input sentence before producing anything, making bidirectionality a natural fit there, while a DECODER (which generates output one token at a time, unable to see its own future output before producing it) is fundamentally restricted to a causal, forward-only direction, exactly the same `Causal mask` restriction that `Scaled dot-product attention`, later in this Part, enforces for attention-based decoders too.

## Explanation

`bidirectional_rnn_forward` runs a first loop over `t in range(seq_len)`, calling `rnn_cell_forward` with the forward-direction weights and accumulating `h_fwd` step by step, appending each step's output to `forward_outputs` in natural (original) time order.

It then runs a SECOND loop over `t in reversed(range(seq_len))`, calling `rnn_cell_forward` with the backward-direction weights and accumulating `h_bwd`, but since this loop visits positions from the END of the sequence toward the START, `backward_outputs` ends up populated in REVERSED order relative to the original sequence; calling `.reverse()` on it afterward restores original time order.

With both lists now aligned in original time order, `zip(forward_outputs, backward_outputs)` pairs up each position's forward and backward hidden states correctly, and `np.concatenate([f, b], axis=-1)` combines them into one `2*hidden_size`-wide vector per position, `np.stack(..., axis=0)` assembling the full `(seq_len, batch_size, 2*hidden_size)` result.
