---
name: tabular-foundation-models-in-context-prediction
title: 'In-Context Prediction'
tags: [tabular-foundation-models, attention, in-context-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

**In-context prediction**

Every single model in this curriculum before this track needed a training loop specific to _this_ dataset: `05-training-loop`'s gradient descent, `04-full-boosting-loop`'s sequential tree fitting, `05-em-algorithm`'s E/M iterations, all of them adjust parameters to fit the data they're given, one dataset at a time. TabPFN's actual, genuinely different idea is **in-context learning**: train one attention model's weights _once_, offline, on a huge variety of synthetic datasets, then freeze those weights completely. For any _new_ dataset, no further training happens at all, the training examples themselves become part of the input, laid out as extra rows in the table, and one forward pass through the frozen network produces predictions for new rows directly.

**Why there is no positional encoding**

A sequence Transformer (the kind Part 2's sequence-modeling questions build toward) has a real problem plain attention doesn't solve on its own: `scaled_dot_product_attention` (`01-row-wise-attention`) treats its inputs as an _unordered set_, nothing in `query @ key^T` depends on which position a token came from, so "the cat sat" and "sat cat the" would produce identical attention computations unless something explicitly tells the model about word order. A data table has no equivalent problem: row 5 of a dataset isn't "after" row 4 in any meaningful sense, shuffling every row of a training set (and its labels along with it) describes the exact same dataset.

### From theory to code

**In-context prediction**

Implement `build_incontext_table(train_features, train_targets, query_features)` and `in_context_predict(train_features, train_targets, query_features, row_weights, col_weights)`. Reuse `03-two-way-attention-block`'s `two_way_attention_block`.

**Why there is no positional encoding**

Implement `is_row_permutation_equivariant(table, row_weights, col_weights, permutation)`: checks that shuffling input rows and shuffling output rows are interchangeable. Reuse `03-two-way-attention-block`'s `two_way_attention_block`.

### Constraints

**In-context prediction**

- `build_incontext_table` returns shape `(n_train + n_query, n_features + 1, 1)`: training rows carry their real target in the last column; query rows get exactly `0` there (masked, not a guess).
- `in_context_predict` returns shape `(n_query,)`: the query rows' target-column values after exactly one forward pass through `two_way_attention_block`.
- `row_weights`/`col_weights` are fixed, given inputs, never updated inside `in_context_predict`, no training loop of any kind.

**Why there is no positional encoding**

- Runs `two_way_attention_block` on `table` and on `table[permutation]` (the same weights both times).
- Returns `True` iff the permuted-input output equals the original output with the same permutation applied to its rows.
- Returns a plain Python `bool`, not a NumPy boolean.

### Hints

**In-context prediction**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The table's last column holds the target, real values for training rows, `0` for query rows, since NumPy arrays initialize to `0` already if you build the array with `np.zeros` and only fill in what's known.

</details>

<details>
<summary>Hint 2</summary>

`in_context_predict` is exactly three steps: build the table, run `two_way_attention_block` once, then slice `output[n_train:, -1, 0]`, the query rows' post-attention target-column entries.

</details>

**Why there is no positional encoding**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the block's output on the original table once, and on `table[permutation]` once, two separate forward passes, same weights both times.

</details>

<details>
<summary>Hint 2</summary>

The property being checked is `block(table[permutation]) == block(table)[permutation]`, compare those two arrays with `np.allclose`, then convert the result to a plain `bool`.

</details>

## Theory

### The simple version

**In-context prediction**

```text
training rows: features AND their real target, both known
query rows:    features known, target UNKNOWN (masked to 0, not guessed)
   -> combine into ONE table
   -> ONE forward pass through a FIXED, already-trained attention block
predictions for the query rows, read directly off the output
```

**Why there is no positional encoding**

That's exactly what positional encoding is for in a sequence Transformer, an extra signal added to each token's embedding specifically to break this permutation symmetry, because word order is genuinely part of a sentence's meaning. This track's row-wise attention and column-wise attention were built with no positional encoding anywhere, and that isn't an oversight, it's the mathematically correct choice: a tabular model _should_ be permutation-equivariant in row order (shuffle the input rows, get the output rows shuffled the same way, nothing else changes) and, similarly, shouldn't have its predictions depend on which row happened to appear first.

### The formula

**In-context prediction**

This is exactly what `03-two-way-attention-block`'s row-wise and column-wise attention makes possible: a query row's target column can attend to the training rows' _known_ targets (via column-wise attention within that target column) and to its own known features (via row-wise attention within its own row), letting the fixed network effectively "look up" what similar training rows' targets were and combine that into a prediction, entirely within forward-pass computation, no gradient step involved for this specific dataset at all.

**Why there is no positional encoding**

```text
sequence attention:  order carries real meaning      -> needs positional encoding to distinguish positions
table row attention: order is arbitrary bookkeeping  -> should be, and is, permutation-equivariant without it
```

(Column order is a real, if softer, exception worth naming: a table's columns _do_ have fixed identity, "age" is always "age", so a practical implementation typically ties each column to a learned per-column embedding rather than leaving columns fully interchangeable the way rows are. That's a modeling choice layered on top, though, not a requirement of the attention mechanism itself the way positional encoding is for sequences.)

### How NumPy/PyTorch actually implements this

**In-context prediction**

Context only, untested by your submission: this is the actual mechanism behind TabPFN (Prior-Fitted Networks), a real, published tabular foundation model, its weights are trained once offline on millions of synthetic datasets, then frozen and shipped; predicting on a brand-new real dataset is a single forward pass exactly like this exercise's `in_context_predict`, with no fine-tuning step at inference time.

**Why there is no positional encoding**

Context only, untested by your submission: this is an architectural property check, not a PyTorch operation, real sequence Transformers add a positional encoding tensor (learned or sinusoidal, as `05-transformers-llm`'s own position-embedding questions cover) directly to token embeddings before attention runs, specifically to remove the permutation-equivariance this exercise verifies is desirable to _keep_ for tabular attention.

## Explanation

**In-context prediction.** `build_incontext_table` lays training rows and query rows into one table: training rows get their real `train_targets` value in the last column, query rows get exactly `0` there, an explicit "this is unknown" marker (not a guessed value, and not something the model should trust as real), the same masking idea that gives the block something to actually resolve during its forward pass.

`in_context_predict` builds that table, runs it through `two_way_attention_block` exactly once with `row_weights`/`col_weights` treated as fixed, given inputs (never updated inside this function, there's no loop here at all, unlike every earlier training question in this curriculum), and reads `output[n_train:, -1, 0]`, the query rows' entries in the target column, as the model's predictions. Changing `train_features`/`train_targets`/`query_features` changes what table gets built and thus what the single forward pass computes, but never changes `row_weights`/`col_weights` themselves, the same fixed weights would be reused for a completely different dataset handed to this exact function.

**Why there is no positional encoding.** `is_row_permutation_equivariant` runs `two_way_attention_block` twice: once on `table` as given, and once on `table[permutation]`, the same table with its rows reordered. If the block truly has no positional encoding anywhere (no term in `row_wise_attention`, `column_wise_attention`, or the residual connections that depends on a row's raw index rather than its content), then shuffling the input rows first and running the block afterward must give an output that is _exactly_ the original output with the same row shuffle applied, `original_output[permutation]`, comparing the two directly is what the function returns.

This is a genuinely different kind of check than the earlier questions' hand-computed values or oracle comparisons, it verifies an architectural _property_ the implementation should have, rather than checking one specific numeric result, precisely because the property in question, "does this depend on row order," is the whole point of the contrast this question names.
