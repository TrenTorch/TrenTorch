---
name: seq-rnn-seq2seq-bottleneck
title: 'Sequence-to-sequence / encoder-decoder: the bottleneck problem attention was invented to solve'
tags: [nlp, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Machine translation (and many other tasks: summarization, question answering) needs to map one variable-length sequence to another. The classic pre-Transformer solution, "sequence-to-sequence" (Sutskever et al., 2014), is elegantly simple: an ENCODER RNN (`[01-rnn-cell-forward]`, applied repeatedly, exactly `[06-bidirectional-rnn]`'s forward-direction loop) reads the entire input sentence and compresses it down into a single, FIXED-SIZE hidden state, the "context vector." A DECODER RNN then starts from that context vector and generates the output sentence, one token at a time.

This design has a genuine, well-documented weakness this question demonstrates numerically rather than just describing: `hidden_size` stays FIXED regardless of how long the input sentence is. A 5-word sentence and a 50-word sentence both get compressed down into the exact SAME size vector, and, just like `[03-bptt-vanishing-exploding]` demonstrated for gradients flowing backward, an RNN's hidden state, updated step by step going FORWARD, tends to be dominated by RECENT inputs, information from early in a long sequence can get substantially overwritten by everything that came after it, long before the encoder ever reaches the end. The FINAL hidden state, the only thing the decoder ever sees, disproportionately reflects the LATE part of the input, with early content potentially barely surviving at all. This is the exact motivation named directly in `Scaled dot-product attention`, the very next track in this curriculum: instead of forcing the ENTIRE input sequence through one fixed-size bottleneck, attention gives the decoder access to EVERY encoder hidden state directly, letting it look back at whichever parts of the input actually matter for the CURRENT word being generated, regardless of how far back in the sequence they occurred.

### From theory to code

Implement `encode_all_hidden_states(x_seq, h0, weight_ih, weight_hh, bias_ih, bias_hh)`, running `[01-rnn-cell-forward]`'s `rnn_cell_forward` (already provided, reused via `load_solution`) across the whole sequence and returning EVERY step's hidden state. Implement `get_bottleneck_context(hidden_states)`, extracting just the LAST one, the classic seq2seq "context vector," everything else discarded. Implement `cosine_similarity(a, b)`, a similarity measure between `0` (unrelated) and `1` (identical direction), used to numerically MEASURE how much information from different parts of a sequence actually survives into the final context vector.

### Constraints

- `encode_all_hidden_states` must return ALL `seq_len` hidden states, shape `(seq_len, batch_size, hidden_size)`, not just the last one.
- `get_bottleneck_context` returns exactly `hidden_states[-1]`, the final time step's hidden state, discarding everything from earlier steps.
- `cosine_similarity` must correctly handle inputs of ANY matching shape (flatten both before computing), returning a single scalar float.

### Hints

<details>
<summary>Hint 1: encode_all_hidden_states</summary>

Loop `for t in range(seq_len): h = rnn_cell_forward(x_seq[t], h, weight_ih, weight_hh, bias_ih, bias_hh); hidden_states.append(h)`, starting `h = h0`, and `return np.stack(hidden_states, axis=0)` at the end, exactly `[06-bidirectional-rnn]`'s forward loop, just returning EVERY step's output instead of discarding all but the last.

</details>

<details>
<summary>Hint 2: get_bottleneck_context</summary>

`return hidden_states[-1]`, a one-line slice picking out the final time step's hidden state from `encode_all_hidden_states`'s full output.

</details>

<details>
<summary>Hint 3: cosine_similarity</summary>

`a_flat = a.reshape(-1)`, `b_flat = b.reshape(-1)`, then `np.dot(a_flat, b_flat) / (np.linalg.norm(a_flat) * np.linalg.norm(b_flat) + 1e-8)` (the small `1e-8` in the denominator avoids a divide-by-zero if either vector happens to be exactly zero).

</details>

## Theory

### The simple version

Summarizing an entire book into a SINGLE sentence, and handing ONLY that one sentence to someone who then has to answer detailed questions about the book, questions about the very first chapter included. A short book might compress reasonably well; a very LONG book almost certainly loses substantial detail in that single-sentence summary, and whatever detail survives tends to be whatever was FRESHEST in the summarizer's mind, typically the ENDING, rather than an even, uniform coverage of the whole book. Giving the question-answerer access to the FULL, unsummarized book instead (attention's approach: every encoder hidden state, not just a compressed final one) obviously does much better, at the cost of needing to search through more material to find the relevant part.

### The formula

There's no new numeric formula here beyond `[01-rnn-cell-forward]`'s own recurrence, applied repeatedly:

```
h[0] = rnn_cell_forward(x[0], h0, ...)
h[t] = rnn_cell_forward(x[t], h[t-1], ...)    for t = 1, ..., seq_len-1

context = h[seq_len - 1]     # the classic seq2seq bottleneck: only the LAST one survives
```

The measurable claim this question demonstrates: `cosine_similarity(context_A, context_B)` stays HIGH when sequences A and B differ substantially in their EARLY steps but agree in their LATE steps (early differences barely register in the final context), and drops substantially when A and B agree early but differ LATE (late differences dominate the final context almost entirely).

### How PyTorch actually implements this

Classic seq2seq models, still implemented in PyTorch today for smaller-scale or specialized use cases, wire together an encoder `nn.RNN`/`nn.LSTM`/`nn.GRU` and a decoder of the same kind exactly this way: the encoder's FINAL hidden state (and, for an LSTM, final cell state too) becomes the decoder's INITIAL hidden state, and the decoder then generates output tokens one at a time from there, with no further access to the encoder's earlier hidden states at all. `Scaled dot-product attention` and the `Multi-Head Attention` questions later in this Part implement the actual fix real production translation and language systems adopted: instead of this bottleneck, the decoder computes, at EVERY generation step, a weighted combination of ALL the encoder's hidden states (exactly the full `encode_all_hidden_states` output this question builds, never discarded down to just the last one), letting it dynamically "look back" at whichever part of the input is most relevant to the word it's currently generating. This shift, from "compress everything into one fixed vector" to "attend to everything, dynamically, as needed," is widely regarded as the single most important architectural idea leading directly to the Transformer.

## Explanation

`encode_all_hidden_states` loops through `x_seq` calling `rnn_cell_forward` at each step (starting from `h0`), collecting EVERY step's resulting hidden state into a list, and stacks them into a single `(seq_len, batch_size, hidden_size)` array, preserving the FULL sequence of hidden states rather than discarding any of them.

`get_bottleneck_context` returns `hidden_states[-1]`, the LAST entry along the time axis, exactly modeling the classic seq2seq architecture's decision to keep only the final hidden state as the "context vector" handed to the decoder.

`cosine_similarity` flattens both inputs to 1D, computes their dot product, and divides by the product of their norms (with a small epsilon guarding against division by zero), producing a value in roughly `[-1, 1]` that measures how aligned two vectors' directions are, used here to numerically quantify how much of a sequence's early vs. late content actually survives into its final, bottlenecked context vector.
