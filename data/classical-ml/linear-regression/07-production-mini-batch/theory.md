The naive training loop has two problems no production system tolerates:

**Full-batch doesn't scale.** Every single step recomputes the gradient over the _entire_ dataset. Fine for 300 rows. Impossible for 300 million — `X` alone won't fit in memory, let alone `X.T @ error`. Production training instead uses **mini-batch gradient descent**: shuffle the data once per epoch, split it into small batches, take one gradient step per batch. You never need more than one batch in memory at a time, and you get more update steps per epoch for free.

**Hand-derived gradients don't scale either.** The manual `dw = (2/n) X.T @ (y_hat - y)` formula was derivable by hand because linear regression is the simplest possible model. Nobody hand-derives gradients for a 96-layer transformer. Real PyTorch code never writes a gradient formula for this — it calls `.backward()` and lets autograd compute it. This is exactly why the Deep Learning Foundations section builds an autograd engine: it's the thing that makes manual calculus disappear from every model after this one.

A real production version of exactly what this track built looks like this:

```python
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

Every hand-written piece from this track maps onto exactly one line here. The question below builds the NumPy-only version of this — same mini-batch structure, still no `import torch` in your submission, but engineered the way production code actually is.
