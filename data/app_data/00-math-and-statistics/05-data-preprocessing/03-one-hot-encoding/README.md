---
name: math-one-hot-encoding
title: One-hot encoding a categorical column
tags: [data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A column of city names, `"NYC"`, `"LA"`, `"NYC"`, `"Chicago"`, can't be fed directly into `linear` (this curriculum's very first question) or any matrix-multiply-based model, there's no meaningful numeric distance between "NYC" and "LA" the way there is between the number `3` and `5`. Assigning `NYC=0, LA=1, Chicago=2` doesn't fix this, it silently implies Chicago is "twice as far" from NYC as LA is, a completely fabricated numeric relationship that doesn't exist in the underlying category.

One-hot encoding sidesteps the problem entirely: instead of one arbitrary number per category, use one dedicated 0/1 column per possible category. No category is numerically "closer" to any other, every pairwise distance between two different categories is identical, exactly the "no fabricated relationship" property a categorical variable actually has.

### From theory to code

Theory turns a length-`n` categorical column into an `(n, k)` binary matrix (`k` = number of distinct categories), one column per category, a single `1` per row marking that row's category. Implement the category-discovery step first, then the encoding itself, built to accept an explicit category list (not just always deriving one fresh) for the reason Theory's PyTorch section explains.

Implement `get_unique_categories(column)` and `one_hot_encode(column, categories=None)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `get_unique_categories` returns categories in a fixed, sorted order (so encoding is reproducible).
- `one_hot_encode`'s output shape is `(len(column), len(categories))`.
- Every row of the output sums to exactly `1` (exactly one category per row).
- If `categories` is passed explicitly, use it as-is, don't recompute from `column`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.unique` already returns sorted, distinct values in one call.

</details>

<details>
<summary>Hint 2</summary>

Build a `{category: column_index}` lookup dict once, then loop over rows, setting exactly one `1` per row using that lookup.

</details>

## Theory

### The simple version

Asking "how far is Chicago from Los Angeles" on a 0/1/2-style numeric encoding of cities is nonsensical, but that's exactly what feeding raw category codes into a model implicitly asks it to compute. One-hot encoding avoids the question entirely: instead of one number, use a whole row of switches, one per possible city, flip exactly one to "on." Now there's no fabricated ordering or distance between categories at all, just "which one is it."

### The formula

For a categorical column with `k` distinct values, one-hot encoding builds an `(n, k)` matrix:

```text
one_hot[i, j] = 1   if column[i] == categories[j]
              = 0   otherwise
```

Every row has EXACTLY one `1` (each sample belongs to exactly one category) and sums to `1`, this is a useful sanity check: a correctly one-hot-encoded matrix's row sums are always all `1`s.

The category ORDER matters more than it might first appear. A model trained with `["bird", "cat", "dog"]` mapped to columns `[0, 1, 2]` needs EVERY future input, including test data seen after training, encoded with that exact same column order, `"dog"` must always land in column 2, never wherever `np.unique` happens to sort it on a DIFFERENT dataset that might not even contain every category. This is why `one_hot_encode` accepts an explicit `categories` argument rather than always recomputing categories fresh from whatever data it's currently given.

### How PyTorch actually implements this

`torch.nn.functional.one_hot(tensor, num_classes)` computes exactly this matrix (for integer class-index input, so a real pipeline typically maps string categories to integers first, then one-hot encodes). In practice, though, one-hot encoding a categorical feature and feeding it through a `linear` layer is mathematically equivalent to a much cheaper operation: `torch.nn.Embedding(num_categories, embedding_dim)` looks up a learned vector directly by category index, skipping the explicit one-hot matrix and matmul entirely. This is why one-hot encoding shows up constantly for LABELS (`02-cross-entropy`'s target, conceptually one-hot even when represented as a plain integer index) but is rarely used for high-cardinality categorical INPUT features in real deep learning pipelines, `nn.Embedding` achieves the same "no fabricated ordering" property far more efficiently once the category count gets large.

## Explanation

`get_unique_categories` returns `np.unique(column)`, which already returns sorted, distinct values, giving deterministic column ordering for free.

`one_hot_encode` derives `categories` via `get_unique_categories` only if none was supplied (respecting an explicitly-passed category list, per Theory's train/test consistency point), builds a `{category: column_index}` lookup, and loops over every row, setting a single `1` at the column matching that row's category, leaving every other entry at its initialized `0`.
