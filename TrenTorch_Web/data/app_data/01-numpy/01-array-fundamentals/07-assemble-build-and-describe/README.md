---
name: numpy-assemble-build-and-describe
title: 'Assemble: Build and Describe an Array From a Spec'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that combines every topic in this module — creating arrays multiple ways, controlling dtype, and reporting full structural metadata — into one realistic data-preparation task.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Choosing the correct array-creation function (`np.array`, `np.zeros`, `np.arange`, `np.linspace`) based on a given specification's `"kind"`.
- Applying an explicit `dtype` when one is given.
- Reporting the resulting array's full structural metadata (`shape`, `ndim`, `size`, `dtype`).

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

Dispatch on `spec["kind"]` with an if/elif chain, building the array with the matching NumPy call and passing `dtype=spec["dtype"]` whenever it is not `None` (all four creation functions accept a `dtype` keyword). Then read `shape`, `ndim`, `size`, and `str(dtype)` off the built array itself, rather than recomputing them separately — this guarantees the reported metadata always matches the real array.
