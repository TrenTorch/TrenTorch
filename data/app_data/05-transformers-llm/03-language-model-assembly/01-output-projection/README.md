---
name: txf-lm-output-projection
title: 'Output projection to vocab logits'
tags: [transformers, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every piece built in `[01-transformer-block]` and `[02-modern-transformer-architecture]` operates entirely in `d_model`-dimensional space: `[01-transformer-block/07-stack-blocks]`'s final output is a `(seq_len, d_model)` tensor, a refined vector at every position. To actually predict the NEXT token, that `d_model`-sized vector has to become a score for EVERY word in the vocabulary, `vocab_size` numbers instead of `d_model` numbers, one per candidate next word. This is exactly the same "project up to a different size" operation `[04-seq-modeling/02-embeddings/01-token-embedding-lookup]`'s embedding table performed in REVERSE (id-to-vector there, vector-to-id-scores here), and `[02-modern-transformer-architecture/09-untied-embeddings]` already built and named both directions of this exact operation.

### From theory to code

Implement `output_projection(hidden_states, output_weight)`, an ordinary linear projection (no bias, matching real LLM implementations) from `d_model` up to `vocab_size`.

### Constraints

- `output_weight` has shape `(vocab_size, d_model)`; the projection is `hidden_states @ output_weight.T`.
- No bias term: matches how modern LLM output heads are typically implemented (and how `[02-modern-transformer-architecture/09-untied-embeddings]`'s functions were already built).
- Works for any number of leading batch/sequence dimensions on `hidden_states`.

### Hints

<details>
<summary>Hint 1</summary>

`return hidden_states @ output_weight.T`, identical to `[09-untied-embeddings]`'s `output_projection_untied`. This question exists to give the operation its own, LM-assembly-specific name and place in the pipeline being built up across this track.

</details>

## Theory

### The simple version

Everything up through `[01-transformer-block/07-stack-blocks]` was refining a single, running "understanding" of each position, a `d_model`-sized vector. The output projection is the final translation step: converting that internal, abstract understanding into a concrete VOTE for every possible next word, one number per word in the entire vocabulary, the raw material `softmax` needs to turn into actual next-token probabilities.

### The formula

```
logits = hidden_states @ output_weight^T
```

`hidden_states`: `(..., d_model)`. `output_weight`: `(vocab_size, d_model)`. `logits`: `(..., vocab_size)`.

### How PyTorch actually implements this

`model.lm_head`, an ordinary `torch.nn.Linear(d_model, vocab_size, bias=False)`, is essentially every real decoder-only LLM's output projection, named `lm_head` (language-model head) in most Hugging Face `transformers` implementations. `[02-weight-tying]`, immediately following this question, examines whether `output_weight` should be its own independent parameter or the SAME matrix as the input embedding table.

## Explanation

`output_projection` computes `hidden_states @ output_weight.T`, an ordinary linear projection with no bias, taking the Transformer stack's final `d_model`-sized representation at every position and mapping it to a `vocab_size`-sized vector of raw scores, one per candidate next token. This is literally the same operation `[02-modern-transformer-architecture/09-untied-embeddings]`'s `output_projection_untied` already implemented; this question gives it its proper name and place as the very last step of a full language model's forward pass, immediately before `[02-modern-transformer-architecture/10-logit-scaling]`'s optional scaling and a final softmax.
