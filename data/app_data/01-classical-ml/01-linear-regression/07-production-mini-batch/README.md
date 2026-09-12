---
name: linear-regression-production-mini-batch
title: 'Production Engineering: Mini-Batch Training'
tags: [classical-ml, linear-regression, production-engineering, mini-batch]
difficulty: Advanced
---

## Statement

Implement:

```python
def train_linear_regression_production(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
    batch_size: int,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Mini-batch gradient descent, reusing mse_gradient / gd_step per batch
    instead of once per epoch over the full dataset.
    """
```

Your function should:

1. Shuffle the sample order at the start of every epoch (a different shuffle each epoch, this is what keeps mini-batch gradients from being biased by data order).
2. Split the shuffled data into batches of `batch_size` (the last batch may be smaller if `n_samples` doesn't divide evenly, must not crash or silently drop it).
3. Take one gradient step per batch, not per epoch.
4. Never materialize more than one batch's worth of `input` at a time inside the per-batch step (no operation should touch the full `input` array once batching starts).
5. Accept an optional `seed`: when given, two calls with the same `seed` (and the same everything else) must return exactly the same `weight, bias`, including across epochs, not just within the first one. When `seed` is `None`, training is genuinely random run to run.
6. `weight`/`bias` follow `01-hypothesis-function`'s convention: `weight` shape `(1, in_features)`, `bias` shape `(1,)`, never squeezed.

## Theory

The naive training loop has three problems no production system tolerates:

**Full-batch doesn't scale.** Every single step recomputes the gradient over the _entire_ dataset. Fine for 300 rows. Impossible for 300 million, `input` alone won't fit in memory, let alone `grad_prediction.T @ input`. Production training instead uses **mini-batch gradient descent**: shuffle the data once per epoch, split it into small batches, take one gradient step per batch. You never need more than one batch in memory at a time, and you get more update steps per epoch for free.

**Hand-derived gradients don't scale either.** The manual `grad_weight = (2/N) input.T @ (prediction - target)` formula was derivable by hand because linear regression is the simplest possible model. Nobody hand-derives gradients for a 96-layer transformer. Real PyTorch code never writes a gradient formula for this, it calls `.backward()` and lets autograd compute it. This is exactly why the Deep Learning Foundations section builds an autograd engine: it's the thing that makes manual calculus disappear from every model after this one.

**A third problem, easy to miss: reproducibility.** The naive loop never shuffles anything, so it's already deterministic. The moment you add shuffling, you've added randomness, and a real production training run needs to be re-runnable with the identical result, for debugging a regression, for a paper's reported numbers, for CI comparing today's run against yesterday's. That means a `seed` parameter isn't a nice-to-have, it's the difference between "reproducible experiment" and "we have no idea why this run's numbers are different."

There's a genuine gotcha in wiring this correctly: `np.random.default_rng(seed)` has to be created **once, before the epoch loop begins**, not once per epoch. Re-seeding inside the loop (`rng = np.random.default_rng(seed)` on every iteration) would give every single epoch the exact same shuffle order, defeating the entire point of shuffling per epoch in the first place, even though it looks reasonable at a glance and even "feels" like the more careful, explicit thing to do. Create the generator once; let its internal state keep advancing across epochs, the same generator object producing a new-but-reproducible permutation each time `.permutation()` is called on it again.

A real production version of exactly what this track built looks like this:

```python
torch.manual_seed(seed)                  # the reproducibility fix, done once, up front
model = torch.nn.Linear(n_features, 1)
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=lr)

for input_batch, target_batch in dataloader:  # mini-batches, not the whole dataset
    optimizer.zero_grad()
    prediction = model(input_batch)           # the hypothesis function
    loss = loss_fn(prediction, target_batch)  # the loss
    loss.backward()                           # the gradient, computed automatically
    optimizer.step()                          # the update
```

Every hand-written piece from this track maps onto exactly one line here, including `torch.manual_seed`, the same reproducibility fix as `seed` below, in the same spot: set once, before training starts, never inside the loop. The question below builds the NumPy-only version of this, same mini-batch structure, same reproducibility guarantee, still no `import torch` in your submission, but engineered the way production code actually is.

## Explanation

`rng.permutation(n_samples)` is regenerated fresh inside the epoch loop, not once outside it, a single reused permutation would train on the identical batch order every epoch, defeating the entire point of shuffling.

`batch_idx = order[start:start + batch_size]` slices the _shuffled index array_, not `input` directly, so `input` and `target_2d` stay correctly paired to the same samples no matter how they're reordered.

The final, possibly-shorter batch needs no special case: `range(0, n_samples, batch_size)`'s last `start` value naturally produces a shorter slice on its own, no `if` branch needed for the remainder.

Reusing `mse_gradient` / `gd_step` unchanged, just called on `input_batch`/`target_batch` instead of the full dataset, is the actual point of the exercise: production and naive training aren't different algorithms, they're the same functions called at a different granularity.

`rng = np.random.default_rng(seed)` sits _outside_ the epoch loop, called exactly once, this is the opposite mistake from the permutation bug above, and just as easy to make. Creating a fresh `default_rng(seed)` on every epoch would seed the generator identically each time, so every epoch would draw the _same_ "random" permutation, reproducible, but uselessly so, since it defeats per-epoch shuffling entirely. One generator, created once, whose internal state keeps advancing across every `.permutation()` call, is what gives reproducible _and_ genuinely different-per-epoch shuffles at the same time.
