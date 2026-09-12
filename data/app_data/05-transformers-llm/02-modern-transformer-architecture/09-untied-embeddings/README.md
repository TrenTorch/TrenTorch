---
name: txf-modern-untied-embeddings
title: 'Untied embeddings, contrasted against weight tying'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A language model needs TWO conceptually different matrices shaped `(vocab_size, d_model)`: an INPUT embedding table (`[04-seq-modeling/02-embeddings/01-token-embedding-lookup]`, looking a token id UP to get a vector) and an OUTPUT projection (turning the model's final hidden state into a score, a "logit," for every word in the vocabulary, so a `softmax` over those logits gives next-token probabilities). Press & Wolf (2016) observed something genuinely useful: these two matrices, despite serving different DIRECTIONS of the same lookup (id-to-vector vs. vector-to-id-scores), can literally be the SAME matrix, "tied" together, rather than two entirely separate, independently-learned parameter sets, without hurting model quality, and while meaningfully REDUCING the total parameter count (a `vocab_size * d_model`-sized matrix, often a substantial fraction of a smaller model's total parameters, gets counted only once instead of twice).

The alternative, UNTIED embeddings, uses two entirely separate matrices: the model learns its own best input representation independently from its own best output-scoring function, at the cost of the extra parameters. Whether tying helps or hurts is itself an empirical, model-size-dependent question, smaller models often benefit measurably from tying (proportionally, the savings matter more, and sharing information between the "read" and "write" directions of the vocabulary can act as a useful regularizer), while very large models are more often trained untied, having plenty of capacity to spare and, in some cases, benefiting from letting the two roles specialize independently.

### From theory to code

Implement `output_projection_tied(hidden_states, embedding_table)`, projecting `hidden_states` to vocabulary logits by reusing an EXISTING embedding table (transposed), and `output_projection_untied(hidden_states, output_weight)`, the same projection using a SEPARATE, independently-learned matrix.

### Constraints

- Both functions compute `hidden_states @ matrix.T`, `matrix` being `embedding_table` in the tied case and `output_weight` in the untied case; both matrices are shaped `(vocab_size, d_model)`.
- The TIED version must genuinely reuse the SAME matrix object passed in as the embedding table, not a copy: if that table changes (as it would during training, since the SAME parameter also receives gradient updates from the input-embedding side), the output projection changes too, automatically.
- The UNTIED version's `output_weight` is entirely independent: changes to some other, unrelated embedding table must have no effect on it whatsoever.

### Hints

<details>
<summary>Hint 1: Both functions</summary>

Both are literally the same one-line computation: `return hidden_states @ matrix.T`. The distinction between "tied" and "untied" isn't in the MATH at all, it's entirely in WHICH matrix gets passed in, and whether that same matrix object is ALSO used elsewhere (as the input embedding table) or not.

</details>

<details>
<summary>Hint 2: Why this demonstrates tying correctly</summary>

Because NumPy arrays are mutable, passing the exact same `embedding_table` array into BOTH `[04-seq-modeling/02-embeddings/01-token-embedding-lookup]`'s lookup AND this question's `output_projection_tied` means any later modification to that array (e.g. a gradient update during training) is automatically visible from both call sites, no extra syncing code required. That's the entire mechanism weight tying relies on.

</details>

## Theory

### The simple version

A dictionary that works in BOTH directions: looking up a word's DEFINITION (input embedding: token id to vector) and looking up which word BEST MATCHES a given definition (output projection: vector to token scores). Weight tying says: this can be the SAME physical dictionary, consulted in either direction, rather than maintaining two separate books that happen to describe the same vocabulary and have to be kept in sync by hand. Untied embeddings maintains two genuinely separate books instead, at the cost of shelf space (parameters), but with the freedom for each book to specialize however turns out to work best for its own specific job.

### The formula

```
tied:   logits = hidden_states @ embedding_table.T     # SAME matrix used for input lookup
untied: logits = hidden_states @ output_weight.T        # a SEPARATE, independent matrix
```

Identical computation in both cases; the distinction is purely about which parameters get shared versus kept independent.

### How PyTorch actually implements this

`model.lm_head.weight = model.embed_tokens.weight` (a direct Python attribute assignment, making both names point at the exact same underlying `torch.nn.Parameter` tensor) is literally how weight tying gets implemented in real Hugging Face `transformers` model code; PyTorch's `autograd` then automatically accumulates gradients from BOTH usage sites (the embedding lookup and the output projection) into that one shared parameter during backpropagation, with no special-casing required beyond that one assignment. `[05-transformers-llm/03-language-model-assembly]`'s "Weight tying" question, later in this curriculum, wires this exact choice into a full, working language model's forward pass; this question's job was establishing the underlying MECHANISM and its direct contrast, in isolation.

## Explanation

Both `output_projection_tied` and `output_projection_untied` compute the identical operation, `hidden_states @ matrix.T`: the actual "tying" or "untying" isn't a difference in the MATH at all, it's entirely about which matrix gets passed in, and whether that matrix is ALSO the same object used elsewhere as the input embedding table. Because NumPy arrays are mutable objects, passing `embedding_table` into `output_projection_tied` means any later in-place modification to that array (standing in for a gradient update during real training) is immediately reflected in the output projection too, with no additional bookkeeping, exactly the property that makes weight tying a genuine parameter-sharing mechanism rather than merely "two parameters that happen to start out equal."
