---
name: seq-embeddings-token-embedding-lookup
title: Token embedding lookup
tags: [nlp, transformers, embeddings]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-tokenization/05-encode-decode-roundtrip]`'s `encode` produces a sequence of integer token ids, but an integer id is a completely ARBITRARY label: id `47` and id `48` might refer to two totally unrelated words, and there's no reason the network should treat them as "close" just because their id numbers happen to be adjacent. What a network actually needs is a DENSE VECTOR representation of each token, one where semantically similar words end up with similar vectors (learned automatically during training, not hand-designed), so `[03-dl-training/02-layers/01-linear-forward]`'s matrix multiplications and everything built on top of them have something meaningful to compute with.

The embedding table is exactly this: one row per vocabulary entry, each row a learnable vector of `embed_dim` numbers. "Looking up" a token's embedding is conceptually just a lookup table access (in exactly the sense the "lookup table" comparison in `[03-dl-training/05-why-deep-networks-work/02-representation-learning]` described, except here the vocabulary size is fixed and small enough that a genuine per-token row DOES make sense, unlike that question's exponentially-many feature COMBINATIONS), but framed as a matrix operation so it fits naturally into a network trained end-to-end with `[02-deep-learning-core/04-autograd]`'s backpropagation.

### From theory to code

Implement `embedding_forward(token_ids, embedding_table)`. `embedding_table` has shape `(vocab_size, embed_dim)`, one row per vocabulary entry. `token_ids` can be any shape, a single sequence of ids, or a whole batch of sequences. The output replaces every id in `token_ids` with that id's corresponding row from `embedding_table`, so the output shape is `token_ids`'s shape with one extra trailing `embed_dim` dimension.

### Constraints

- For a single id, `embedding_forward` returns exactly `embedding_table[id]`, that row, unchanged.
- For `token_ids` of shape `(batch_size, seq_len)`, the output must have shape `(batch_size, seq_len, embed_dim)`.
- The SAME id appearing multiple times in `token_ids` must return the SAME row every time (the embedding table doesn't change during a single forward pass).
- Must not modify `embedding_table` itself.

### Hints

<details>
<summary>Hint 1</summary>

NumPy's fancy indexing already does exactly this in one line: `embedding_table[token_ids]`. If `token_ids` has shape `(batch_size, seq_len)` and `embedding_table` has shape `(vocab_size, embed_dim)`, the result automatically comes out as `(batch_size, seq_len, embed_dim)`.

</details>

<details>
<summary>Hint 2</summary>

Fancy indexing with an array of ids (rather than a single integer or a slice) always returns a NEW array (a copy of the selected rows), so `embedding_table` itself is never modified by this operation, exactly matching the constraint above.

</details>

## Theory

### The simple version

A coat check at a theater: instead of describing your coat in words every time (color, size, brand, a description that could be ambiguous or hard to match), you're handed a numbered ticket, and later that SAME number retrieves EXACTLY your coat from a rack, quickly and unambiguously. A token id is the ticket number; the embedding table is the rack; looking up an embedding is handing over the ticket and getting back the actual, rich object (here, a vector of learned features) it refers to.

### The formula

```
embedding_forward(token_ids, embedding_table) = embedding_table[token_ids]
```

Trivial as a formula, but the SHAPE behavior is the substantive part: for `token_ids` of shape `(d1, d2, ..., dk)` and `embedding_table` of shape `(vocab_size, embed_dim)`, the result has shape `(d1, d2, ..., dk, embed_dim)`, every dimension of `token_ids` preserved, with a new trailing `embed_dim` axis appended.

### How PyTorch actually implements this

`torch.nn.Embedding.forward` implements exactly this row-gather operation (dispatching to `torch.nn.functional.embedding`, backed by an ATen kernel that performs an index-select along the table's first dimension), and the embedding table itself, `embedding_table` here, is a genuine `nn.Parameter`: it starts at a random initialization (`[03-dl-training/02-layers/04-weight-initialization]`'s concerns apply here too) and is UPDATED by gradient descent during training, just like any other layer's weights, so that semantically related tokens gradually drift toward similar vectors purely as a side effect of the training objective, no explicit "make these similar" instruction is ever given. `[02-embedding-backward]`, immediately following this question, derives the (perhaps surprising) gradient this lookup operation needs during backpropagation: since only the ROWS that were actually looked up receive any gradient signal at all (every other row in the table gets a gradient of exactly zero on that particular batch), a naive dense gradient computation would be enormously wasteful for a large vocabulary, which is exactly why real implementations use a specialized SPARSE update instead.

## Explanation

`embedding_forward` returns `embedding_table[token_ids]` directly, relying on NumPy's fancy (array-based) indexing: providing an array of integer indices (rather than a single scalar index) selects one row per index and stacks them together, automatically producing an output shaped like `token_ids` with the embedding table's row dimension (`embed_dim`) appended as a new trailing axis, and produces a fresh array rather than a view into `embedding_table`, leaving the original table untouched.
