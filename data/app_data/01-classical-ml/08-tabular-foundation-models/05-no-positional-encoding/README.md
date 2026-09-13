---
name: tabular-foundation-models-no-positional-encoding
title: 'Contrast note: why no positional encoding here, unlike Part 2'
tags: [tabular-foundation-models, attention]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A sequence Transformer (the kind Part 2's sequence-modeling questions build toward) has a real problem plain attention doesn't solve on its own: `scaled_dot_product_attention` (`01-row-wise-attention`) treats its inputs as an _unordered set_ — nothing in `query @ key^T` depends on which position a token came from, so "the cat sat" and "sat cat the" would produce identical attention computations unless something explicitly tells the model about word order. A data table has no equivalent problem: row 5 of a dataset isn't "after" row 4 in any meaningful sense, shuffling every row of a training set (and its labels along with it) describes the exact same dataset.

### From theory to code

Implement `is_row_permutation_equivariant(table, row_weights, col_weights, permutation)`: checks that shuffling input rows and shuffling output rows are interchangeable. Reuse `03-two-way-attention-block`'s `two_way_attention_block`.

### Constraints

- Runs `two_way_attention_block` on `table` and on `table[permutation]` (the same weights both times).
- Returns `True` iff the permuted-input output equals the original output with the same permutation applied to its rows.
- Returns a plain Python `bool`, not a NumPy boolean.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the block's output on the original table once, and on `table[permutation]` once — two separate forward passes, same weights both times.

</details>

<details>
<summary>Hint 2</summary>

The property being checked is `block(table[permutation]) == block(table)[permutation]` — compare those two arrays with `np.allclose`, then convert the result to a plain `bool`.

</details>

## Theory

### The simple version

That's exactly what positional encoding is for in a sequence Transformer — an extra signal added to each token's embedding specifically to break this permutation symmetry, because word order is genuinely part of a sentence's meaning. This track's row-wise attention and column-wise attention were built with no positional encoding anywhere, and that isn't an oversight — it's the mathematically correct choice: a tabular model _should_ be permutation-equivariant in row order (shuffle the input rows, get the output rows shuffled the same way, nothing else changes) and, similarly, shouldn't have its predictions depend on which row happened to appear first.

### The formula

```text
sequence attention:  order carries real meaning      -> needs positional encoding to distinguish positions
table row attention: order is arbitrary bookkeeping  -> should be, and is, permutation-equivariant without it
```

(Column order is a real, if softer, exception worth naming: a table's columns _do_ have fixed identity — "age" is always "age" — so a practical implementation typically ties each column to a learned per-column embedding rather than leaving columns fully interchangeable the way rows are. That's a modeling choice layered on top, though, not a requirement of the attention mechanism itself the way positional encoding is for sequences.)

### How PyTorch actually implements this

Context only, untested by your submission: this is an architectural property check, not a PyTorch operation — real sequence Transformers add a positional encoding tensor (learned or sinusoidal, as `05-transformers-llm`'s own position-embedding questions cover) directly to token embeddings before attention runs, specifically to remove the permutation-equivariance this exercise verifies is desirable to _keep_ for tabular attention.

## Explanation

`is_row_permutation_equivariant` runs `two_way_attention_block` twice: once on `table` as given, and once on `table[permutation]`, the same table with its rows reordered. If the block truly has no positional encoding anywhere (no term in `row_wise_attention`, `column_wise_attention`, or the residual connections that depends on a row's raw index rather than its content), then shuffling the input rows first and running the block afterward must give an output that is _exactly_ the original output with the same row shuffle applied, `original_output[permutation]` — comparing the two directly is what the function returns.

This is a genuinely different kind of check than the earlier questions' hand-computed values or oracle comparisons — it verifies an architectural _property_ the implementation should have, rather than checking one specific numeric result, precisely because the property in question, "does this depend on row order," is the whole point of the contrast this question names.
