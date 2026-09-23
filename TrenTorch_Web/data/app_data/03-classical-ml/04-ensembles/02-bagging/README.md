---
name: ensembles-bagging
title: 'Stretch: bagging concept'
tags: [classical-ml, ensembles, random-forest, stretch]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Majority voting needs trees that are not exact copies. Bagging creates that diversity by training the same learner on many same-sized random samples drawn with replacement. A row may appear repeatedly or not at all, but its label must always travel with it.

### From theory to code

Implement `bootstrap_sample` and `train_random_forest`. Draw paired bootstrap rows, then train exactly `n_trees` with the existing `build_tree` function.

### Constraints

- Bootstrap input and label arrays preserve their original shapes.
- Draw exactly `input.shape[0]` indices from `[0, n_samples)` with replacement.
- Use the same index array for `input` and `labels`.
- Build one `np.random.default_rng(seed)` before the tree loop.
- Return exactly `n_trees` independently bootstrapped `build_tree` results.
- Equal fixed seeds reproduce a call; a reused generator must advance between trees.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Replacement means an index-drawing operation may repeat a value; it does not need a permutation.

</details>

<details><summary>Hint 2</summary>

Pass one advancing generator into each bootstrap call rather than re-creating it inside the loop.

</details>

## Theory

### The simple version

Bagging gives every tree a shuffled bag containing the same number of draws as the original dataset. Some examples occur several times and some are absent, creating different training views while preserving the underlying signal.

### The formula

```text
rng = default_rng(seed)
indices = rng.integers(0, n_samples, size=n_samples)
boot_input, boot_labels = input[indices], labels[indices]
trees = [build_tree(bootstrap_sample(...), max_depth) for each tree]
```

The implementation builds the generator once; passing that `Generator` to `default_rng` in `bootstrap_sample` keeps its state advancing.

### How PyTorch actually implements this

Context only, untested by your submission: bootstrap aggregation is a tree-ensemble training pattern, not a core `torch.nn` primitive. The random index draw corresponds to integer sampling with replacement.

## Explanation

`bootstrap_sample` creates `rng`, records `n_samples`, and uses `rng.integers(0, n_samples, size=n_samples)` for replacement draws. Returning `input[indices], labels[indices]` preserves row-label pairing. `train_random_forest` creates `rng` once outside its loop, gathers each `boot_input, boot_labels`, and appends `build_tree(boot_input, boot_labels, max_depth)`. Reusing the generator makes equal seeded runs reproducible while ensuring different trees do not receive repeated identical draws.
