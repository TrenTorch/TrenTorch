---
name: numpy-assemble-trace-ownership
title: 'Assemble: Trace Ownership Through a Multi-Step Pipeline'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that builds a multi-step chain of array operations and correctly reports, at every step, whether the result is a view or a copy and what its ultimate data owner is.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module — what a view is, which operations produce views vs copies, `.copy()`, mutation propagation, and `.base` — into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Performing a sequence of operations, some views and some copies.
- Identifying, at each step, whether that step's result shares memory with the original array (`np.shares_memory`).
- Using `.base` (following a chain if needed) to determine each result's ultimate data owner.
- Predicting and verifying the consequence of a mutation applied partway through the chain.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

`step_a = arr[2:9]` is a view (basic slice). `step_b = step_a[[0, 2, 4]]` is a copy (fancy indexing). `step_c = step_a.copy()` is an explicit copy, taken _before_ the mutation. Mutating `step_a[0] = -1` writes into the shared buffer, so it's visible through `arr` (at `arr[2]`, since `step_a` starts at `arr`'s index 2) and through anything still sharing that buffer — but `step_b` and `step_c` were already independent by the time the mutation happened, so neither reflects it. `step_a`'s ultimate owner is found by walking `.base` from `step_a` until reaching `arr` itself.
