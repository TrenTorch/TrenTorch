---
name: txf-lm-full-forward-pass
title: 'Full forward pass (tokens to embeddings to blocks to logits)'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Every previous question in this curriculum's `[04-seq-modeling]` and `[05-transformers-llm]` sections built exactly ONE piece of a language model in isolation: `[04-seq-modeling/02-embeddings/01-token-embedding-lookup]` turns ids into vectors, `[04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding]` injects position, `[01-transformer-block/07-stack-blocks]` refines those vectors through many Transformer blocks, and `[02-weight-tying]`'s `compute_output_logits` turns the result into vocabulary scores. This question's entire content is WIRING, connecting five already-independently-verified pieces into one genuine, working, end-to-end forward pass, from raw integer token ids all the way to next-token logits, with no new mathematics introduced anywhere.

### From theory to code

Implement `full_lm_forward(token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask)`, chaining: token embedding lookup, adding sinusoidal positional encoding, running the result through `[07-stack-blocks]`'s stack of Transformer blocks, and finally `[02-weight-tying]`'s output projection.

### Constraints

- `token_ids` includes a leading batch dimension, `(batch, seq_len)`: every downstream piece (attention's head-splitting, specifically) requires one.
- Positional encoding is computed for exactly `token_ids`'s sequence length and ADDED to the token embeddings (`[05-combine-token-positional-embeddings]`'s pattern), before any Transformer block runs.
- `blocks_params` and `num_heads` pass straight through to `[07-stack-blocks]`'s `stack_transformer_blocks`, unchanged.
- `tied`/`output_weight` pass straight through to `[02-weight-tying]`'s `compute_output_logits`, unchanged.

### Hints

<details>
<summary>Hint 1: The embedding stage</summary>

```python
token_embeddings = embedding_forward(token_ids, token_embedding_table)
positional_embeddings = sinusoidal_positional_encoding(seq_len, d_model)
x = combine_embeddings(token_embeddings, positional_embeddings)
```

`seq_len = token_ids.shape[-1]`, `d_model = token_embedding_table.shape[-1]`.

</details>

<details>
<summary>Hint 2: The rest of the pipeline</summary>

```python
x = stack_transformer_blocks(x, num_heads, blocks_params, mask=mask)
return compute_output_logits(x, token_embedding_table, tied, output_weight)
```

Two more function calls, each already fully built and independently tested; this question adds no new computation of its own beyond correctly chaining them in order.

</details>

## Theory

### The simple version

An assembly line where every previous curriculum question built and independently quality-tested ONE station: the "look up a word" station, the "stamp a position onto it" station, the "refine through many processing stages" station, the "convert the final result into a vocabulary-wide score" station. This question's entire job is arranging those already-working stations in the correct ORDER on one production line, verifying that what comes out of one station is exactly the shape and kind of thing the next station expects, with no new machinery invented at this stage at all.

### The formula

```
token_embeddings      = Embed(token_ids)
positional_embeddings = SinusoidalPositionalEncoding(seq_len, d_model)
x = token_embeddings + positional_embeddings
x = StackedTransformerBlocks(x)
logits = OutputProjection(x)
```

Every one of these five steps was independently built, independently verified against a real reference (or a structural property), and independently tested EARLIER in this curriculum; this question is purely their composition.

### How PyTorch actually implements this

A real Hugging Face `transformers` decoder-only model's `forward` method performs exactly this sequence of calls (`self.embed_tokens`, adding positional information, `self.layers` (a `torch.nn.ModuleList` of Transformer blocks), `self.lm_head`), just organized as PyTorch module method calls rather than a flat function, with the SAME underlying computation either way. `[05-training-loop]`, immediately following this question, treats `full_lm_forward` as the model being trained; `[07-greedy-decoding]` and the questions after it treat it as the model being SAMPLED from, calling it repeatedly to generate text one token at a time.

## Explanation

`full_lm_forward` chains five already-verified pieces in sequence: `embedding_forward` looks up every token id's vector, `sinusoidal_positional_encoding` computes a position-dependent signal for the input's own sequence length, `combine_embeddings` adds the two together, `stack_transformer_blocks` runs the combined result through every Transformer block in `blocks_params` (each one internally handling its own attention, normalization, residual connections, and feed-forward sublayer, none of which this question needs to know about directly), and `compute_output_logits` converts the final refined representation into vocabulary-sized logits, either tied to the input embedding table or via a separate `output_weight`. No new computation is introduced anywhere in this function; its entire value is correctly connecting pieces whose individual correctness was already established independently, each in its own earlier question.
