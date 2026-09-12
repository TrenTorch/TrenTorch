---
name: tabular-foundation-models-in-context-prediction
title: 'In-context prediction: single forward pass, no per-dataset training loop'
tags: [tabular-foundation-models, attention, in-context-learning]
difficulty: Intermediate
---

## Statement

Implement:

```python
def build_incontext_table(train_features, train_targets, query_features) -> np.ndarray: ...
def in_context_predict(train_features, train_targets, query_features, row_weights, col_weights) -> np.ndarray: ...
```

- Reuse `03-two-way-attention-block`'s `two_way_attention_block`.

## Theory

Every single model in this curriculum before this track needed a training loop specific to _this_ dataset: `05-training-loop`'s gradient descent, `04-full-boosting-loop`'s sequential tree fitting, `05-em-algorithm`'s E/M iterations, all of them adjust parameters to fit the data they're given, one dataset at a time. TabPFN's actual, genuinely different idea is **in-context learning**: train one attention model's weights _once_, offline, on a huge variety of synthetic datasets, then freeze those weights completely. For any _new_ dataset, no further training happens at all, the training examples themselves become part of the input, laid out as extra rows in the table, and one forward pass through the frozen network produces predictions for new rows directly.

```text
training rows: features AND their real target, both known
query rows:    features known, target UNKNOWN (masked to 0, not guessed)
   ↓ combine into ONE table
   ↓ ONE forward pass through a FIXED, already-trained attention block
predictions for the query rows, read directly off the output
```

This is exactly what `03-two-way-attention-block`'s row-wise and column-wise attention makes possible: a query row's target column can attend to the training rows' _known_ targets (via column-wise attention within that target column) and to its own known features (via row-wise attention within its own row), letting the fixed network effectively "look up" what similar training rows' targets were and combine that into a prediction, entirely within forward-pass computation, no gradient step involved for this specific dataset at all.

## Explanation

`build_incontext_table` lays training rows and query rows into one table: training rows get their real `train_targets` value in the last column, query rows get exactly `0` there, an explicit "this is unknown" marker (not a guessed value, and not something the model should trust as real), the same masking idea that gives the block something to actually resolve during its forward pass.

`in_context_predict` builds that table, runs it through `two_way_attention_block` exactly once with `row_weights`/`col_weights` treated as fixed, given inputs (never updated inside this function, there's no loop here at all, unlike every earlier training question in this curriculum), and reads `output[n_train:, -1, 0]`, the query rows' entries in the target column, as the model's predictions. Changing `train_features`/`train_targets`/`query_features` changes what table gets built and thus what the single forward pass computes, but never changes `row_weights`/`col_weights` themselves, the same fixed weights would be reused for a completely different dataset handed to this exact function.
