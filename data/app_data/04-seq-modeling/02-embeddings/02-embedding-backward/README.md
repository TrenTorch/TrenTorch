---
name: seq-embeddings-embedding-backward
title: 'Embedding backward (scatter-add gradient)'
tags: [nlp, transformers, embeddings, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-token-embedding-lookup]`'s `embedding_forward` is a SELECTION operation: it picks out specific rows from `embedding_table` and returns them. `[02-deep-learning-core/04-autograd]`'s `matmul_backward` derived how gradients flow backward through a matrix multiplication, but embedding lookup isn't a matmul, it's indexing, and indexing needs its own backward rule. The intuition is straightforward once stated: only the rows that were ACTUALLY looked up during the forward pass can possibly have contributed to the loss, so every row that was never selected gets a gradient of exactly ZERO, while a row that WAS selected gets the upstream gradient from wherever it was used.

The genuinely tricky part, and the reason this question exists separately from a generic "backward for indexing" exercise: the SAME token id very commonly appears MULTIPLE times within a single batch (the word "the" might appear a dozen times across a batch of sentences), and each occurrence independently contributes its own gradient to that SAME row of the embedding table. The correct gradient for that row is the SUM of every occurrence's individual contribution, not just the last one, or the first one, a naive implementation that simply ASSIGNS `grad_table[id] = grad_output[position]` for each position, overwriting rather than accumulating, would silently drop every occurrence except the last one seen, quietly corrupting training for every token that appears more than once per batch (which, for common words, is nearly always).

### From theory to code

Implement `embedding_backward(grad_output, token_ids, vocab_size)`. Build a zero-initialized `grad_table` of shape `(vocab_size, embed_dim)`. For every position in `token_ids`, ADD (not overwrite) that position's corresponding slice of `grad_output` into `grad_table` at the row given by that position's token id.

### Constraints

- `grad_table` must start at all zeros: rows never referenced by `token_ids` must remain exactly zero.
- When a token id appears MULTIPLE times in `token_ids`, that row's final gradient must be the SUM of every occurrence's own gradient contribution.
- `grad_table`'s shape must be exactly `(vocab_size, embed_dim)`, regardless of `token_ids`'s own shape (a single sequence or a whole batch).
- Do not use a Python `for` loop with plain indexed assignment (`grad_table[id] = ...`); this silently drops accumulation for repeated ids.

### Hints

<details>
<summary>Hint 1: Flattening first</summary>

`token_ids` might be multi-dimensional (a whole batch). Flatten both `token_ids` and `grad_output` down to a simple `(num_positions,)` array of ids and a matching `(num_positions, embed_dim)` array of gradients before processing: `token_ids.reshape(-1)` and `grad_output.reshape(-1, embed_dim)`.

</details>

<details>
<summary>Hint 2: The accumulation operation</summary>

`np.add.at(grad_table, flat_ids, flat_grad)` is NumPy's built-in "scatter-add": unlike `grad_table[flat_ids] += flat_grad` (which, for REPEATED indices, only applies the LAST write due to how NumPy's fancy-indexing assignment is implemented, silently dropping earlier occurrences), `np.add.at` correctly accumulates every single occurrence, even when the same index appears many times in `flat_ids`.

</details>

<details>
<summary>Hint 3</summary>

`embed_dim = grad_output.shape[-1]` reads the embedding dimension directly off `grad_output`'s own last axis, no need to pass it in separately.

</details>

## Theory

### The simple version

A tip jar shared by a shift of servers, where every customer's tip gets added to the SAME jar, regardless of how many customers there were or how many times the same customer came back for a second visit that same day. If, instead, each new tip somehow REPLACED whatever was in the jar rather than adding to it, only the LAST customer's tip would remain by the end of the shift, every earlier contribution silently vanished. The embedding table's gradient works like the tip jar: every position in the input that referenced a given row contributes its OWN gradient, and all of those contributions must be summed together, not overwritten.

### The formula

```
grad_table = zeros(vocab_size, embed_dim)
for position i in token_ids (flattened):
    grad_table[token_ids[i]] += grad_output[i]    # accumulate, never overwrite
```

This IS the general chain rule applied to a SELECTION/gather operation: `[02-deep-learning-core/04-autograd/04-graph-node]`'s `Value` class uses `+=` accumulation in its own `_backward` closures for exactly this same reason, whenever a single value is used more than once in a computation graph, its gradient contributions from every use must sum together, embedding lookup is simply the case where "used more than once" happens at the granularity of entire table rows rather than individual scalar values.

### How PyTorch actually implements this

`torch.nn.Embedding`'s backward pass implements precisely this scatter-add operation (dispatching to `torch.Tensor.index_add_` or an equivalent specialized ATen kernel under the hood), and it's specifically why embedding gradients are commonly represented as SPARSE tensors internally in PyTorch (`nn.Embedding(..., sparse=True)`) for very large vocabularies: since only the handful of rows that actually appeared in a given batch have any nonzero gradient at all (out of a vocabulary that might contain hundreds of thousands of entries), materializing and storing a full DENSE `(vocab_size, embed_dim)` gradient array every single step, as this question's straightforward NumPy implementation does for clarity, would waste enormous amounts of memory and compute at production scale. `optimizer.step()` (any of the `[03-dl-training/01-optimizers]` update rules) then applies this row-level gradient to nudge exactly the embeddings that were actually used during that batch, leaving every other row in the table completely untouched.

## Explanation

`embedding_backward` first flattens both `token_ids` and `grad_output` down to one-dimensional-index / two-dimensional-gradient form (`(num_positions,)` and `(num_positions, embed_dim)` respectively), regardless of the original batch shape. It then calls `np.add.at(grad_table, flat_ids, flat_grad)`, NumPy's genuinely accumulating scatter-add: for every position, it adds that position's gradient slice into `grad_table` at the row given by that position's id, correctly SUMMING contributions when the same id appears at multiple positions, rather than the silent last-write-wins behavior a plain `grad_table[flat_ids] += flat_grad` would produce for repeated indices.
