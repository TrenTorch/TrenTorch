---
name: dl-training-batchnorm
title: 'Internal covariate shift, and what BatchNorm was actually designed to fix'
tags: [neural-networks, layers, training-dynamics]
difficulty: Advanced
---

## Statement

### The problem, from first principles

As a deep network trains, EVERY layer's weights are changing simultaneously, on every single step. This creates a subtle but real problem for any given layer, say, layer 5: the distribution of activations it RECEIVES from layer 4 keeps shifting around, not because layer 5's own input data changed, but because layers 1 through 4 upstream of it are all being updated too. Layer 5 essentially has to keep re-adapting to a constantly moving target, on top of the actual learning problem it's trying to solve, this shifting-distribution effect was named "internal covariate shift" in the original 2015 Batch Normalization paper (Ioffe & Szegedy), as the specific problem BatchNorm was designed to address (though later research has debated how much of BatchNorm's actual benefit really comes from directly fixing this effect, versus other side benefits, like smoothing the loss landscape, that come along with it).

`[02-layers/04-weight-initialization]` addresses a RELATED but distinct problem: getting activation variance right at the very START of training. BatchNorm addresses the SAME kind of variance-control problem, but continuously, DURING every single training step, by explicitly re-centering and re-scaling each layer's activations back to a controlled distribution (mean 0, variance 1, then rescaled by learnable `gamma`/`beta`) every time they pass through, regardless of how much the upstream layers have shifted since the last step.

### From theory to code

Implement `batchnorm_forward`. In TRAINING mode, compute the CURRENT batch's own mean and (biased) variance, per feature, normalize `x` using them, then rescale by the learnable `gamma` (scale) and `beta` (shift) parameters. Simultaneously, update `running_mean` and `running_var` (exponential moving averages, using `momentum`) so they track training statistics over time. In EVAL mode, skip computing batch statistics entirely and normalize using the STORED `running_mean`/`running_var` instead, this is what makes a single test-time sample (where "this batch's mean" would be meaningless, being just that one sample) still normalize sensibly.

### Constraints

- Training mode must use the CURRENT batch's mean and BIASED variance (`ddof=0`, NumPy's default for `.var()`) for the actual normalization of `x`.
- The `running_var` UPDATE specifically must use the batch's UNBIASED variance (`ddof=1`, i.e. `batch_var * n / (n - 1)`), matching `torch.nn.BatchNorm1d`'s exact convention, even though the normalization itself uses the biased variance.
- Eval mode must use `running_mean`/`running_var` directly, computing NO batch statistics at all, and must leave `running_mean`/`running_var` unchanged (no update in eval mode).
- `gamma` and `beta` must be applied AFTER normalization, as `gamma * x_norm + beta`, per feature.

### Hints

<details>
<summary>Hint 1: Training mode normalization</summary>

`batch_mean = x.mean(axis=0)` and `batch_var = x.var(axis=0)` (NumPy's `.var()` defaults to biased/population variance, exactly what's needed here). `x_norm = (x - batch_mean) / np.sqrt(batch_var + eps)`, then `out = gamma * x_norm + beta`.

</details>

<details>
<summary>Hint 2: The running_var subtlety</summary>

For the RUNNING statistics update only (not the normalization itself), convert the biased variance to unbiased: `batch_var_unbiased = batch_var * n / (n - 1)`, where `n = x.shape[0]`. Then `running_mean = (1 - momentum) * running_mean + momentum * batch_mean` and `running_var = (1 - momentum) * running_var + momentum * batch_var_unbiased`.

</details>

<details>
<summary>Hint 3: Eval mode</summary>

In eval mode, skip all of the above: `x_norm = (x - running_mean) / np.sqrt(running_var + eps)`, then `out = gamma * x_norm + beta`, exactly the same rescaling step as training mode, just using the stored running statistics instead of freshly-computed batch statistics.

</details>

## Theory

### The simple version

A thermostat that doesn't just set the temperature once and walk away, it continuously RE-MEASURES the room's current temperature and adjusts, every single moment, because the room keeps changing (a door opens, the sun moves, people enter and leave). BatchNorm is that continuous re-measurement, applied to a layer's activations instead of room temperature: rather than assuming a layer's activation distribution stays put once training starts, it re-centers and re-scales those activations back to a controlled, known distribution on every single forward pass, compensating for however much the upstream layers have shifted things since the last step.

### The formula

Training mode, for a batch of size `n`:

```
batch_mean = mean(x, axis=0)
batch_var = var(x, axis=0)                       # biased (ddof=0)

x_norm = (x - batch_mean) / sqrt(batch_var + eps)
out = gamma * x_norm + beta

batch_var_unbiased = batch_var * n / (n - 1)      # for the running update only
running_mean = (1 - momentum) * running_mean + momentum * batch_mean
running_var  = (1 - momentum) * running_var  + momentum * batch_var_unbiased
```

Eval mode:

```
x_norm = (x - running_mean) / sqrt(running_var + eps)
out = gamma * x_norm + beta
```

### How PyTorch actually implements this

`torch.nn.BatchNorm1d` (and its `BatchNorm2d`/`BatchNorm3d` siblings, for convolutional feature maps) implements exactly this formula, biased variance for normalization, unbiased variance specifically for the running-statistics update, a genuinely easy-to-miss detail confirmed directly against `torch.nn.BatchNorm1d`'s own output while building this question. `gamma` and `beta` are `nn.Parameter` instances (trained via ordinary backpropagation, exactly like any other layer's weights, via `[03-training-loop/02-assemble-training-loop]`'s training loop), while `running_mean`/`running_var` are registered as BUFFERS, not parameters, meaning they're tracked and saved/loaded with the model's state, but never receive a gradient or get updated by the optimizer directly, only through this forward pass's own exponential-moving-average logic. `[03-training-loop/03-train-eval-mode]`'s `self.training` flag is exactly what a real `BatchNorm1d.forward` checks to decide which of these two code paths (batch statistics vs. running statistics) to take, making BatchNorm, alongside `[02-layers/03-dropout]`, one of the two canonical reasons `model.eval()` genuinely changes a network's computed output, not just some bookkeeping flag with no numerical consequence.

## Explanation

Training mode computes `batch_mean`/`batch_var` (biased) from the current `x`, normalizes with them, and applies `gamma`/`beta`. Separately, it computes `batch_var_unbiased = batch_var * n / (n - 1)` and folds `batch_mean`/`batch_var_unbiased` into `running_mean`/`running_var` via the standard exponential-moving-average update, `(1 - momentum) * old + momentum * new`, matching `torch.nn.BatchNorm1d`'s exact bias-correction convention for the running variance specifically, even though normalization itself always uses the biased variance.

Eval mode skips computing any batch statistics at all: it normalizes directly against the stored `running_mean`/`running_var`, applies the same `gamma`/`beta` rescaling, and returns `running_mean`/`running_var` UNCHANGED, since eval-mode forward passes should never themselves update the tracked running statistics.
