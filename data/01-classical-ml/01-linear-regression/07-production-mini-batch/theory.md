The naive training loop has three problems no production system tolerates:

**Full-batch doesn't scale.** Every single step recomputes the gradient over the _entire_ dataset. Fine for 300 rows. Impossible for 300 million — `X` alone won't fit in memory, let alone `X.T @ error`. Production training instead uses **mini-batch gradient descent**: shuffle the data once per epoch, split it into small batches, take one gradient step per batch. You never need more than one batch in memory at a time, and you get more update steps per epoch for free.

**Hand-derived gradients don't scale either.** The manual `dw = (2/n) X.T @ (y_hat - y)` formula was derivable by hand because linear regression is the simplest possible model. Nobody hand-derives gradients for a 96-layer transformer. Real PyTorch code never writes a gradient formula for this — it calls `.backward()` and lets autograd compute it. This is exactly why the Deep Learning Foundations section builds an autograd engine: it's the thing that makes manual calculus disappear from every model after this one.

**A third problem, easy to miss: reproducibility.** The naive loop never shuffles anything, so it's already deterministic. The moment you add shuffling, you've added randomness — and a real production training run needs to be re-runnable with the identical result, for debugging a regression, for a paper's reported numbers, for CI comparing today's run against yesterday's. That means a `seed` parameter isn't a nice-to-have, it's the difference between "reproducible experiment" and "we have no idea why this run's numbers are different."

There's a genuine gotcha in wiring this correctly: `np.random.default_rng(seed)` has to be created **once, before the epoch loop begins** — not once per epoch. Re-seeding inside the loop (`rng = np.random.default_rng(seed)` on every iteration) would give every single epoch the exact same shuffle order, defeating the entire point of shuffling per epoch in the first place, even though it looks reasonable at a glance and even "feels" like the more careful, explicit thing to do. Create the generator once; let its internal state keep advancing across epochs, the same generator object producing a new-but-reproducible permutation each time `.permutation()` is called on it again.

A real production version of exactly what this track built looks like this:

```python
torch.manual_seed(seed)                  # the reproducibility fix, done once, up front
model = torch.nn.Linear(n_features, 1)
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=lr)

for X_batch, y_batch in dataloader:      # mini-batches, not the whole dataset
    optimizer.zero_grad()
    y_hat = model(X_batch).squeeze()     # the hypothesis function
    loss = loss_fn(y_hat, y_batch)       # the loss
    loss.backward()                      # the gradient, computed automatically
    optimizer.step()                     # the update
```

Every hand-written piece from this track maps onto exactly one line here — including `torch.manual_seed`, the same reproducibility fix as `seed` below, in the same spot: set once, before training starts, never inside the loop. The question below builds the NumPy-only version of this — same mini-batch structure, same reproducibility guarantee, still no `import torch` in your submission, but engineered the way production code actually is.
