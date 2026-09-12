---
name: txf-lm-weight-tying
title: 'Weight tying (share input/output embedding matrix)'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[02-modern-transformer-architecture/09-untied-embeddings]` established the mechanism and the direct contrast in isolation: an input embedding table and an output projection matrix, both shaped `(vocab_size, d_model)`, can either be TWO separate, independently-learned parameters ("untied"), or literally the SAME matrix, consulted in both directions ("tied"). This question wires that choice directly into a full language model's assembly, as a single `tied` flag controlling which behavior `[01-full-forward-pass]`, immediately following, actually uses.

### From theory to code

Implement `compute_output_logits(hidden_states, embedding_table, tied, output_weight)`, dispatching to `embedding_table` when `tied=True` (ignoring `output_weight` entirely) or to `output_weight` when `tied=False`, and `count_output_head_parameters(vocab_size, d_model, tied)`, the number of ADDITIONAL parameters the choice introduces.

### Constraints

- `tied=True`: use `embedding_table` for the projection; `output_weight` is not needed and may be `None`.
- `tied=False`: use `output_weight` for the projection.
- `count_output_head_parameters` returns `0` when tied (no new matrix at all) and `vocab_size * d_model` when untied (one full new matrix).

### Hints

<details>
<summary>Hint 1</summary>

```python
matrix = embedding_table if tied else output_weight
return hidden_states @ matrix.T
```

</details>

<details>
<summary>Hint 2</summary>

`return 0 if tied else vocab_size * d_model`. This is purely a parameter-COUNTING function, no matrices actually get constructed.

</details>

## Theory

### The simple version

A choice a model architect makes once, before training even starts: does the model get ONE shared reference book for both "look up a word" and "score a word" (tied, `[02-modern-transformer-architecture/09-untied-embeddings]`'s shared-dictionary analogy), or TWO separate books (untied)? `count_output_head_parameters` is simply counting how many extra pages the untied choice requires printing, compared to reusing the book the model already needed anyway.

### The formula

```
tied:   logits = hidden_states @ embedding_table^T,  extra_params = 0
untied: logits = hidden_states @ output_weight^T,     extra_params = vocab_size * d_model
```

### How PyTorch actually implements this

`model.tie_weights()`, a method most Hugging Face `transformers` language models expose directly, performs `model.lm_head.weight = model.get_input_embeddings().weight`, and a model's config typically exposes a `tie_word_embeddings` boolean controlling whether this gets called automatically at initialization. `[01-full-forward-pass]`, immediately following this question, wires this exact `tied` flag all the way through a complete forward pass, from raw token ids to final vocabulary logits.

## Explanation

`compute_output_logits` picks between `embedding_table` and `output_weight` based on the `tied` flag, then applies the identical `@ matrix.T` projection either way, exactly matching `[09-untied-embeddings]`'s two separate functions, now unified behind one switch. `count_output_head_parameters` returns `0` for the tied case (the output head introduces no NEW parameters beyond the embedding table it's reusing) and `vocab_size * d_model` for the untied case (one entire new matrix), a direct, concrete measure of the parameter-count savings weight tying provides, often a meaningful fraction of a smaller model's total parameter budget.
