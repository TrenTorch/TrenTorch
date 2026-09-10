Q1 and Q2 compute `sigmoid(z)` then `bce_loss(p, y)` as two separate steps. Real PyTorch code never does this. `torch.nn.functional.binary_cross_entropy_with_logits` (and the `BCEWithLogitsLoss` module wrapping it) computes both in one fused operation, working directly from the raw logits `z`, never materializing a separate probability `p` at all.

Why this matters beyond style: `sigmoid(z)` genuinely loses information for very negative or very positive `z` — once `z` is extreme enough, `sigmoid(z)` rounds to exactly `0.0` or `1.0` in floating point, and `bce_loss`'s clip then has to paper over a probability that's already lost precision. The fused version sidesteps this entirely using the log-sum-exp identity:

```text
BCEWithLogits(z, y) = max(z, 0) - z*y + log(1 + exp(-|z|))
```

This is mathematically identical to `-mean(y*log(sigmoid(z)) + (1-y)*log(1-sigmoid(z)))`, but every term stays well-behaved for any `z`, because the exponential only ever sees `-|z|` (always ≤ 0, never overflows) instead of `-z` (which can be arbitrarily large and positive). Real PyTorch:

```python
model = torch.nn.Linear(n_features, 1)
loss_fn = torch.nn.BCEWithLogitsLoss()   # fused sigmoid + BCE
optimizer = torch.optim.SGD(model.parameters(), lr=lr)

for X_batch, y_batch in dataloader:
    optimizer.zero_grad()
    z = model(X_batch).squeeze()          # raw logits, no sigmoid here
    loss = loss_fn(z, y_batch)             # sigmoid happens inside, fused
    loss.backward()
    optimizer.step()
```
