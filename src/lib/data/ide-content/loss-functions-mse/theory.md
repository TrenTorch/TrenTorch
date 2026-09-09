# Theory: Mean Squared Error

## What

MSE averages the squared distance between every prediction and its target:

```
MSE = mean((y_pred - y_true) ** 2)
```

Squaring does two things at once: it makes every error positive (so overshooting and undershooting don't cancel out), and it penalizes large errors disproportionately more than small ones.

## Why squared, not absolute

You could average `|y_pred - y_true|` instead (that's L1 loss, also real and used elsewhere). MSE's advantage is that it's smooth and differentiable everywhere, including at zero error, which gives gradient descent a clean, well-behaved gradient to follow. L1's gradient is constant in magnitude regardless of how close the prediction already is, which makes it converge less smoothly near the optimum -- one of the tradeoffs a real model choice weighs.

## How it maps onto real PyTorch

`torch.nn.functional.mse_loss(y_pred, y_true)` computes exactly this. `nn.MSELoss()` is the module wrapper. This is the loss you'll pair with the linear regression hypothesis from the earlier question in this track: predict with `w * x + b`, score the prediction with MSE, then backpropagate through both.

## When to use it (and when not to)

Use MSE when predicting a continuous value and when large errors genuinely should cost more (a housing-price model being off by $100k is worse than being off by $10k, and worse than 10x as bad). Avoid it for classification -- squaring a probability error doesn't produce a well-calibrated gradient the way cross-entropy does (a later question in this curriculum). Also be cautious with MSE when your data has real outliers: because errors are squared, one wildly wrong prediction can dominate the whole loss and drag training toward fitting that outlier instead of the bulk of the data.

## Pros and cons

- **Pros:** smooth, convex when paired with a linear model, easy to reason about (units are "squared target units," and its square root, RMSE, is in the original units).
- **Cons:** sensitive to outliers (that squaring cuts both ways); not scale-invariant, so features and targets usually need normalizing first for stable training.

## At scale

MSE itself is cheap -- a subtraction, a square, and a mean, all vectorized. What actually matters at scale is what you compute it _over_: real training loops compute MSE per mini-batch (dozens to thousands of examples at once), not one example at a time, so the reduction (`mean`) is doing real work reducing a batch of losses down to the single scalar that `.backward()` needs to start from.
