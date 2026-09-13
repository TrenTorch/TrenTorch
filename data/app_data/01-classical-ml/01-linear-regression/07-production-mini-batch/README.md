---
name: linear-regression-production-mini-batch
title: 'Production Engineering: Mini-Batch Training'
tags: [classical-ml, linear-regression, production-engineering, mini-batch]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`05-training-loop` uses every row for every update, which is clear but becomes expensive as datasets grow. Mini-batches let training update from small groups while still eventually seeing the whole dataset. The practical challenge is preserving feature-target pairing, handling the final short group, and making shuffled training reproducible when a seed is supplied.

### From theory to code

Implement `train_linear_regression_production`. Use the earlier MSE gradient and gradient-descent step for one shuffled batch at a time; Theory explains the epoch-level ordering and the single long-lived random generator.

### Constraints

- `input` has shape `(n_samples, in_features)` and `target` has shape `(n_samples,)`.
- Return zero-initialized then trained `weight` with shape `(1, in_features)` and `bias` with shape `(1,)`.
- Reshape targets to `(n_samples, 1)` once before training.
- Shuffle sample indices once per epoch and take one step for each batch, including a final batch smaller than `batch_size`.
- Construct `np.random.default_rng(seed)` once before the epoch loop.
- The same non-`None` seed and arguments must produce bit-identical parameters; `seed=None` must not force a fixed order.
- Slice only the current batch from `input` and `target`; reuse `mse_gradient` and `gd_step`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Shuffle row indices, not features and targets separately. One index array preserves their pairing.

</details>

<details>
<summary>Hint 2</summary>

`range(0, n_samples, batch_size)` naturally visits the start of a final short batch.

</details>

<details>
<summary>Hint 3</summary>

Create one generator before training. In each epoch, call its `permutation(n_samples)`, then use `order[start : start + batch_size]` to select both batch arrays.

</details>

## Theory

### The simple version

Rather than asking an entire warehouse of examples for advice before moving, ask one small box at a time. The resulting advice is noisier, but it is cheap to obtain and leads to many updates per pass through the warehouse. Shuffling stops a fixed data order from repeatedly steering those updates in the same sequence.

### The formula

For each epoch, the implementation draws a permutation `order` of `0..n_samples-1`. For every slice `I = order[start : start + batch_size]`, it performs:

```text
(dW, db) = mse_gradient(input[I], weight, bias, target_2d[I])
(weight, bias) = gd_step(weight, bias, dW, db, lr)
```

The stepped range includes the remainder because Python slicing stops at the array end.

### How PyTorch actually implements this

Context only, untested by your submission: a `torch.utils.data.DataLoader` commonly supplies shuffled mini-batches to a `torch.nn.Linear` model, while `torch.optim.SGD` updates its parameters. This test suite also contains an offline-generated oracle for the special one-full-batch case, compared with a zero-initialized PyTorch linear model trained for 50 steps.

## Explanation

`n_samples, in_features = input.shape` drives both the parameter shape and all batching bounds. After `target_2d` and `rng` are created once, the outer loop obtains a fresh `order = rng.permutation(n_samples)` per epoch. The inner stepped `range` creates `batch_idx`; indexing `input[batch_idx]` and `target_2d[batch_idx]` together preserves rows and permits the final shorter slice. Each pair of `mse_gradient` and `gd_step` calls updates immediately, so no full-dataset batch is materialized. Because `rng` is not reset inside the loop, one seed yields a reproducible sequence of different epoch permutations.
