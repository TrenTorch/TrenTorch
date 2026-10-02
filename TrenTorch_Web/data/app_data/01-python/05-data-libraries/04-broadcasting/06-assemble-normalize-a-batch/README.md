---
name: numpy-assemble-normalize-a-batch
title: 'Assemble: Normalize a Batch Using Broadcasting Only'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that combines every topic in this module — recognizing when broadcasting applies, computing broadcast-compatible shapes, correctly using `newaxis`, and diagnosing an incompatible case — into one realistic batch-preprocessing task.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Applying per-row and per-column operations using broadcasting, choosing the correct `newaxis` placement for each.
- Computing a broadcast result shape directly, without trial and error.
- Correctly detecting and reporting a genuinely incompatible shape pair, rather than letting an unhandled error propagate.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

`scaled = data * feature_scales` broadcasts `feature_scales` (shape `(num_features,)`) against `data`'s trailing dimension directly — no reshape needed. `biased = scaled + bias_per_sample[:, np.newaxis]` reshapes `bias_per_sample` to `(num_samples, 1)` so it stretches down the rows rather than trying (and generally failing) to align against the trailing `num_features` dimension. Step 3 attempts `biased + feature_scales` unreshaped and wraps it in `try`/`except ValueError`, since whether this succeeds depends entirely on whether `feature_scales`'s length happens to equal `num_features` (which it does here, so it actually succeeds) — the function still has to check rather than assume. `predicted_broadcast_shape` is computed with the same padding-and-max logic as the rule topic, applied to `biased.shape` and `bias_per_sample[:, np.newaxis].shape`.
