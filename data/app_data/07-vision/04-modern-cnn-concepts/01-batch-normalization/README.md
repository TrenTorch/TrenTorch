---
name: vision-modern-batchnorm
title: Batch Normalization
tags: [computer-vision, cnn, normalization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Deep networks are hard to train because the distribution of activations flowing into each layer keeps shifting as the parameters of every earlier layer change during training. A layer that learned to work well with inputs centered around 0 with unit spread can suddenly see inputs centered around 50 a few steps later, and has to re-adapt. Batch normalization fixes this by explicitly re-centering and re-scaling the activations of every channel, every forward pass, using statistics computed from the current batch.

### From theory to code

Theory says: for each channel, compute the mean and variance of that channel's values across the whole batch (and across every spatial position), use them to standardize that channel to zero mean and unit variance, then apply a learned per-channel scale (`gamma`) and shift (`beta`) so the network can undo the standardization if that turns out to be better for a particular channel.

Implement `batch_norm2d(x, gamma, beta, eps=1e-5)` against that reasoning.

### Constraints

- `x`: shape `(N, C, H, W)` — a batch of feature maps.
- `gamma`, `beta`: shape `(C,)` — one learned scale and shift per channel.
- Statistics (mean, variance) are computed per channel, over the `N`, `H` and `W` axes together — not per-sample, not per-spatial-position.
- `eps` is added inside the square root purely to avoid division by zero when a channel's variance is (near) zero.
- Returns an array the same shape as `x`.
- `x`, `gamma` and `beta` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`x.mean(axis=(0, 2, 3), keepdims=True)` and `x.var(axis=(0, 2, 3), keepdims=True)` compute exactly the per-channel batch statistics you need, and `keepdims=True` keeps them broadcastable against the original `(N, C, H, W)` shape.

</details>

<details>
<summary>Hint 2</summary>

`gamma` and `beta` are shape `(C,)` but need to broadcast against `(N, C, H, W)` — reshape each to `(1, C, 1, 1)` before multiplying/adding.

</details>

## Theory

### The simple version

Imagine every channel of every layer has its own "thermostat." Batch normalization looks at all the values currently flowing through one channel (across the whole batch, at every pixel), figures out their average temperature and how much they're fluctuating, and resets them to a standard, comfortable range — centered at 0, spread of 1. Then it lets the network dial that thermostat back up or down (via `gamma` and `beta`) if a different range actually works better for that particular channel.

### The formula

```text
mean_c = mean(x[:, c, :, :])                     # scalar, per channel
var_c  = var(x[:, c, :, :])                      # scalar, per channel
x_norm[:, c, :, :] = (x[:, c, :, :] - mean_c) / sqrt(var_c + eps)
out[:, c, :, :]    = gamma[c] * x_norm[:, c, :, :] + beta[c]
```

### How PyTorch actually implements this

`torch.nn.BatchNorm2d` does exactly this during training, plus one thing this exercise skips: it also maintains a running (exponential moving average) estimate of the mean and variance seen across all of training, which is what gets used instead of batch statistics at evaluation time (`model.eval()`) — so a single test image doesn't get normalized using its own (meaningless, batch-of-one) statistics. `nn.BatchNorm2d`'s `gamma` and `beta` are its learnable `.weight` and `.bias` parameters, trained by backpropagation exactly like a `Linear` layer's weights.

## Explanation

`x.mean(axis=(0, 2, 3), keepdims=True)` and `x.var(axis=(0, 2, 3), keepdims=True)` reduce over every axis except the channel axis, producing one mean and one variance per channel, still shaped `(1, C, 1, 1)` so they broadcast cleanly against the full `(N, C, H, W)` input. Subtracting the mean and dividing by `sqrt(var + eps)` standardizes every channel independently to zero mean and unit variance across the batch — `eps` only matters when a channel happens to have near-zero variance, keeping the division numerically safe. Reshaping `gamma` and `beta` from `(C,)` to `(1, C, 1, 1)` lets the final `gamma_r * x_norm + beta_r` apply each channel's own learned scale and shift to every sample and every spatial position of that channel in one broadcasted operation.
