---
name: tabular-foundation-models-in-context-prediction
title: 'In-context prediction: single forward pass, no per-dataset training loop'
tags: [tabular-foundation-models, attention, in-context-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every single model in this curriculum before this track needed a training loop specific to *this* dataset: `05-training-loop`'s gradient descent, `04-full-boosting-loop`'s sequential tree fitting, `05-em-algorithm`'s E/M iterations — all of them adjust parameters to fit the data they're given, one dataset at a time. TabPFN's actual, genuinely different idea is **in-context learning**: train one attention model's weights *once*, offline, on a huge variety of synthetic datasets, then freeze those weights completely. For any *new* dataset, no further training happens at all — the training examples themselves become part of the input, laid out as extra rows in the table, and one forward pass through the frozen network produces predictions for new rows directly.

### From theory to code

Implement `build_incontext_table(train_features, train_targets, query_features)` and `in_context_predict(train_features, train_targets, query_features, row_weights, col_weights)`. Reuse `03-two-way-attention-block`'s `two_way_attention_block`.

### Constraints

- `build_incontext_table` returns shape `(n_train + n_query, n_features + 1, 1)`: training rows carry their real target in the last column; query rows get exactly `0` there (masked, not a guess).
- `in_context_predict` returns shape `(n_query,)`: the query rows' target-column values after exactly one forward pass through `two_way_attention_block`.
- `row_weights`/`col_weights` are fixed, given inputs — never updated inside `in_context_predict`, no training loop of any kind.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The table's last column holds the target — real values for training rows, `0` for query rows, since NumPy arrays initialize to `0` already if you build the array with `np.zeros` and only fill in what's known.

</details>

<details>
<summary>Hint 2</summary>

`in_context_predict` is exactly three steps: build the table, run `two_way_attention_block` once, then slice `output[n_train:, -1, 0]` — the query rows' post-attention target-column entries.

</details>

## Theory

### The simple version

```text
training rows: features AND their real target, both known
query rows:    features known, target UNKNOWN (masked to 0, not guessed)
   -> combine into ONE table
   -> ONE forward pass through a FIXED, already-trained attention block
predictions for the query rows, read directly off the output
```

### The formula

This is exactly what `03-two-way-attention-block`'s row-wise and column-wise attention makes possible: a query row's target column can attend to the training rows' *known* targets (via column-wise attention within that target column) and to its own known features (via row-wise attention within its own row), letting the fixed network effectively "look up" what similar training rows' targets were and combine that into a prediction, entirely within forward-pass computation — no gradient step involved for this specific dataset at all.

### How PyTorch actually implements this

Context only, untested by your submission: this is the actual mechanism behind TabPFN (Prior-Fitted Networks), a real, published tabular foundation model — its weights are trained once offline on millions of synthetic datasets, then frozen and shipped; predicting on a brand-new real dataset is a single forward pass exactly like this exercise's `in_context_predict`, with no fine-tuning step at inference time.

## Explanation

`build_incontext_table` lays training rows and query rows into one table: training rows get their real `train_targets` value in the last column, query rows get exactly `0` there — an explicit "this is unknown" marker (not a guessed value, and not something the model should trust as real), the same masking idea that gives the block something to actually resolve during its forward pass.

`in_context_predict` builds that table, runs it through `two_way_attention_block` exactly once with `row_weights`/`col_weights` treated as fixed, given inputs (never updated inside this function — there's no loop here at all, unlike every earlier training question in this curriculum), and reads `output[n_train:, -1, 0]`, the query rows' entries in the target column, as the model's predictions. Changing `train_features`/`train_targets`/`query_features` changes what table gets built and thus what the single forward pass computes, but never changes `row_weights`/`col_weights` themselves — the same fixed weights would be reused for a completely different dataset handed to this exact function.
