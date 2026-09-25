---
name: numpy-assemble-reproducible-synthetic-dataset
title: 'Assemble: Reproducible Synthetic Dataset with Initialized Weights'
tags: [numpy-random]
difficulty: Advanced
---

## Statement

Implement one function that uses a single seeded generator to build a synthetic regression dataset, split it into train and test sets, and initialize a weight matrix.

## Theory

This problem introduces no new concepts. It combines every topic in this module:

- Create **one** `Generator` from the seed and use only that generator.
- Draw in a **fixed, specified order** — draw order determines which values each step receives.
- Use standard-normal, uniform, and normal draws with the correct shapes and ranges.
- Build the train/test split with a boolean mask from a uniform draw, and compute targets with a matrix-vector product.

The dataset follows $y = Xw + \varepsilon$, where $X$ has shape $(n, d)$, $w$ has shape $(d,)$, and $\varepsilon$ has shape $(n,)$.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

Draw in exactly the specified order from one `rng`: `X`, `true_w`, `noise`, `split`, `W_init`. Compute `y = X @ true_w + noise`. Build `is_test = split < test_fraction` and index both `X`/`y` with `is_test` and `~is_test` to get the test/train splits, preserving row order since boolean masking always selects in original order. Any deviation from this exact draw sequence would desynchronize every downstream value from the reference implementation, since each draw consumes a specific slice of the generator's stream.
